
from abc import abstractmethod


class Logger(object):

    @abstractmethod
    def info(self, msg: str, args: dict):
        """
        :param msg: 提示字符串，用于阅读
        :param args: 其他参数
        以INFO level记录日志
        """
        pass

    @abstractmethod
    def warn(self, msg: str, args: dict):
        """
        :param msg: 提示字符串，用于阅读
        :param args: 其他参数
        以WARN level记录日志
        """
        pass

    @abstractmethod
    def debug(self, msg: str, args: dict):
        """
        :param msg: 提示字符串，用于阅读
        :param args: 其他参数
        以DEBUG level记录日志
        """
        pass

    @abstractmethod
    def error(self, msg: str, args: dict):
        """
        :param msg: 提示字符串，用于阅读
        :param args: 其他参数
        以ERROR level记录日志
        """
        pass

    @abstractmethod
    def fatal(self, msg: str, args: dict):
        """
        :param msg: 提示字符串，用于阅读
        :param args: 其他参数
        该函数调用后会直接终止程序
        以FATAL level记录日志
        """
        pass
