"""
Core scraper module for Mandarake Auction.

Fetch listing, item detail, and RSS feed.
"""

import re
import logging
from datetime import datetime, timezone
from typing import Optional

import httpx
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

BASE_URL = "https://ekizo.mandarake.co.jp"

CATEGORIES = {
    "manga-books": "Manga",
    "manga_before_1965": "Manga (pre-1965)",
    "manga_after_1965": "Manga (post-1965)",
    "furoku": "Furoku",
    "magazines": "Magazines",
    "mook": "Mook",
    "culture": "Culture",
    "spiritual": "Spiritual",
    "bungei-sf": "Bungei/SF",
    "art-design-photo": "Art/Design/Photo",
    "music": "Music",
    "books-others": "Books (Others)",
    "toys": "Toys",
    "soft_vinyl": "Soft Vinyl",
    "indy_sofvi": "Indy Sofvi",
    "plamo": "Plastic Models",
    "gokin": "Die-cast (Gokin)",
    "plastic_toys": "Plastic Toys",
    "ametoy": "Ametoy",
    "figure": "Figure",
    "pvc_action_figure": "PVC Action Figure",
    "trading_figure": "Trading Figure",
    "doll": "Doll",
    "stuffed_toy": "Stuffed Toy",
    "figure-parts": "Figure Parts",
    "figure-others": "Figure (Others)",
    "cd": "CD",
    "record": "Record",
    "tape": "Tape",
    "music-others": "Music (Others)",
    "dvd-bluray": "DVD/Blu-ray",
    "video": "Video",
    "video-others": "Video (Others)",
    "game": "Game",
    "game_hardware": "Game Hardware",
    "game_software": "Game Software",
    "game_others": "Game (Others)",
    "card": "Card",
    "card_single": "Card (Single)",
    "card_box": "Card (Box)",
    "card_deck": "Card (Deck)",
    "card_supply": "Card (Supply)",
    "card-others": "Card (Others)",
    "poster": "Poster",
    "cell": "Cell",
    "cel-others": "Cell (Others)",
    "manga_original_art": "Manga Original Art",
    "keychain": "Keychain",
    "strap": "Strap",
    "badge": "Badge",
    "pen": "Pen",
    "towel": "Towel",
    "clock": "Clock",
    "bag": "Bag",
    "goods-others": "Goods (Others)",
    "apparel": "Apparel",
    "watch": "Watch",
    "accessory": "Accessory",
    "model_kit": "Model Kit",
    "anime_supply": "Anime Supply",
    "interior": "Interior",
    "hobby-others": "Hobby (Others)",
}

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ja-JP,ja;q=0.9,en;q=0.8",
}


def _make_client() -> httpx.Client:
    """Create httpx client with retry transport."""
    transport = httpx.HTTPTransport(retries=3)
    return httpx.Client(
        transport=transport,
        headers=HEADERS,
        timeout=30.0,
    )


def _clean_int(value: str) -> int:
    """Parse a price or count string (e.g. '¥5,000' or '1,200') into int."""
    cleaned = re.sub(r"[^\d\-]+", "", value)
    if cleaned == "":
        return 0
    return int(cleaned)


def _clean_price(value: str) -> int:
    """Remove non-digits and return integer."""
    digits = re.sub(r"\D", "", value)
    if digits == "":
        return 0
    return int(digits)


def _make_absolute(url: str, base_path: str = "") -> str:
    """Convert relative URL to absolute. base_path is the directory prefix to prepend for relative URLs."""
    if url.startswith("http"):
        return url
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return BASE_URL + url
    if base_path:
        return BASE_URL + base_path + url
    return BASE_URL + "/" + url


def _is_item_block(block) -> bool:
    """Check if a div.block contains actual auction item data."""
    return bool(block.find("span", id="itemNo"))


