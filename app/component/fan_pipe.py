from abstract.component import ConnectionPool, Logger
from abstract.component.fan_pipe import MasterFanPipe
from abstract.component.websocket_conn import WebsocketConn
from abstract.consensus import FanSpeed, AirMode


class MasterFanPipeImpl(MasterFanPipe):
    def __init__(self, inj):
        self.socket_conn = inj.require(WebsocketConn)  # type: WebsocketConn
        self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
        self.logger = inj.require(Logger)  # type: Logger

    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode):
        """
        开始送风，什么模式
        由MasterAirCond调用，不是由从控调用，向从控送风
        """
        if type(speed) is FanSpeed: speed = speed.value
        if type(mode) is AirMode: mode = mode.value

        self.logger.info('start_supply', args={'room_id': room_id, 'speed': speed, 'mode': mode})
        return self.socket_conn.put_event(room_id, 'start_supply', (speed, mode, room_id))

    def supply_once(self, room_id: int, duration: int):
        """
        送一次风，送了多久（毫秒）
        由MasterAirCond调用，不是由从控调用，向从控送风
        """
        self.logger.info('supply_once', args={'room_id': room_id, 'duration': duration})
        return self.socket_conn.put_event(room_id, 'supply_once', (duration, room_id))

    def stop_supply(self, room_id: int):
        """
        停止送风
        由MasterAirCond调用，不是由从控调用，向从控送风
        """
        self.logger.info('stop_supply', args={'room_id': room_id})
        return self.socket_conn.put_event(room_id, 'stop_supply', (room_id,))
