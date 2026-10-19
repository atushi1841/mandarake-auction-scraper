# Mandarake Auction Scraper — Japan Used Collectibles Auctions

> **Live on Apify:** [Mandarake Auction Japan Scraper - Used Collectibles Prices API](https://apify.com/fruitful_quintessence/mandarake-auction-scraper) — callable as a REST API from any language.

## What this actor does

This actor scrapes **live auction listings from Mandarake (まんだらけ)**, Japan's premier second-hand anime, manga, figure, and collectibles marketplace. It returns structured JSON — item name, current bid price in JPY, bid count, watcher count, selling shop, image, auction-end time, and a direct item URL — across more than **60 categories**.

Mandarake Auctions is where Japanese collectors buy and sell rare items: manga and doujinshi, anime figures, PVC action figures, trading cards and card packs, soft vinyl toys, model kits, retro games and hardware, records and CDs, animation cels, original art, and a long tail of niche hobby collectibles. Because it is an **auction** marketplace, the recorded price reflects real, time-stamped bidding pressure rather than a static shop tag — one of the best sources of live **Japanese marketplace data** for valuation.

The actor supports four modes: **category browsing**, **keyword search** with deep pagination (800+ items per keyword), **RSS feed monitoring** in Japanese or English, and **single-item detail lookup**. A built-in webhook lets you push run summaries to Slack, Discord, n8n, or Zapier the moment a run finishes.

## Input schema

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `mode` | select | `category` | `category` / `rss` / `detail` / `search` |
| `category` | select | `toys` | One of 60+ Mandarake category slugs (used in `category` mode) |
| `keyword` | string | `` | Search keyword (used in `search` mode) |
| `maxResults` | integer | `50` | Maximum items to return (1–200) |
| `maxPages` | integer | `2` | Pages to scrape for search / category modes (~40 items / page, max 20) |
| `itemIndex` | integer | `0` | Numeric item index for `detail` mode (found in the item URL) |
| `language` | select | `ja` | RSS feed language: `ja` or `en` |
| `webhookUrl` | string | `` | POST a JSON summary to this URL on completion |
| `proxyConfiguration` | proxy | JP proxy | Apify proxy configuration |

Example input (keyword search):

```json
{
  "mode": "search",
  "keyword": "フィギュア",
  "maxResults": 100,
  "maxPages": 5
}
```

## Output

Each item is written to the default Apify dataset in this shape:

```json
{
  "name": "フィギュア ドラゴンボール",
  "current_price_jpy": 3000,
  "bid_count": 5,
  "watcher_count": 12,
  "shop_name": "まんだらけ 中野店",
  "item_url": "https://order.mandarake.co.jp/auction/...",
  "image_url": "https://img.mandarake.co.jp/...",
  "end_time": "2026-08-15T20:00:00+09:00"
}
```

The `current_price_jpy`, `bid_count`, and `watcher_count` fields together let you gauge live demand for each item at a glance.

## Use cases

- **Price monitoring** — follow the current bid and buyout price of a specific collectible over time, and be alerted when a desirable item approaches your budget.
- **Market research** — analyze bidding patterns, watcher counts, and price distributions to understand what collectors are willing to pay in each category.
- **Resale arbitrage** — find undervalued auction items by comparing Mandarake bids to Mercari or Yahoo Auctions going prices, then flip for a margin.
- **Inventory feeds** — feed structured auction data into an LLM or vector database for automated pricing and curation.
- **Automated alerts** — add a `webhookUrl` to receive Slack, Discord, or n8n notifications whenever new items match your search.

## Why Japan data

Japan's collectibles auction market is global in reach but local in character — condition grading, product rarity, and demand nuances are specific to the Japanese market. Mandarake is the largest and most reputable venue for this in the country, and its live auction data gives the clearest signal of what collectors are actually bidding. For anyone dealing in anime figures, trading cards, retro games, manga, or original art, dependable access to this **Japanese marketplace data** is a genuine edge for both buying and pricing decisions.

## Pricing

Pay-per-event (**PPE**): **$0.005 per item** scraped, plus a small per-run start fee.

- A typical **100-item search run costs about $0.50**.
- No monthly subscription — you pay only for the items you actually capture.
- Charges accrue only on items successfully written to the dataset.

## FAQ

**Does this scrape Yahoo Auctions Japan?** No. This actor only scrapes Mandarake Auction. (See our separate Yahoo Auctions Japan scraper for that marketplace.)

**Do I need a Mandarake account or API key?** No. The actor scrapes publicly available listing and auction pages.

**Are the item titles in Japanese?** Yes — Mandarake is a Japanese site, so titles appear in Japanese (many product/model names are in English or Katakana).

**How fresh is the data?** Live. The actor fetches listing pages at execution time; nothing is cached.

**Can I run this on a schedule?** Yes — use the Apify **Schedule** tab to run daily or hourly for continuous auction monitoring.

**Can I get notified when the run finishes?** Yes — supply a `webhookUrl` and the actor will POST a JSON summary (including `event`, `actor`, `keyword`, `itemCount`, `datasetId`, `datasetUrl`) to your endpoint.

## Limitations

- Mandarake blocks aggressive crawling; respect the built-in rate limiting (1–3 s delays between requests).
- Images are hosted on the Mandarake CDN and may expire after the auction ends.
- The actor does not bypass CAPTCHAs and respects `robots.txt`.

## Integrations

Works with Apify **Connectors** (Slack, Google Sheets, Notion, Supabase, GitHub) and webhooks. Combine with a **Schedule** to build a fully automated collectibles auction-monitoring pipeline.

---

## Gumroad Products

- [FREE Sample – Japan Hobby & Collectibles Market Price Dataset](https://atushi5.gumroad.com/l/kutuxe?utm_source=github_readme&utm_medium=readme&utm_campaign=japan_hobby)
- [Japanese Anime Figure & Collectibles Market Price Dataset (Weekly CSV)](https://atushi5.gumroad.com/l/agyhq?utm_source=github_readme&utm_medium=readme&utm_campaign=japan_hobby)
- [週次レポート｜日本ホビー・中古市場マーケット動向](https://atushi5.gumroad.com/l/qdyyyi?utm_source=github_readme&utm_medium=readme&utm_campaign=japan_hobby)

> Source data: [Apify Store – fruitful_quintessence](https://apify.com/fruitful_quintessence)
