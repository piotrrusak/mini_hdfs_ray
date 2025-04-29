from src.logger import setup_logging
setup_logging() # logging.INFO/logging.WARNING/logging.ERROR/logging.DEBUG

import logging
logger = logging.getLogger(__name__)

import ray
import time

@ray.remote
class AutoHealer:
    def __init__(self, dm):
        self.dm = dm

    def run(self):
        logger.info(f"Auto heal: Rozpoczynam działanie.")
        while True:
            time.sleep(10)
            logger.info(f"Auto-Heal: Wykonuje automatyczną procedure leczącą.")
            ray.get(self.dm.heal.remote())