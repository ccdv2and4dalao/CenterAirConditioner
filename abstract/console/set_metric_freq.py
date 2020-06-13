from abc import abstractmethod
from .base_subconsole import BaseSubConsole


class SetMetricFrequencyConsole:
    @abstractmethod
    def __call__(self, *args):
        pass