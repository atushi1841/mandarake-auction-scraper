"""
Data models for Mandarake Auction items.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class MandarakeItem:
    """Basic item fields from listing page."""
    item_index: int
    item_no: str
    name: str
    current_price_jpy: int
    start_price_jpy: int
    bid_count: int
    watch_count: int
    shop_name: str
    image_url: str
    item_url: str
    category: str
    auction_type: str
    scraped_at: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class MandarakeItemDetail(MandarakeItem):
    """Extended item fields from detail page."""
    description: str = ""
    end_datetime: str = ""
    condition: str = ""
    category_path: str = ""
    all_images: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
