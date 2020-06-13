from abc import abstractmethod


class SetModeConsole:
    @abstractmethod
    def __call__(self, *args):
        pass
