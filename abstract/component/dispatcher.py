from abc import abstractmethod, ABC

from abstract.component.bootable import Bootable

# 3.中央空调具备开关按钮，只可人工开启和关闭，中央空调正常开启后处于待机状态。
#     c)当有来自从控机的温控要求时，中央空调开始工作；
#     d)当所有房间都没有温控要求时，中央空调的状态回到待机状态。
# 13.中央空调只能同时处理三台从控机的请求，为此主机要有负载均衡的能力。如果有超过三台从控机请求，则需要对所有请求机器进行调度，调度算法可自行定义，如先来先到、高速风优先抢占、时间片轮询等。

class Dispatcher(Bootable, ABC):

    @abstractmethod
    def is_idle(self) -> bool:
        pass

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
