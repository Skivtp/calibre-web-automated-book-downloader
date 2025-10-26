"""Book download manager handling search and retrieval operations via inpx-web."""

from pathlib import Path
from typing import List, Optional, Callable
from threading import Event

import downloader
from logger import setup_logger
from models import BookInfo, SearchFilters
from inpx_backend import InpxWebBackend

logger = setup_logger(__name__)


def search_books(query: str, filters: SearchFilters) -> List[BookInfo]:
    """Search for books matching the query in inpx-web.

    Args:
        query: Search term (title, author, etc.)
        filters: SearchFilters (currently not deeply used)

    Returns:
        List[BookInfo]: List of matching books
    """
    backend = InpxWebBackend()
    results = backend.search(query)

    books: List[BookInfo] = []
    for r in results:
        books.append(
            BookInfo(
                id=r["download"],           # используем ссылку как id
                preview=None,               # inpx-web не отдаёт превью
                title=r["title"],
                author=r["author"],
                publisher="",
                year="",
                language="ru",
                format=r["format"] or "",
                size="",
                download_urls=[r["download"]],
            )
        )

    if not books:
        logger.info(f"No books found for query: {query}")
        raise Exception("No books found. Please try another query.")

    return books


def get_book_info(book_id: str) -> BookInfo:
    """Get detailed information for a specific book.

    Args:
        book_id: Book identifier (here it's just the download URL)

    Returns:
        BookInfo
    """
    # В нашем случае book_id = download_url
    return BookInfo(
        id=book_id,
        preview=None,
        title="",
        author="",
        publisher="",
        year="",
        language="ru",
        format="",
        size="",
        download_urls=[book_id],
    )


def download_book(
    book_info: BookInfo,
    book_path: Path,
    progress_callback: Optional[Callable[[float], None]] = None,
    cancel_flag: Optional[Event] = None,
) -> bool:
    """Download a book from inpx-web.

    Args:
        book_info: BookInfo with download_urls
        book_path: Path to save the book
        progress_callback: Optional callback for progress
        cancel_flag: Optional cancel event

    Returns:
        bool: True if successful
    """
    if not book_info.download_urls:
        logger.error("No download URLs available")
        return False

    url = book_info.download_urls[0]
    try:
        logger.info(f"Downloading `{book_info.title}` from `{url}`")
        data = downloader.download_url(url, "", progress_callback, cancel_flag)
        if not data:
            raise Exception("No data received")

        with open(book_path, "wb") as f:
            f.write(data.getbuffer())

        logger.info(f"Writing `{book_info.title}` successfully")
        return True
    except Exception as e:
        logger.error_trace(f"Failed to download from {url}: {e}")
        return False
