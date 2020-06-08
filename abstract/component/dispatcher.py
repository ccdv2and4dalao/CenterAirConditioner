from abc import abstractmethod, ABC

from abstract.component.bootable import Bootable


class Dispatcher(Bootable, ABC):

    @abstractmethod
    def push(self, opaque, tag: str) -> bool:
        """
        :param opaque: 调度器需要保存的数据，目前正在考虑该参数是否是可序列化的（用于持久化）
        :param tag: 用于区分opaque的特征字符串
        :return: 返回是否push成功
        """
        pass

    @abstractmethod
    def on_pop(self, pop_callback=lambda opaque, tag: None):
        """
        :param pop_callback: 回调函数
        该函数原则上只能调用一次，如果调用多次，将raise一个LogicError
        """
        pass

    @abstractmethod
    def on_fallback(self, fallback_callback=lambda opaque, tag: None):
        """
        :param fallback_callback: 回调函数
        该函数原则上只能调用一次，如果调用多次，将raise一个LogicError
        """
        pass