def _parse_item_block(block, category: str = "") -> dict:
    """Parse a single item div.block into a dictionary."""
    scraped_at = datetime.now(timezone.utc).isoformat()

    item_no_el = block.find("span", id="itemNo")
    item_no = item_no_el.get_text(strip=True) if item_no_el else ""

    name_el = block.find("span", id="itemName")
    name = name_el.get_text(strip=True) if name_el else ""

    now_el = block.find("span", id="nowPrice")
    current_price_jpy = _clean_price(now_el.get_text(strip=True)) if now_el else 0

    start_el = block.find("span", id="startPrice")
    start_price_jpy = _clean_price(start_el.get_text(strip=True)) if start_el else 0

    bid_el = block.find("span", id="bidCount")
    bid_count = _clean_int(bid_el.get_text(strip=True)) if bid_el else 0

    watch_el = block.find("span", id="watchCount")
    watch_count = _clean_int(watch_el.get_text(strip=True)) if watch_el else 0

    shop_el = block.find("span", id="shopName")
    shop_name = shop_el.get_text(strip=True) if shop_el else ""

    auction_el = block.find("span", id="auctionName")
    auction_type = auction_el.get_text(strip=True) if auction_el else ""

    img_el = block.find("img", id="thumbnail")
    image_url = _make_absolute(img_el.get("src")) if img_el else ""

    link_el = block.find("a", href=re.compile(r"itemInfoJa\.html\?index=\d+"))
    if link_el:
        href = link_el.get("href")
        item_url = _make_absolute(href, base_path="/auction/item/")
        match = re.search(r"index=(\d+)", href)
        item_index = int(match.group(1)) if match else 0
    else:
        item_url = ""
        item_index = 0

    return {
        "item_index": item_index,
        "item_no": item_no,
        "name": name,
        "current_price_jpy": current_price_jpy,
        "start_price_jpy": start_price_jpy,
        "bid_count": bid_count,
        "watch_count": watch_count,
        "shop_name": shop_name,
        "image_url": image_url,
        "item_url": item_url,
        "category": category,
        "auction_type": auction_type,
        "scraped_at": scraped_at,
    }


def fetch_listing(
    category: Optional[str] = None,
    page: int = 1,
) -> list[dict]:
    """Fetch listing page and return list of item dictionaries."""
    params = {}
    if category:
        params["category"] = category
    if page > 1:
        params["page"] = page

    url = f"{BASE_URL}/auction/item/itemsListJa.html"
    client = _make_client()
    try:
        resp = client.get(url, params=params)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error("Failed to fetch listing: %s", exc)
        return []
    finally:
        client.close()

    soup = BeautifulSoup(resp.text, "lxml")
    all_blocks = soup.find_all("div", class_="block")
    item_blocks = [b for b in all_blocks if _is_item_block(b)]
    logger.info("Found %d item blocks out of %d total blocks", len(item_blocks), len(all_blocks))

    items = []
    for block in item_blocks:
        items.append(_parse_item_block(block, category or ""))
    return items


