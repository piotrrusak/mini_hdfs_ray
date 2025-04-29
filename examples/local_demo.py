import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
logger = logging.getLogger(__name__)

from src.logger import setup_logging
setup_logging(logging.INFO) # logging.INFO/logging.WARNING/logging.ERROR/logging.DEBUG

from src.data_manager import DataManager
from src.auto_healer import AutoHealer
from src.data_space import DataSpace

import ray
import time

ray.init()

dm = DataManager.remote(15, 2)

for _ in range(10):
    space = DataSpace.remote()
    dm.add_space.remote(space)

ah = AutoHealer.remote(dm)
ah.run.remote()

ray.get(dm.add.remote("test", "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"))

time.sleep(2)

logger.warning(f"Result: {ray.get(dm.get.remote('test'))}")

dm.kill.remote(2)

time.sleep(4)

ray.get(dm.update.remote("test", "xyz"))

time.sleep(2)

logger.warning(f"Result: {ray.get(dm.get.remote('test'))}")

time.sleep(2)

ray.get(dm.update.remote("test", "abcdefghijklmnopqrstuvwxyz"))

time.sleep(2)

dm.list_artifacts.remote()

time.sleep(1)

dm.list_spaces.remote()

logger.warning(f"Result: {ray.get(dm.get.remote('test'))}")
