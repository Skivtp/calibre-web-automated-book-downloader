import logging
from pathlib import Path
from urllib.parse import urlparse
import os

import downloader
import inpx_backend
from models import SearchFilters, BookInfo

logger = logging.getLogger("book_manager")


def search_books(query: str, filters: SearchFilters):
    return inpx_backend.InpxWebBackend().search(query)


def get_book_info(book_id: str) -> BookInfo:
    # book_id у нас фактически = URL для скачивания
    return BookInfo(id=book_id, title="", author="", download_urls=[book_id])


def download_book(book_info: BookInfo, book_path: Path, progress_callback=None, cancel_flag=None) -> bool:
    url = book_info.download_urls[0]
    try:
        logger.info(f"Downloading `{book_info.title}` from `{url}`")
        data = downloader.download_url(url, "", progress_callback, cancel_flag)
        if not data:
            raise Exception("No data received")

        parsed = urlparse(url)
        filename = os.path.basename(parsed.path) or "book.fb2"
        book_path = Path("/cwa-book-ingest") / filename

        with open(book_path, "wb") as f:
            f.write(data.getbuffer())

        logger.info(f"Writing `{book_info.title}` successfully to {book_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download from {url}: {e}", exc_info=True)
        return False
