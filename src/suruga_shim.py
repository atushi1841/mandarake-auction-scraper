"""Shim to make Suruga-ya scraper importable from the comparison tool."""
import sys
from pathlib import Path

# Add the Suruga-ya scraper source to path
SURUGA_PATH = Path('/mnt/d/Project2/suruga-scraper/src')
if str(SURUGA_PATH) not in sys.path:
    sys.path.insert(0, str(SURUGA_PATH))

from scraper import scrape  # noqa: E402

# Re-export as different name to avoid confusion
suruga_scrape = scrape
__all__ = ['suruga_scrape']

