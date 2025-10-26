import logging

logger = logging.getLogger("network")

class Network:
    def __init__(self, mode="inpx-web"):
        self.mode = mode
        logger.info(f"Network initialized ({mode} mode)")
