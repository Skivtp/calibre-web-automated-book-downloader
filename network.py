import logging

logger = logging.getLogger("network")

class Network:
    def __init__(self, mode="inpx-web"):
        self.mode = mode
        logger.info(f"Network initialized ({mode} mode)")

# --- добавляем init() для совместимости ---
_instance = None

def init(mode="inpx-web"):
    global _instance
    if _instance is None:
        _instance = Network(mode)
    return _instance
