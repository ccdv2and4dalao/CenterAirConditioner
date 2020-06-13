from abc import abstractmethod

class BaseSubConsole:
    @abstractmethod
    def register(self, prefix: str):
        pass