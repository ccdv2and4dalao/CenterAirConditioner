from abstract.middleware import PaymentMiddleware
from proto.metrics import MetricsRequest
from proto.generate_statistics import GenerateStatisticRequest
from proto.stop_state_control import StopStateControlRequest

class PaymentMiddlewareImpl(PaymentMiddleware):
    def __init__(self):
        self.metric = {}
        self.statistic = {}

    def update_room_metric(self, req: MetricsRequest):
        r_id = req.room_id
        if r_id not in self.metric:
            pass


    def get_room_statistic(self, req: GenerateStatisticRequest):
        pass

    def save_room_statistic(self, req: StopStateControlRequest):
        pass