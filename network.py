"""Network operations manager for the book downloader application.

Упрощённая версия для работы только с inpx-web.
"""

import urllib.request
from logger import setup_logger

logger = setup_logger(__name__)

# Настраиваем opener с User-Agent, чтобы сервер не блокировал запросы
opener = urllib.request.build_opener()
opener.addheaders = [
    (
        'User-agent',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/129.0.0.0 Safari/537.3'
    )
]
urllib.request.install_opener(opener)

def init():
    """Пустая функция для совместимости с downloader.py"""
    logger.info(
