from abc import abstractmethod

class MetricConsole:
    @abstractmethod
    def __call__(self, *args):
        pass
