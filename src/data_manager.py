from src.logger import setup_logging
setup_logging() # logging.INFO/logging.WARNING/logging.ERROR/logging.DEBUG

import logging
logger = logging.getLogger(__name__)

from src.data_space import DataSpace
from src.artifact import Artifact

import ray
import numpy as np
import random

@ray.remote
class DataManager:
    def __init__(self, chunk_length, replication_factor):
        self.chunk_length = chunk_length
        self.replication_factor = replication_factor

        self.spaces = []
        self.spaces_blackset = set()
        self.artifacts = {}

    def add_space(self, space):
        self.spaces.append(space)

    def add(self, name, data):
        if name in self.artifacts.keys():
            logger.info(f"Add: Name already in use, use update instead of upload")
            return 0

        a = Artifact()

        a.quantity_of_chunks = int(np.ceil(len(data) / self.chunk_length))

        a.chunk_locations = [[] for _ in range(a.quantity_of_chunks)]

        self.artifacts[name] = a

        for i in range(int(np.ceil(len(data) / self.chunk_length))):
            chunk = data[i * self.chunk_length : (i + 1) * self.chunk_length]

            for _ in range(self.replication_factor):
                space_no = self.set_chunk(name, i, chunk)
                logger.info(f"Add: Zapisuje: {name + str(i)} do DataSpace: {space_no}")

        return 1

    def update(self, name, data):
        if name not in self.artifacts.keys():
            logger.info(f"Update: Name not in use, use upload instead of update")
            return 0

        a = self.artifacts[name]

        for i in range(int(np.ceil(len(data) / self.chunk_length))):

            f = False

            if i >= a.quantity_of_chunks:
                chunk = data[i * self.chunk_length: (i + 1) * self.chunk_length]

                a.quantity_of_chunks += 1
                a.chunk_locations.append([])

                for _ in range(self.replication_factor):
                    space_no = self.set_chunk(name, i, chunk)
                    logger.info(f"Update: Dopisuje: {name + str(i)} do DataSpace: {space_no}")

                f = True

            if f:
                continue

            chunk = data[i * self.chunk_length : (i + 1) * self.chunk_length]

            if chunk != self.get_chunk(name, i):
                logger.info(f"Update: Nadpisuje: {name+str(i)} do DataSpace: {i}")
                for location in a.chunk_locations[i]:
                    self.spaces[location].update.remote(name+str(i), chunk)

        for i in range(int(np.ceil(len(data) / self.chunk_length)) + 1, a.quantity_of_chunks):
            logger.info(f"Update: Usuwam wszystkie kopie nieistniejącego już chunka: {name+str(i)}")
            for location in a.chunk_locations[i]:
                self.spaces[location].remove.remote(name+str(i))

        a.quantity_of_chunks = int(np.ceil(len(data) / self.chunk_length))
        a.chunk_locations = a.chunk_locations[:a.quantity_of_chunks]

    def get_chunk(self, name, chunk_no):
        a = self.artifacts[name]
        for location in a.chunk_locations[chunk_no]:
            try:
                return ray.get(self.spaces[location].get.remote(name + str(chunk_no)))
            except ray.exceptions.RayActorError:
                logger.info(f"GetChunk: Nie udało się odebrać chunka z DataSpace: {location}")
        return 0

    def get(self, name):
        a = self.artifacts[name]

        result = ""

        for i in range(a.quantity_of_chunks):
            f = False
            e = False
            for location in a.chunk_locations[i]:
                try:
                    done, pending = ray.wait([self.spaces[location].get.remote(name + str(i))], timeout=1)
                    if done:
                        result += ray.get(done[0])
                        if result == 0:
                            e = True
                            break
                        logger.info(f"Get: Odbieram: {name+str(i)}z DataSpace: {location}")
                        f = True
                        break
                    logger.info(f"Get: Nie udało się odebrać chunka z DataSpace: {location}")
                except ray.exceptions.RayActorError:
                    logger.info(f"Get: DataSpace {location} nie żyje. Spróbuje z innego źródła")

            if f:
                continue

            if e:
                logger.warning(f"Get: Nie udało się odczytać chunka.")
                break

        return result

    def check_status(self):
        broken = set()
        for i in range(len(self.spaces)):
            try:
                ray.get(self.spaces[i].check_status.remote())
            except ray.exceptions.RayActorError:
                broken.add(i)
                logger.info(f"Check: DataSpace: {i} nie żyje.")
        if len(broken) > 0:
            for b in broken:
                self.spaces_blackset.add(b)
            return 0
        return 1

    def set_chunk(self, name, i, chunk):
        a = self.artifacts[name]
        space_no = random.choice([j for j in range(len(self.spaces)) if j not in self.spaces_blackset and j not in a.chunk_locations[i]])
        a.chunk_locations[i].append(space_no)
        self.spaces[space_no].add.remote(name+str(i), chunk)
        return space_no

    def heal(self):
        result = self.check_status()
        if result != 1:
            for name in self.artifacts.keys():
                a = self.artifacts[name]
                for i in range(a.quantity_of_chunks):
                    for location in a.chunk_locations[i]:
                        if location in self.spaces_blackset:
                            a.chunk_locations[i].remove(location)
                            chunk = self.get_chunk(name, i)
                            space_no = self.set_chunk(name, i, chunk)
                            logger.info(f"Heal: Artefakt o nazwie: {name} miał chunk w space z blacksetu. Wstawiłem nową kopie chunka: {name+str(i)} do DataSpace: {space_no}")

    def list_artifacts(self):
        for name in self.artifacts.keys():
            a = self.artifacts[name]
            a.list()

    def list_spaces(self):
        for i in range(len(self.spaces)):
            if i not in self.spaces_blackset:
                ray.get(self.spaces[i].list.remote())

    def kill(self, i):
        ray.kill(self.spaces[i])