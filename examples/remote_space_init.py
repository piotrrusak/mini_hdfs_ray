import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import logging
logger = logging.getLogger(__name__)

from src.logger import setup_logging
setup_logging(logging.INFO) # logging.INFO/logging.WARNING/logging.ERROR/logging.DEBUG

from src.data_space import DataSpace

import ray
import time

ray.init(address="auto", namespace="hdfs")

manager = ray.get_actor("manager")
for _ in range(10):
    space = DataSpace.options(resources={"space": 1}).remote()
    manager.add_space.remote(space)

time.sleep(90)