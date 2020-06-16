from typing import Union

import lib
from abstract.component import Logger
from abstract.model import EventModel, EventType, StatisticModel
from abstract.service.admin.get_slave_statistics import AdminGetSlaveStatisticsService
from app.service.generate_statistics import GenerateStatisticServiceImpl
from lib.dateutil import now
from proto import DatabaseError, FailedResponse
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsResponse, AdminGetSlaveStatisticsRequest


class AdminGetSlaveStatisticsServiceImplV2(GenerateStatisticServiceImpl, AdminGetSlaveStatisticsService):
    def __init__(self, inj):
        super().__init__(inj)
        self.response_factory = AdminGetSlaveStatisticsResponse
        self.event_model = inj.require(EventModel)  # type: EventModel
        self.statistic_model = inj.require(StatisticModel)  # type: StatisticModel
        self.logger = inj.require(Logger)  # type: Logger

    def serve(self, req: AdminGetSlaveStatisticsRequest) -> Union[AdminGetSlaveStatisticsResponse, FailedResponse]:
        events = self.event_model.query_control_events_by_time_interval(
            req.room_id,
            lib.dateutil.to_local(req.start_time), lib.dateutil.to_local(req.stop_time))
        if events is None:
            return DatabaseError(f'DatabaseError: {self.event_model.why()}')

        data = []
        for i, event in enumerate(events):
            if event.event_type == EventType.StopControl:
                right = event
                if i == 0 or events[i - 1].event_type != EventType.StartControl:
                    self.logger.warn('stop event type not matching start event', args={'event_id': event.id})
                    continue
                left = events[i - 1]

                energy, cost = self.statistic_model.query_sum_by_time_interval(
                    req.room_id, left.checkpoint, right.checkpoint)
                data.append({
                    'room_id': req.room_id,
                    'start_time': lib.dateutil.str_to_rfc3339(left.checkpoint),
                    'stop_time': lib.dateutil.str_to_rfc3339(right.checkpoint),
                    'fan_speed': left.str_arg,
                    'energy': float(energy),
                    'cost': float(cost)
                })
        ret = AdminGetSlaveStatisticsResponse()
        ret.data = data
        return ret
