from abstract.service import GenerateStatisticService
from abc import abstractmethod, ABC
from proto.generate_statistics import GenerateStatisticRequest, GenerateStatisticResponse


class BaseGenerateStatisticServiceImpl(GenerateStatisticService):
    @abstractmethod
    def get_metrics(self, room_id):
        pass


class GenerateStatisticServiceImpl(BaseGenerateStatisticServiceImpl):
    def __init__(self):
        pass

    def serve(self, req):
        pass

    def get_metrics(self, room_id):
        pass