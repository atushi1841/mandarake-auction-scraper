"""
Tests for Mandarake Auction Scraper output data format.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import MandarakeItem, MandarakeItemDetail


def test_mandarake_item_to_dict():
    """MandarakeItem.to_dict() must produce expected field names."""
    item = MandarakeItem(
        name="テスト商品",
        item_index=123,
        item_no="ABC-456",
        current_price_jpy=1000,
        start_price_jpy=500,
        bid_count=3,
        watch_count=10,
        shop_name="Test Shop",
        image_url="https://example.com/img.jpg",
        item_url="https://example.com/1",
        category="toys",
        auction_type="通常",
        scraped_at="2026-07-29T00:00:00Z",
    )
    d = item.to_dict()
    assert d["name"] == "テスト商品"
    assert d["current_price_jpy"] == 1000
    assert d["start_price_jpy"] == 500
    assert d["item_url"] == "https://example.com/1"
    assert d["category"] == "toys"


def test_mandarake_item_detail_fields():
    """MandarakeItemDetail must have extra fields."""
    detail = MandarakeItemDetail(
        name="詳細商品",
        item_index=456,
        item_no="DEF-789",
        current_price_jpy=2000,
        start_price_jpy=1500,
        bid_count=5,
        watch_count=20,
        shop_name="Detail Shop",
        image_url="https://example.com/img2.jpg",
        item_url="https://example.com/2",
        category="figure",
        auction_type="出品",
        scraped_at="2026-07-29T12:00:00Z",
        description="レアアイテムの詳細説明",
        end_datetime="2026-12-31T23:59:59Z",
    )
    d = detail.to_dict()
    assert d["name"] == "詳細商品"
    assert d["description"] == "レアアイテムの詳細説明"
    assert d["end_datetime"] == "2026-12-31T23:59:59Z"
