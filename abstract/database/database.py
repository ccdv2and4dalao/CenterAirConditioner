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
    def select(self, sql: str) -> List[tuple]:
        pass

    @abstractmethod
    def insert(self, sql: str) -> bool:
        pass

    @abstractmethod
    def create(self, sql: str) -> bool:
        pass

    @abstractmethod
    def delete(self, sql: str) -> bool:
        pass

    @abstractmethod
    def update(self, sql: str) -> bool:
        pass

    



class KVDatabase(object):
    @abstractmethod
    def get(self, k: str) -> object:
        pass

    @abstractmethod
    def set(self, k: str) -> bool:
        pass


