import time
from threading import local

from abstract.component import Logger, Dispatcher, UUIDGenerator, MasterAirCond
from abstract.component.connection_pool import ConnectionPool
from abstract.model import EventModel, StatisticModel
from lib.injector import Injector


class BasicStateControlServiceImpl(object):
    def __init__(self, inj: Injector):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond
        self.uuid_provider = inj.require(UUIDGenerator)  # type: UUIDGenerator
        self.dispatcher = inj.require(Dispatcher)  # type: Dispatcher
        self.event_model = inj.require(EventModel)  # type: EventModel
        self.dispatcher.on_pop(self._pop_request)
        self.dispatcher.on_fallback(self._fallback_request)
        self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
        self.logger = inj.require(Logger)  # type: Logger
        self.statistic_model = inj.require(StatisticModel) # type: StatisticModel
        self.base_time = time.perf_counter()

    def push_start_request(self, room_id, speed_fan, mode, tag):
        return self.dispatcher.push(
            {'room_id': room_id, 'need_fan': True, 'speed_fan': speed_fan, 'mode': mode}, tag)

    def push_stop_request(self, room_id, tag: str) -> bool:
        return self.dispatcher.push(
            {'room_id': room_id, 'need_fan': False}, tag)

    def generate_tag(self) -> str:
        return self.uuid_provider.generate_uuid()

    def _pop_request(self, req: dict, tag: str) -> None:
        b = local()
        b.room_id, b.mode = req['room_id'], req['mode']
        b.speed = self.connection_pool.get().fan_speed
        b.co = 5 if b.speed.value == 'high' else 4 if b.speed.value == 'mid' else 3

        self.master_air_cond.start_supply(b.room_id, b.speed, b.mode)
        self.event_model.insert_start_state_control_event(b.room_id, b.speed)
        
        b.t1 = time.perf_counter()
        try:
            while self.connection_pool.get(b.room_id).need_fan:
                time.sleep(2.0)
                b.new_speed = self.connection_pool.get().fan_speed
                if  b.new_speed != b.speed:
                    b.speed = b.new_speed
                    # stop old speed
                    self.master_air_cond.stop_supply(b.room_id)
                    self.event_model.insert_stop_state_control_event(b.room_id)
                    # start new speed
                    b.co = 5 if b.speed.value == 'high' else 4 if b.speed.value == 'mid' else 3
                    self.master_air_cond.start_supply(b.room_id, b.speed, b.mode)
                    self.event_model.insert_start_state_control_event(b.room_id, b.speed)

                b.t2 = time.perf_counter()
                self.statistic_model.insert(b.room_id, (b.t2 - b.t1) * b.co / 5,
                                            (b.t2 - b.t1) * b.co)
                b.t1 = b.t2
        except Exception as e:
            pass

        self.master_air_cond.stop_supply(b.room_id)
        self.event_model.insert_stop_state_control_event(b.room_id)

    def _fallback_request(self, req: dict, tag: str) -> None:
        req['tag'] = tag
        self.logger.warn('abort request', req)

    def _update_statistics(self, opaque: dict, tag: str) -> None:
        raise DeprecationWarning('_update_statistics function hasnt been used')
        pass