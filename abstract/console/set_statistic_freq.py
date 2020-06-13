from abc import abstractmethod
from .base_subconsole import BaseSubConsole


class SetStatisticFrequencyConsole:
    @abstractmethod
    def __call__(self):
        pass