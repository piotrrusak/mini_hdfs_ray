import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
logger = logging.getLogger(__name__)

from src.logger import setup_logging
setup_logging(logging.INFO) # logging.INFO/logging.WARNING/logging.ERROR/logging.DEBUG

from src.data_manager import DataManager
from src.auto_healer import AutoHealer

import ray
import time

ray.init(address="auto", namespace="hdfs")

manager = DataManager.options(name="manager", resources={"manager": 1}).remote(15, 2)

time.sleep(90)