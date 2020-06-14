from abc import abstractmethod, ABC
from typing import Union

from abstract.service import Service
from proto.admin.set_metric_delay import AdminSetMetricDelayRequest, AdminSetMetricDelayResponse
from proto import FailedResponse

class AdminSetMetricDelayService(Service, ABC):
    @abstractmethod
    def serve(self, req: AdminSetMetricDelayRequest) -> Union[AdminSetMetricDelayResponse, FailedResponse]:
        pass