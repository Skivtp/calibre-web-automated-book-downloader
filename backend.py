"""Backend facade for the downloader app (inpx-web only)."""

from pathlib import Path
from threading import Event
from typing import List, Optional, Callable

import book_manager
from models import SearchFilters, BookInfo


def queue_status():
    """Return current queue status (stub implementation)."""
    return {"status": "ok", "queue_length": 0}


def get_active_downloads():
    """Return list of active downloads (stub)."""
    return []


def search_books(query: str, filters: SearchFilters) -> List[BookInfo]:
    """Proxy to book_manager.search_books"""
    return book_manager.search_books(query, filters)


def get_book_info(book_id: str) -> BookInfo:
    """Proxy to book_manager.get_book_info"""
    return book_manager.get_book_info(book_id)


def download_book(
    book_info: BookInfo,
    book_path: Path,
    progress_callback: Optional[Callable[[float], None]] = None,
    cancel_flag: Optional[Event] = None,
) -> bool:
    """Proxy to book_manager.download_book"""
    return book_manager.download_book(book_info, book_path, progress_callback, cancel_flag)
