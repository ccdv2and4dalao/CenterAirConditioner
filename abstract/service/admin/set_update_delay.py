from abc import abstractmethod, ABC
from typing import Union

from abstract.service import Service
from proto.admin.set_update_delay import AdminSetUpdateDelayRequest, AdminSetUpdateDelayResponse
from proto import FailedResponse

class AdminSetUpdateDelayService(Service, ABC):
    @abstractmethod
    def serve(self, req: AdminSetUpdateDelayRequest) -> Union[AdminSetUpdateDelayResponse, FailedResponse]:
        pass