def fetch_item_detail(item_index: int) -> dict:
    """Fetch single item detail page and return dictionary with rich fields."""
    url = f"{BASE_URL}/auction/item/itemInfoJa.html?index={item_index}"
    client = _make_client()
    try:
        resp = client.get(url)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error("Failed to fetch item detail %s: %s", item_index, exc)
        return {}
    finally:
        client.close()

    soup = BeautifulSoup(resp.text, "lxml")
    scraped_at = datetime.now(timezone.utc).isoformat()

    item_no_el = soup.find("span", id="itemNo")
    item_no = item_no_el.get_text(strip=True) if item_no_el else ""

    name_el = soup.find("span", id="itemName")
    name = name_el.get_text(strip=True) if name_el else ""

    now_el = soup.find("span", id="nowPrice-1") or soup.find("span", id="nowPrice")
    current_price_jpy = _clean_price(now_el.get_text(strip=True)) if now_el else 0

    start_el = soup.find("span", id="startPrice")
    start_price_jpy = _clean_price(start_el.get_text(strip=True)) if start_el else 0

    bid_el = soup.find("span", id="bidCount")
    bid_count = _clean_int(bid_el.get_text(strip=True)) if bid_el else 0

    watch_el = soup.find("span", id="watchCount")
    watch_count = _clean_int(watch_el.get_text(strip=True)) if watch_el else 0

    shop_el = soup.find("span", id="shopName")
    shop_name = shop_el.get_text(strip=True) if shop_el else ""

    auction_el = soup.find("span", id="auctionName")
    auction_type = auction_el.get_text(strip=True) if auction_el else ""

    img_el = soup.find("img", id="thumbnail") or soup.find("img", src=re.compile(r"aucimg"))
    image_url = _make_absolute(img_el.get("src")) if img_el else ""

    # Detail-specific fields
    # Description
    desc_el = soup.find("div", class_="item_description")
    description = desc_el.get_text(" ", strip=True) if desc_el else ""

    # End date
    end_el = soup.find("span", id="strExtCloseDate")
    end_datetime_str = end_el.get_text(strip=True) if end_el else ""
    end_datetime = ""
    if end_datetime_str:
        try:
            dt_obj = datetime.strptime(end_datetime_str, "%Y/%m/%d %H:%M:%S")
            end_datetime = dt_obj.replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            end_datetime = end_datetime_str

    # Condition & category are not consistently present; skip for MVP
    condition = ""
    category_path = ""

    # All images
    all_images = []
    for img in soup.find_all("img", src=re.compile(r"aucimg")):
        src = img.get("src")
        if src:
            abs_src = _make_absolute(src)
            if abs_src not in all_images:
                all_images.append(abs_src)

    return {
        "item_index": item_index,
        "item_no": item_no,
        "name": name,
        "current_price_jpy": current_price_jpy,
        "start_price_jpy": start_price_jpy,
        "bid_count": bid_count,
        "watch_count": watch_count,
        "shop_name": shop_name,
        "image_url": image_url,
        "item_url": f"{BASE_URL}/auction/item/itemInfoJa.html?index={item_index}",
        "category": "",
        "auction_type": auction_type,
        "scraped_at": scraped_at,
        "description": description,
        "end_datetime": end_datetime,
        "condition": condition,
        "category_path": category_path,
        "all_images": all_images,
    }


def fetch_rss(language: str = "ja") -> list[dict]:
    """Parse RSS feed (RSS 2.0, despite .rdf extension) and return list of item dictionaries."""
    suffix = "-en" if language == "en" else ""
    url = f"{BASE_URL}/rss/auction{suffix}.rdf"
    client = _make_client()
    try:
        resp = client.get(url)
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        logger.error("Failed to fetch RSS: %s", exc)
        return []
    finally:
        client.close()

    rss_data = []
    try:
        root = ET.fromstring(resp.text)
    except ET.ParseError as exc:
        logger.error("Failed to parse RSS XML: %s", exc)
        return []

    # The file is RSS 2.0 (despite .rdf extension)
    for item_el in root.findall(".//item"):
        title_el = item_el.find("title")
        link_el = item_el.find("link")
        pub_date_el = item_el.find("pubDate")
        enclosure_el = item_el.find("enclosure")

        title = title_el.text if title_el is not None and title_el.text else ""
        link = link_el.text if link_el is not None and link_el.text else ""
        pub_date_str = pub_date_el.text if pub_date_el is not None and pub_date_el.text else ""
        image_url = enclosure_el.get("url", "") if enclosure_el is not None else ""

        item_index = 0
        if "index=" in link:
            match = re.search(r"index=(\d+)", link)
            if match:
                item_index = int(match.group(1))

        rss_data.append({
            "item_index": item_index,
            "name": title,
            "item_url": link,
            "image_url": image_url,
            "published_date": pub_date_str,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
        })
    return rss_data
