from src.logger import setup_logging
setup_logging() # logging.INFO/logging.WARNING/logging.ERROR/logging.DEBUG

import logging
logger = logging.getLogger(__name__)

import ray

@ray.remote
class DataSpace:
    def __init__(self):
        self.storage = {}
    def check_status(self):
        return True
    def add(self, name, data):
        if name not in self.storage.keys():
            self.storage[name] = data
    def update(self, name, data):
        if name in self.storage.keys():
            self.storage[name] = data
    def remove(self, name):
        if name in self.storage.keys():
            self.storage.pop(name)
    def get(self, name):
        return self.storage[name]
    def list(self):
        logger.info(f"Data-Space: {self.storage}")