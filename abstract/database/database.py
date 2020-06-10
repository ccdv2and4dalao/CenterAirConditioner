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
    def connect(self, host='', port=0, user='', password='', database=''):
        pass

    @abstractmethod
    def select(self, sql: str, *args) -> List[tuple]:
        pass

    @abstractmethod
    def insert(self, sql: str, *args) -> int:
        pass

    @abstractmethod
    def create(self, sql: str, *args) -> bool:
        pass

    @abstractmethod
    def delete(self, sql: str, *args) -> bool:
        pass

    @abstractmethod
    def update(self, sql: str, *args) -> bool:
        pass

    @abstractmethod
    def get_last_error(self) -> Exception:
        pass



class KVDatabase(object):
    @abstractmethod
    def get(self, k: str) -> object:
        pass

    @abstractmethod
    def set(self, k: str) -> bool:
        pass


