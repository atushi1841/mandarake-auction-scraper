# Mandarake Auction Scraper — まんだらけ オークション

**Scrape Japanese auction listings from Mandarake (まんだらけ), Japan's premier second-hand anime, manga, figure, and collectibles marketplace.**  
60+ categories, keyword search with pagination (800+ items/keyword), RSS feed, and item detail extraction in clean structured JSON.

[![Apify Store](https://img.shields.io/badge/Apify-Store-blue)](https://apify.com/fruitful_quintessence/mandarake-auction-scraper)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🚀 Quick Start on Apify

1. Go to [Mandarake Auction Scraper on Apify Store](https://apify.com/fruitful_quintessence/mandarake-auction-scraper)
2. Click **"Try"** or **"Start"**
3. Select a category or enter a keyword
4. Run and get your data as JSON, CSV, or XLSX

**Pricing:** Pay per event — $0.005/run + $0.001/search. Free plan available for testing.

---

## 📋 What You Can Extract

| Data Point | Description |
|-----------|-------------|
| Item name | Japanese title of the auction listing |
| Current price (JPY) | Active bid amount in yen |
| Start price (JPY) | Opening bid price |
| Bid count | Number of bids placed |
| Watch count | Number of watchers |
| Shop name | Name of the selling Mandarake shop |
| Main image URL | Product thumbnail |
| Full description | Item details and condition (detail mode) |
| End date/time | Auction closing timestamp |
| Category path | Breadcrumb navigation |
| All images | Every product image (detail mode) |

---

## 🔥 Why This Scraper?

| Feature | This Scraper | Competition |
|---------|:-----------:|:-----------:|
| Category listing (60+ categories) | ✅ | ✅ |
| **Multi-page keyword search** (800+ items) | ✅ **Unique** | ❌ |
| Item detail (description, end date, images) | ✅ | ✅ |
| RSS feed (Japanese & English) | ✅ | ✅ |
| Bid count & watch count | ✅ | ✅ |
| Shop name & type | ✅ | ✅ |
| All images (detail mode) | ✅ | ✅ |
| **Crawl-delay compliant** (polite scraping) | ✅ | varies |
| maxResults: 50 per keyword | ✅ | varies |

**🚩 Unique advantage:** Keyword search with multi-page pagination — up to **800+ items** per keyword (40 items/page × 20 pages). No other Mandarake scraper offers this.

---

## 🎯 Use Cases

1. **Resale & arbitrage research** — Find underpriced items by monitoring bid activity across categories
2. **Price trend monitoring** — Track specific items or categories over days/weeks
3. **Collection & valuation tracking** — Build datasets for insurance, appraisal, or personal collection management
4. **Proxy buying integration** — Feed Mandarake auction data into proxy/service platforms
5. **Market research (Japan collectibles)** — Analyze pricing, demand, and category trends in the Japanese second-hand anime/collectibles market
6. **AI/ML training data** — Build datasets for price prediction, demand forecasting, or recommendation models

---

## 📂 Supported Categories

60+ categories including:

- 漫画 (Manga) — 少年漫画・少女漫画・同人誌
- フィギュア (Figures) — スケールフィギュア・ねんどろいど・プライズ
- ゲーム (Games) — 家庭用ゲーム・携帯ゲーム・レトロゲーム
- トレーディングカード (Trading Cards) — ポケカ・遊戯王・MTG
- DVD/Blu-ray — アニメ・映画・特撮
- CD — アニソン・サントラ・声優
- 玩具 (Toys) — プラモデル・食玩・ぬいぐるみ
- アパレル (Apparel) — Tシャツ・キャップ・バッグ
- And more — 30+ additional niche categories

---

## 🏗 Architecture

```
User Input → mode selection (category / search / rss / detail)
                  ↓
        httpx HTTP client (retry + backoff)
                  ↓
        HTML/RSS parser (BeautifulSoup + lxml)
                  ↓
        Structured item dict (price, bids, images, etc.)
                  ↓
        Apify Dataset → JSON / CSV / XLSX export
```

- **Polite scraping:** 15-second crawl delay between pages
- **Reliable parsing:** httpx with retry + backoff for network resilience
- **Clean output:** Every field validated and typed before storage

---

## ⚙️ Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | select | category | category / rss / detail / search |
| `category` | select | toys | Category slug (category mode) |
| `keyword` | string | — | Search keyword (search mode) |
| `maxPages` | int | 2 | Max pages for paginated modes |
| `itemIndex` | int | — | Item index (detail mode) |
| `language` | select | ja | RSS language (rss mode) |
| `maxResults` | int | 50 | Max items per keyword |

---

## 🔧 Development / Self-Host

```bash
# Requirements
pip install httpx beautifulsoup4 lxml apify

# Run locally
python src/main.py

# Deploy to Apify
npx apify push
```

---

## 📄 Output Schema

Full schema is defined in `.actor/actor.json`. Each run produces a dataset with consistent, validated fields.

---

## 📝 License

MIT — free for commercial and personal use. The scraper itself is MIT-licensed; please respect Mandarake's terms of service and robots.txt when running at scale.

---

*Built for collectors, resellers, and data analysts who need reliable Japanese auction data.*
