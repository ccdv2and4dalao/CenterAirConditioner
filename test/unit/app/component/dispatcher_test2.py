import unittest

from app.server_builder import ServerBuilder
from abstract.service import StartStateControlService, StopStateControlService
from abstract.component.dispatcher import Dispatcher
from abstract.component import ConnectionPool
from lib.memory_connection_pool import SafeMemoryConnectionPoolImpl
from abstract.consensus.fan_speed import FanSpeed
from abstract.consensus.air_mode import AirMode
from abstract.component.websocket_conn import WebsocketConn
from time import sleep

class FakePipe(SafeMemoryConnectionPoolImpl, WebsocketConn):
    def put_event(self, room_id, event_name, data):
        print(f'room: {room_id} do: {event_name}  data: {data}')


class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.sb = ServerBuilder()
        fp = FakePipe()
        # 注释掉severbuilder里的对应两行
        self.sb.injector.provide(ConnectionPool, fp)
        self.sb.injector.provide(WebsocketConn, fp)
        self.sb.build_base()
        self.sb.build_model()
        self.sb.build_middleware()
        self.sb.build_service()
        self.sb.build_controller(self.sb.injector)
        self.dispatcher = self.sb.injector.require(Dispatcher)
        self.dispatcher.boot_up()

    def addEvent(self):
        start = self.sb.injector.require(StartStateControlService)
        stop = self.sb.injector.require(StopStateControlService)
        cp = self.sb.injector.require(ConnectionPool)
        cp.put(8, 6, False)
        cp.put_fan_speed(8, 'low')
        cp.put(7, 5, False)
        cp.put_fan_speed(7, 'low')
        cp.put(6, 4, False)
        cp.put_fan_speed(6, 'low')
        cp.put(5, 3, False)
        cp.put_fan_speed(5, 'high')

        start.start_supply(8, FanSpeed.Low, AirMode.Cool)
        start.start_supply(7, FanSpeed.Low, AirMode.Cool)
        start.start_supply(6, FanSpeed.Low, AirMode.Cool)
        start.start_supply(5, FanSpeed.High, AirMode.Cool)
        sleep(5)
        stop.stop_supply(8)
        sleep(5)
        stop.stop_supply(7)
        sleep(5)
        stop.stop_supply(6)
        sleep(5)
        stop.stop_supply(5)
        print('fin')


if __name__ == '__main__':
    d = DispatcherTest()
    d.setUp()
    d.addEvent()
    while True:
        pass