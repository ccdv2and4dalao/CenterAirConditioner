from abc import ABC, abstractmethod

from abstract.service import Service
from proto import FailedResponse
from proto.connection import ConnectionRequest, ConnectionResponse

# 5.从控机只能人工方式开闭，并通过控制面板设置目标温度，目标温度有上下限制。
#     b)从控机开机后需要与中央空调进行连接认证，用户输入房间号+身份证号后，从控机从中央空调获取工作模式和缺省工作温度，并将它们显示在控制面板上；

class ConnectionService(Service, ABC):

    @abstractmethod
    def serve(self, req: ConnectionRequest) -> ConnectionResponse or FailedResponse:
        pass
