from abc import abstractmethod
from typing import List


class SQLDatabase(object):
    @abstractmethod
    def select(self, sql: str) -> List[tuple]:
        pass


class KVDatabase(object):
    @abstractmethod
    def get(self, k: str) -> object:
        pass


