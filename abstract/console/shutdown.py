from abc import abstractmethod


class ShutdownConsole:
    @abstractmethod
    def __call__(self, *args):
        pass
