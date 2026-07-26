# Mandarake Auction Scraper (Apify Actor)

[Mandarake](https://ekizo.mandarake.co.jp) is a famous Japanese auction marketplace specializing in anime, manga, figures, toys, collectibles, and pop‑culture items. This Apify actor allows you to fetch item listings, view detailed information, and access the latest RSS feed.

## Features

- **Category Listing** – Scrape all items in a given category (e.g., `toys`, `figure`).
- **Item Detail** – Retrieve full details for a single item (description, end date, condition, multiple images).
- **RSS Feed** – Get the 31 most recently posted items in Japanese or English.

## Use Cases

- **Resale Research** – Monitor price trends and bidding activity.
- **Price Monitoring** – Track specific items or categories over time.
- **Collection Tracking** – Build datasets for personal collections or market analysis.

## How to Use

1. Run the actor on Apify.
2. Choose the **mode** (`category`, `rss`, or `detail`).
3. For **category** mode, select one of the available category slugs (default: `toys`).
4. For **detail** mode, provide the numeric `itemIndex` (found in the item URL).
5. The actor will output the scraped data as JSON.

## Data Fields

All field names are in English. Prices are integers. `scraped_at` is an ISO 8601 datetime. All URLs are absolute.

### Listing items

| Field | Description |
|-------|-------------|
| `item_index` | Numeric identifier (from URL) |
| `item_no` | Mandarake internal item number |
| `name` | Item title (Japanese) |
| `current_price_jpy` | Current bid price (JPY) |
| `start_price_jpy` | Starting price (JPY) |
| `bid_count` | Number of bids placed |
| `watch_count` | Number of watchers |
| `shop_name` | Name of the selling shop |
| `image_url` | Main image URL |
| `item_url` | Full detail page URL |
| `category` | Slug of the category scraped |
| `auction_type` | *(future use)* |
| `scraped_at` | Timestamp when the item was scraped |

### Detail (additional fields)

| Field | Description |
|-------|-------------|
| `description` | Text description of the item |
| `end_datetime` | Auction end date/time (ISO 8601) |
| `condition` | Condition statement |
| `category_path` | Breadcrumb category path |
| `all_images` | List of all image URLs |

## Requirements

- Python 3.11+
- `httpx`, `beautifulsoup4`, `lxml`, `apify` (installed automatically).

## License

MIT
