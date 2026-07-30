"""Cross-Platform Price Comparison: Suruga-ya × Mandarake

Compares prices of the same/similar items across both platforms.
Can run standalone or be imported as a module.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


def normalize(name: str) -> str:
    """Normalize item name for matching."""
    n = name.lower().strip()
    n = re.sub(r'[〔〔【】「」『』《》（）()\[\]<>・･]', ' ', n)
    n = re.sub(r'\s+', ' ', n)
    n = re.sub(r'[※☆★◆◇◎◯○●▲△▼▽□■♯♪†‡]', '', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n


def extract_core_words(name: str) -> set[str]:
    """Extract meaningful core words for matching."""
    n = normalize(name)
    # Remove common suffixes
    n = re.sub(r'[（(].*?[）)]', '', n)  # (帯欠) etc.
    n = re.sub(r'[※].*', '', n)
    words = set()
    for w in n.split():
        w = w.strip()
        if len(w) >= 2 and not w.isascii():
            words.add(w)
        elif w.isascii() and len(w) >= 3:
            words.add(w)
    return words


def match_items(
    surugaya_items: list[dict[str, Any]],
    mandarake_items: list[dict[str, Any]],
    threshold: float = 0.3,
) -> list[dict[str, Any]]:
    """Match items across platforms by name similarity (Jaccard overlap)."""
    matched = []
    suruga_normalized = [(i, normalize(i.get('name', ''))) for i in surugaya_items]
    mandarake_normalized = [(i, normalize(i.get('name', ''))) for i in mandarake_items]

    for s_item, s_name in suruga_normalized:
        s_words = set(s_name.split())
        best_match = None
        best_score = 0.0
        best_m_item = None

        for m_item, m_name in mandarake_normalized:
            m_words = set(m_name.split())
            if not s_words or not m_words:
                continue
            intersection = s_words & m_words
            union = s_words | m_words
            score = len(intersection) / len(union) if union else 0.0

            # Bonus: exact substring match
            if s_name in m_name or m_name in s_name:
                score = max(score, 0.5)

            if score > best_score:
                best_score = score
                best_m_item = m_item
                best_match = m_name

        if best_score >= threshold and best_m_item:
            # Determine price direction
            s_price = s_item.get('used_price_jpy') or s_item.get('marketplace_price_jpy') or 0
            m_price = best_m_item.get('current_price_jpy') or best_m_item.get('start_price_jpy') or 0

            diff = s_price - m_price
            cheaper = 'surugaya' if diff > 0 else 'mandarake' if diff < 0 else 'same'
            diff_pct = round(abs(diff) / max(m_price, 1) * 100, 1) if m_price else 0

            matched.append({
                'surugaya_name': s_item.get('name', ''),
                'surugaya_price': s_price,
                'surugaya_url': s_item.get('url', ''),
                'mandarake_name': best_m_item.get('name', ''),
                'mandarake_price': m_price,
                'mandarake_url': best_m_item.get('item_url', ''),
                'price_diff_jpy': diff,
                'price_diff_pct': diff_pct,
                'cheaper_platform': cheaper,
                'match_score': round(best_score, 3),
                'surugaya_in_stock': s_item.get('in_stock', True),
                'mandarake_shop': best_m_item.get('shop_name', ''),
            })

    # Sort by biggest price difference first
    matched.sort(key=lambda x: abs(x['price_diff_jpy']), reverse=True)
    return matched


def format_comparison_table(matched: list[dict[str, Any]], keyword: str) -> str:
    """Format matched items as a readable table."""
    if not matched:
        return f'**【{keyword}】一致する商品は見つかりませんでした**'

    lines = [
        f'**【{keyword}】価格比較結果 — {len(matched)}件一致**',
        '',
        f'| # | Suruga-ya | 価格 | Mandarake | 価格 | 差額 | お得 |',
        f'|---|-----------|------|-----------|------|------|------|',
    ]

    for i, m in enumerate(matched[:15], 1):
        s_name = m['surugaya_name'][:35]
        m_name = m['mandarake_name'][:35]
        s_price = f"¥{m['surugaya_price']:,}" if m['surugaya_price'] else '?'
        m_price = f"¥{m['mandarake_price']:,}" if m['mandarake_price'] else '?'
        diff = m['price_diff_jpy']
        diff_str = f"¥{abs(diff):,}" if diff else '同額'
        if diff > 0:
            benefit = '🟢 駿河屋'
        elif diff < 0:
            benefit = '🔴 まんだらけ'
        else:
            benefit = '⚪ 同額'

        lines.append(f'| {i} | {s_name}... | {s_price} | {m_name}... | {m_price} | {diff_str} | {benefit} |')

    if len(matched) > 15:
        lines.append(f'| ... | 他 {len(matched) - 15} 件 | ... | ... | ... | ... | ... |')

    lines.extend([
        '',
        '**オススメ案件（¥1,000以上差額）:**',
    ])

    big_diffs = [m for m in matched if abs(m['price_diff_jpy']) >= 1000]
    if big_diffs:
        for m in big_diffs[:5]:
            direction = '駿河屋の方が安い' if m['price_diff_jpy'] > 0 else 'まんだらけの方が安い'
            url = f"  - Suruga: {m['surugaya_url']}" if m['surugaya_url'] else ''
            url2 = f"  - Mandarake: {m['mandarake_url']}" if m['mandarake_url'] else ''
            lines.append(f'- ¥{abs(m["price_diff_jpy"]):,}差 → {direction}')
            if url:
                lines.append(url)
            if url2:
                lines.append(url2)
    else:
        lines.append('（該当なし）')

    lines.append(f'\n*スコア閾値: 30%名一致, 表示件数: {len(matched)}件*')
    return '\n'.join(lines)


def compare_by_keyword(keyword: str, max_results: int = 10) -> dict[str, Any]:
    """Main comparison function. Returns structured comparison data."""
    import importlib.util
    import sys as _sys
    from pathlib import Path as _Path

    # Import Mandarake scraper FIRST (before Suruga-ya path pollutes the namespace)
    _M_PATH = str(_Path('/mnt/d/Project2/mandarake-scraper/src'))
    if _M_PATH not in _sys.path:
        _sys.path.insert(0, _M_PATH)
    # Force reimport to avoid Suruga-ya's 'scraper' module
    if 'scraper' in _sys.modules:
        del _sys.modules['scraper']
    import scraper
    mandarake_search = scraper.search_by_keyword
    importlib.reload(scraper)  # ensure fresh state

    # Import Suruga-ya scraper using importlib to avoid name collision
    _S_PATH = str(_Path('/mnt/d/Project2/suruga-scraper/src'))
    _S_SPEC = importlib.util.spec_from_file_location(
        'suruga_scraper_module',
        str(_Path(_S_PATH) / 'scraper.py')
    )
    _suruga_mod = importlib.util.module_from_spec(_S_SPEC)
    _sys.modules['suruga_scraper_module'] = _suruga_mod
    _S_SPEC.loader.exec_module(_suruga_mod)
    suruga_scrape = _suruga_mod.scrape

    # Scrape Suruga-ya
    suruga_path = suruga_scrape(
        keyword,
        max_pages=2,
        in_stock_only=True,
        output=f'/tmp/suruga_{keyword}.json'
    )
    surugaya_items = []
    if suruga_path:
        with open(suruga_path) as f:
            data = json.load(f)
        surugaya_items = data.get('items', [])

    # Search Mandarake
    mandarake_items = mandarake_search(keyword, max_results=max_results)

    # Match
    matched = match_items(surugaya_items, mandarake_items)

    return {
        'keyword': keyword,
        'surugaya_count': len(surugaya_items),
        'mandarake_count': len(mandarake_items),
        'matched_count': len(matched),
        'matches': matched,
    }


if __name__ == '__main__':
    keyword = sys.argv[1] if len(sys.argv) > 1 else 'フィギュア'
    result = compare_by_keyword(keyword)
    print(format_comparison_table(result['matches'], keyword))
    print(f'\n(Suruga-ya: {result["surugaya_count"]}件, Mandarake: {result["mandarake_count"]}件)')
