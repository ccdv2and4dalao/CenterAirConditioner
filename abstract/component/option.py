
from abc import abstractmethod


class OptionProvider(object):

    @abstractmethod
    def find(self, key: str) -> str:
        """
        :param key: 对应Option的long opt值
        :return: 对应Option的值，如果不存在，如果已经设置了default值，则返回default值，都不存在值则返回None
        """
        pass
