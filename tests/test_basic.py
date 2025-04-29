import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import ray
import pytest
import time
import string
import random

from src.data_manager import DataManager
from src.auto_healer import AutoHealer
from src.data_space import DataSpace

ray.init(ignore_reinit_error=True)

@pytest.fixture(scope="module")
def setup_system():
    dm = DataManager.remote(chunk_length=5, replication_factor=2)
    for _ in range(10):
        space = DataSpace.remote()
        dm.add_space.remote(space)
    ah = AutoHealer.remote(dm)
    ah.run.remote()
    time.sleep(1)
    return dm

def test_add_and_get(setup_system):
    dm = setup_system
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
    artifact_name = "test_" + ''.join(random.choices(string.ascii_lowercase, k=5))
    ray.get(dm.add.remote(artifact_name, random_string))
    time.sleep(1)
    result = ray.get(dm.get.remote(artifact_name))
    assert result == random_string

def test_update(setup_system):
    dm = setup_system
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
    artifact_name = "test_" + ''.join(random.choices(string.ascii_lowercase, k=5))
    ray.get(dm.add.remote(artifact_name, random_string))
    time.sleep(1)
    ray.get(dm.update.remote(artifact_name, random_string))
    time.sleep(1)
    result = ray.get(dm.get.remote(artifact_name))
    assert result == random_string

def test_get_after_kill(setup_system):
    dm = setup_system
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=100))
    artifact_name = "test_" + ''.join(random.choices(string.ascii_lowercase, k=5))
    time.sleep(1)
    ray.get(dm.add.remote(artifact_name, random_string))
    ray.get(dm.kill.remote(0))
    time.sleep(1)
    result = ray.get(dm.get.remote(artifact_name))
    assert result == random_string