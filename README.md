# Mandarake Auction Scraper — まんだらけ オークション

Scrapes auction listings (item name, price, bids, watchers, shop, images) from Mandarake (まんだらけ), Japan's premier second-hand anime, manga, figure, and collectibles marketplace. Supports 60+ categories, keyword search with pagination (800+ items/keyword), and RSS feed monitoring.

[![Apify Store](https://img.shields.io/badge/Apify-Store-blue)](https://apify.com/fruitful_quintessence/mandarake-auction-scraper)
[![MIT License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Output Sample

```json
[
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
]
```

## Input

```json
{
  "keyword": "フィギュア",
  "maxPages": 5,
  "proxyConfiguration": {
    "useApifyProxy": true,
    "apifyProxyCountry": "JP"
  }
}
```

Parameters:
- `keyword` (required) — Search term (Japanese characters supported)
- `category` (optional) — Filter by one of 60+ Mandarake categories
- `maxPages` (optional, default: 3) — Pages to scrape (30 items/page)
- `inStock` (optional) — Return only items with active bids

## Use Cases

- **Resale arbitrage** — Find undervalued items by comparing Mandarake auction prices to market rates
- **Price monitoring** — Track auction prices for specific collectibles over time
- **Market research** — Analyze bidding patterns, popular categories, and price distributions
- **Inventory feeds** — Feed structured auction data into LLMs for automated pricing analysis
- **Automated alerts** — Add a webhook URL to receive Slack/Discord/n8n notifications when new items match your search

## Integrations

This actor supports **Apify MCP Connectors** — connect your runs to Slack, Notion, Supabase, or GitHub without sharing credentials. Look for the "Connectors" tab on the run screen.

You can also schedule daily/hourly runs from the **Schedule** tab and receive results via **webhook** (add a `webhookUrl` in the input).

### Webhook Setup Examples

**Slack** — Create a Slack webhook:
1. Go to https://api.slack.com/apps → Create New App → Incoming Webhooks
2. Activate and copy the Webhook URL (looks like `https://hooks.slack.com/services/T00/B00/xxxxx`)
3. Paste it into the `webhookUrl` input field when running the actor
4. Result: Slack posts a message like "Mandarake Auction Scraper completed: 25 items found"

**Discord** — Create a Discord webhook:
1. Server Settings → Integrations → Webhooks → New Webhook
2. Copy the Webhook URL (looks like `https://discord.com/api/webhooks/xxxxx/yyyyy`)
3. Paste it into the `webhookUrl` input field

**n8n / Zapier** — Use any webhook trigger:
1. Create an n8n "Webhook" node or Zapier "Webhooks by Zapier" trigger
2. Copy the generated URL and paste into `webhookUrl`
3. The JSON payload includes: `event`, `actor`, `keyword`, `itemCount`, `datasetId`, `datasetUrl`

### Example: Scheduled Slack Alerts with Price Monitoring

1. Set up keyword search as usual
2. Add a Slack webhook URL to `webhookUrl`
3. Go to **Schedule** tab → Create a daily schedule
4. Every day at 9 AM, the actor runs and posts results to your Slack channel
5. Click the dataset link in Slack to open full results

## Pricing

- **$0.00005 per actor start** + **$0.001 per search** + **$0.00001 per result item**
- Typical 100-item search run: ~**$0.001** total
- You only pay for what you use — no monthly subscription

## Limitations

- Mandarake blocks aggressive crawling; respect the built-in rate limiting
- Images are hosted on Mandarake CDN and may expire after the auction ends
- We do not bypass CAPTCHAs; the actor respects robots.txt

## FAQ

**Does this work for Yahoo Auctions Japan?** No. This actor only scrapes Mandarake Auction. See our other actors.

**How fresh is the data?** Live at run time. We do not cache results.

**Can I run this on a schedule?** Yes. Use the Apify Schedule tab to run daily or hourly.

**Does this require an API key?** No. The actor scrapes publicly available listing pages.

## Changelog

- v0.2.1 (2026-07-29): Reduced pricing — start fee $0.00005, search $0.001
- v0.2.0 (2026-07-27): Added isPrimaryEvent pricing model
- v0.1.0 (2026-07-26): Initial release with keyword search and 60+ categories
