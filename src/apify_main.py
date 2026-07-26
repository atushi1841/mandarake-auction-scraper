"""
Apify actor entry point for Mandarake Auction Scraper.
"""
import logging
import sys

from apify import Actor

from scraper import fetch_listing, fetch_item_detail, fetch_rss, CATEGORIES
from models import MandarakeItem, MandarakeItemDetail

logger = logging.getLogger(__name__)


async def main() -> None:
    """Main entry point for Apify actor."""
    await Actor.init()
    try:
        input_data = await Actor.get_input() or {}
        mode = input_data.get("mode", "category")
        category = input_data.get("category", "toys")
        item_index = input_data.get("itemIndex")

        if mode == "category":
            items = fetch_listing(category=category, page=1)
            if not items:
                logger.warning("No items fetched for category %s", category)
            # Convert to model and push
            for item in items:
                obj = MandarakeItem(**item)
                await Actor.push_data(obj.to_dict())
            logger.info("Pushed %d items for category %s", len(items), category)

        elif mode == "rss":
            language = input_data.get("language", "ja")  # optional
            items = fetch_rss(language=language)
            # RSS items have fewer fields; we can still push as dicts
            for item in items:
                await Actor.push_data(item)
            logger.info("Pushed %d RSS items", len(items))

        elif mode == "detail":
            if item_index is None:
                logger.error("itemIndex is required for detail mode")
                # still push empty? just output error
                await Actor.fail(status_message="itemIndex required for detail mode")
                return
            detail = fetch_item_detail(item_index)
            if not detail:
                logger.warning("No detail fetched for index %s", item_index)
            obj = MandarakeItemDetail(**detail)
            await Actor.push_data(obj.to_dict())
            logger.info("Pushed detail for index %s", item_index)

        else:
            logger.error("Unknown mode: %s", mode)
            await Actor.fail(status_message=f"Unknown mode: {mode}")

    except Exception as exc:
        logger.exception("Actor run failed")
        await Actor.fail(status_message=str(exc))
    finally:
        await Actor.exit()


import asyncio

if __name__ == "__main__":
    asyncio.run(main())
