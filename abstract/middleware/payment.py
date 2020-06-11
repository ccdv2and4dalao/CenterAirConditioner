from abc import ABC, abstractmethod

from abstract.middleware.abstract import Middleware


# 10.系统中央空调部分具备计费功能：可根据中央空调对从控机的请求时长及高中低风速的供风量进行费用计算；
# a)每分钟中速风的能量消耗为一个标准功率单位；
# b)低速风的每分钟功率消耗为0.8标准功率；
# c)高速风的每分钟功率消耗为1.2标准功率；
# d)并假设，每一个标准功率消耗的计费标准是5元。
# 11.中央空调实时计算每个房间所消耗的能量以及所需支付的金额，并将对应信息发送给每个从控机进行在线显示，以便客户可以实时查看用量和金额。

class PaymentMiddleware(Middleware, ABC):
    """
    鉴权中间件
    """
    pass

    @abstractmethod
    def __init__(self):
        pass
