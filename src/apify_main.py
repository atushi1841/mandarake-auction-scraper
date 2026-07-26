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
        max_results = int(input_data.get("maxResults", 25))
        if max_results < 1:
            max_results = 1

        if mode == "category":
            # Empty category = all items. Specific category slugs are available
            # but the site may not filter by them reliably.
            cat = category if category and category != "toys" else ""
            items = fetch_listing(category=cat, page=1)
            if not items:
                logger.warning("No items fetched for category %s", category)
            # Limit to maxResults
            items = items[:max_results]
            # Convert to model and push
            for item in items:
                obj = MandarakeItem(**item)
                await Actor.push_data(obj.to_dict())
            logger.info("Pushed %d items for category %s", len(items), category)
            await Actor.set_status_message(f"Returned {len(items)} items for category mode")

        elif mode == "rss":
            language = input_data.get("language", "ja")  # optional
            items = fetch_rss(language=language)
            # Limit to maxResults
            items = items[:max_results]
            # RSS items have fewer fields; we can still push as dicts
            for item in items:
                await Actor.push_data(item)
            logger.info("Pushed %d RSS items", len(items))
            await Actor.set_status_message(f"Returned {len(items)} RSS items")

        elif mode == "detail":
            if item_index is None:
                logger.error("itemIndex is required for detail mode")
                # still push empty? just output error
                await Actor.fail(status_message="itemIndex required for detail mode")
                return
            detail = fetch_item_detail(item_index)
            if not detail:
                logger.warning("No detail fetched for index %s", item_index)
            # Treat as list to unify limiting
            items = [detail] if detail else []
            items = items[:max_results]
            for item in items:
                obj = MandarakeItemDetail(**item)
                await Actor.push_data(obj.to_dict())
            logger.info("Pushed %d detail items for index %s", len(items), item_index)
            await Actor.set_status_message(f"Returned {len(items)} detail items")

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
