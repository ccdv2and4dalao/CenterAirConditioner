from abc import abstractmethod

class MainConsole:
    @abstractmethod
    def parse(self, cmd: str):
        pass

    @abstractmethod
    def register(self, prefix: str, obj: object):
        pass

    @abstractmethod
    def help(self):
        pass