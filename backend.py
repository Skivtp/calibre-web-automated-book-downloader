"""Backend facade for the downloader app (inpx-web only)."""

from pathlib import Path
from threading import Event
from typing import List, Optional, Callable

import book_manager
from models import SearchFilters, BookInfo


def queue_status():
    return {"status": "ok", "queue_length": 0}


def get_active_downloads():
    return []


def search_books(query: str, filters: SearchFilters) -> List[BookInfo]:
    return book_manager.search_books(query, filters)


def get_book_info(book_id: str) -> BookInfo:
    return book_manager.get_book_info(book_id)


def download_book(
    book_info: BookInfo,
    book_path: Path,
    progress_callback: Optional[Callable[[float], None]] = None,
    cancel_flag: Optional[Event] = None,
) -> bool:
    return book_manager.download_book(book_info, book_path, progress_callback, cancel_flag)


def queue_book(book_id: str, priority: int = 0) -> bool:
    """Заглушка: сразу скачиваем книгу без очереди"""
    book_info = get_book_info(book_id)
    from pathlib import Path
    book_path = Path("/cwa-book-ingest") / f"{book_id}.fb2"
    return download_book(book_info, book_path)
