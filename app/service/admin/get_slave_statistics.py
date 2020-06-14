import datetime

from dateutil.parser import parse

from abstract.model import EventModel, EventType, Event, StatisticModel
from abstract.service.admin.get_slave_statistics import AdminGetSlaveStatisticsService
from app.service.generate_statistics import GenerateStatisticServiceImpl
from lib.dateutil import now
from proto.admin.get_slave_statistics import AdminGetSlaveStatisticsResponse, AdminGetSlaveStatisticsRequest
from proto import MasterAirCondNotAlive
from abstract.component import MasterAirCond

class AdminGetSlaveStatisticsServiceImpl(GenerateStatisticServiceImpl, AdminGetSlaveStatisticsService):
    def __init__(self, inj):
        self.response_factory = AdminGetSlaveStatisticsResponse
        self.event_model = inj.require(EventModel)  # type: EventModel
        self.statistic_model = inj.require(StatisticModel)  # type: StatisticModel
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: AdminGetSlaveStatisticsRequest):
        if not self.master_air_cond.is_boot:
            return MasterAirCondNotAlive("master aircon is off")
        events = self.event_model.query_by_time_interval(None, datetime.datetime(2000, 1, 1), now())
        data = []
        i = 0
        room_events = {}
        for event in events:
            rid = event.room_id
            if rid not in room_events.keys():
                room_events[rid] = []
            room_events[rid].append(event)
        for rid, lists in room_events.items():
            i = 0
            while i < len(lists):
                while i < len(lists) and lists[i].event_type != EventType.StartControl: i += 1
                if i >= len(lists): break
                l = lists[i]
                if i + 1 < len(lists):
                    r = lists[i + 1]
                    if r.event_type != EventType.StopControl:
                        print('event type mismatch: missing stop control')
                else:
                    r = Event()
                    r.checkpoint = now()
                energy, cost = self.statistic_model.query_sum_by_time_interval(rid, l.checkpoint, r.checkpoint)
                data.append({'room_id': rid, 'start_time': l.checkpoint, 'stop_time': r.checkpoint,
                             'fan_speed': l.str_arg, 'energy': energy, 'cost': cost})
                i += 2
        data.sort(key=lambda x: x['start_time'])
        for d in data:
            d['start_time'] = parse(d['start_time']).strftime("%Y-%m-%dT%H:%M:%SZ")
            d['stop_time'] = parse(d['stop_time']).strftime("%Y-%m-%dT%H:%M:%SZ")
            d['energy'] = float(d['energy'])
            d['cost'] = float(d['cost'])
        ret = AdminGetSlaveStatisticsResponse()
        ret.data = data
        return ret
