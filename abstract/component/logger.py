
from abc import abstractmethod


class Logger(object):

    @abstractmethod
    def info(self, msg: str, args: dict):
        pass

    @abstractmethod
    def warn(self, msg: str, args: dict):
        pass

    @abstractmethod
    def debug(self, msg: str, args: dict):
        pass

    @abstractmethod
    def error(self, msg: str, args: dict):
        pass

    @abstractmethod
    def fatal(self, msg: str, args: dict):
        pass
