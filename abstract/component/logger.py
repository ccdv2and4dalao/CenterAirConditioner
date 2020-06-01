
from abc import abstractmethod


class Logger(object):

    @abstractmethod
    def info(self, msg: str):
        pass

    @abstractmethod
    def warn(self, msg: str):
        pass

    @abstractmethod
    def debug(self, msg: str):
        pass

    @abstractmethod
    def error(self, msg: str):
        pass

    @abstractmethod
    def fatal(self, msg: str):
        pass

