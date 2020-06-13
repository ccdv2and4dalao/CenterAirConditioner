from abc import abstractmethod


class StatusConsole:
    @abstractmethod
    def __call__(self, *args):
        pass
