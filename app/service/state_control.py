from abstract.component import Logger, Dispatcher, UUIDGenerator, MasterAirCond
from abstract.component.connection_pool import ConnectionPool
from lib.injector import Injector


class BasicStateControlServiceImpl(object):
    def __init__(self, inj: Injector):
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond
        self.uuid_provider = inj.require(UUIDGenerator)  # type: UUIDGenerator
        self.dispatcher = inj.require(Dispatcher)  # type: Dispatcher
        self.dispatcher.on_pop(self._pop_request)
        self.dispatcher.on_fallback(self._fallback_request)
        self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
        self.logger = inj.require(Logger)  # type: Logger

    def push_start_request(self, room_id, speed_fan, mode, tag):
        return self.dispatcher.push(
            {'room_id': room_id, 'need_fan': True, 'speed_fan': speed_fan, 'mode': mode}, tag)

    def push_stop_request(self, room_id, tag: str) -> bool:
        return self.dispatcher.push(
            {'room_id': room_id, 'need_fan': False}, tag)

    def generate_tag(self) -> str:
        return self.uuid_provider.generate_uuid()

    def _pop_request(self, req: dict, tag: str) -> None:
        room_info = req['need_fan'] and self.connection_pool.get(req['room_id'])
        if not room_info or not room_info.need_fan:
            # fast forward
            resp = self.master_air_cond.stop_supply(req['room_id'])
        else:
            resp = self.master_air_cond.start_supply(req['room_id'], req['speed_fan'], req['mode'])
        if not resp:
            d = resp.__dict__
            d['tag'] = tag
            self.logger.warn('failed supply', d)
            # self._update_statistics(failed response, tag)
        else:
            self._update_statistics(req, tag)

    def _fallback_request(self, req: dict, tag: str) -> None:
        req['tag'] = tag
        self.logger.warn('abort request', req)

    def _update_statistics(self, opaque: dict, tag: str) -> None:
        pass
