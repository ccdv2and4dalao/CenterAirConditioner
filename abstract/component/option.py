
from abc import abstractmethod


class OptionProvider(object):

    @abstractmethod
    def find(self, key: str) -> str:
        pass
