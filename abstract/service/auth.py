from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.generate_statistics import GenerateStatisticRequest, GenerateStatisticResponse


class AuthService(Service, ABC):

    @abstractmethod
    def serve(self, req: GenerateStatisticRequest) -> GenerateStatisticResponse or FailedResponse:
        pass
