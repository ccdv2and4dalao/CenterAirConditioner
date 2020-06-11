from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.generate_statistics import GenerateStatisticRequest, GenerateStatisticResponse

# 11.中央空调实时计算每个房间所消耗的能量以及所需支付的金额，并将对应信息发送给每个从控机进行在线显示，以便客户可以实时查看用量和金额。

class GenerateStatisticService(Service, ABC):

    @abstractmethod
    def serve(self, req: GenerateStatisticRequest) -> GenerateStatisticResponse or FailedResponse:
        pass
