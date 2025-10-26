"""Network operations manager for the book downloader application (simplified for inpx-web)."""

import urllib.request
from logger import setup_logger

logger = setup_logger(__name__)

# Настраиваем opener с User-Agent
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
    """Dummy init for compatibility."""
    logger.info("Network initialized (inpx-web mode)")
    pass
