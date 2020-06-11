from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.start_state_control import StartStateControlRequest, StartStateControlResponse
from proto.stop_state_control import StopStateControlRequest, StopStateControlResponse

# 2.中央空调是冷暖两用，根据季节进行工作模式调整。
#    a)当设置为供暖时，供暖温度控制在25°C～30°C之间；
#    b)当设置为制冷时，制冷温度控制在18°C～25°C之间。

# 3.中央空调具备开关按钮，只可人工开启和关闭，中央空调正常开启后处于待机状态。
#     a)中央空调开机后，默认处于制冷模式，缺省工作温度为22°C，当切换到供暖模式时，缺省工作温度为28°C；

# 4.房间内有独立的从控空调机，但没有冷暖控制设备。
#     b)如果从控机发出的请求和中央空调设置的冷暖控制状态发生矛盾时，以中央空调机的状态优先，否则中央空调机不予响应。

class StartStateControlService(Service, ABC):

    @abstractmethod
    def serve(self, req: StartStateControlRequest) -> StartStateControlResponse or FailedResponse:
        pass


class StopStateControlService(Service, ABC):

    @abstractmethod
    def serve(self, req: StopStateControlRequest) -> StopStateControlResponse or FailedResponse:
        pass
