from abc import abstractmethod


class ReportConsole:
    @abstractmethod
    def __call__(self, *args):
        pass
