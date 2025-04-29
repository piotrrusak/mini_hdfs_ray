from src.logger import setup_logging
setup_logging() # logging.INFO/logging.WARNING/logging.ERROR/logging.DEBUG

import logging
logger = logging.getLogger(__name__)

class Artifact:
    def __init__(self):
        self.quantity_of_chunks = 0

        self.chunk_locations = []

    def add(self, locations):
        self.chunk_locations.append(locations)
        self.quantity_of_chunks += 1

    def list(self):
        for i in range(self.quantity_of_chunks):
            logger.info(f"Artifact: Lista lokalizacji chunka: {i} to: {self.chunk_locations[i]}")