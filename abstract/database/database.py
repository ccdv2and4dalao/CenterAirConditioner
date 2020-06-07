from abc import abstractmethod
from typing import List


class SQLDatabase(object):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def _select(self, sql: str) -> List[tuple]:
        pass

    @abstractmethod
    def _insert(self, sql: str) -> bool:
        pass

    @abstractmethod
    def _create(self, sql: str) -> bool:
        pass

    @abstractmethod
    def _delete(self, sql: str) -> bool:
        pass

    @abstractmethod
    def _update(self, sql: str) -> bool:
        pass

    



class KVDatabase(object):
    @abstractmethod
    def get(self, k: str) -> object:
        pass

    @abstractmethod
    def set(self, k: str) -> bool:
        pass


