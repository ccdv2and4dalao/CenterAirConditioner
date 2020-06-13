import asyncio

# from aiohttp import web
# import socketio
# import aiohttp_cors
from abc import abstractmethod

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_socketio import send, emit
from flask import request, session
from datetime import timedelta, datetime
from threading import Lock
import time
import threading

# sio = socketio.AsyncServer(cors_allowed_origins='http://localhost:9000')
from abstract.component import ConnectionPool
from abstract.consensus import FanSpeed, AirMode
from app.component.fan_pipe import MasterFanPipe
from lib.injector import Injector
from lib.memory_connection_pool import MemoryConnectionPoolImpl

app = Flask(__name__)
CORS(app)


# cors = aiohttp_cors.setup(app, defaults={
#     # Allow all to read all CORS-enabled resources from
#     # http://client.example.org.
#     "http://localhost:9000": aiohttp_cors.ResourceOptions(
#         allow_credentials=True,
#         expose_headers="*",
#         allow_headers="*",
#     ),
#     "http://127.0.0.1:9000": aiohttp_cors.ResourceOptions(
#         allow_credentials=True,
#         expose_headers="*",
#         allow_headers="*",
#     ),
# })

# sio.attach(app)


# class BackgroundTask(object):
#     def __init__(self):
#         self.task = dict()
#         self.mutex = Lock()
#
#     def put(self, sid):
#         self.task[sid] = 0
#         threading.Thread(target=self._work, args=(sid,)).start()
#
#     def _work(self, sid):
#         self.work(sid)
#
#     def lock(self):
#         self.mutex.release()
#
#     def work(self, sid):
#         while True:
#             if self.task[sid] == 3:
#                 self.task.pop(sid)
#                 socketio.emit('state_control_stopped')
#                 return
#             socketio.emit('fan_request', {'fan_speed': 'high', 'duration': 1000})
#             time.sleep(1)
#             print(datetime.now())
#             self.task[sid] += 1


# tm = BackgroundTask()

class SocketIOConnection(object):

    @abstractmethod
    def put_event(self, room_id, event_name, data):
        pass


pipe = None


def functional_socket_io_connection_impl(inj):
    sio = SocketIO(app, cors_allowed_origins='*')

    class FunctionalSocketIOConnectionImpl(SocketIOConnection):
        def __init__(self):
            self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
            self.sio = sio
            self.session_id_rev_mapping = dict()

            @sio.on('connect')
            def connect():
                room_id = int(request.args['room_id'])
                self.connection_pool.put_session_id(room_id, request.sid)
                self.session_id_rev_mapping[request.sid] = room_id

                pipe.start_supply(room_id, FanSpeed.High, AirMode.Cool)
                print('start_supply', datetime.now())
                time.sleep(0.5)
                pipe.supply_once(room_id, 500)
                time.sleep(0.5)
                pipe.supply_once(room_id, 500)
                # print('supply_once', datetime.now())
                # time.sleep(2.5)
                # pipe.stop_supply(room_id)
                # print('stop_supply', datetime.now())

            @sio.on('disconnect')
            def disconnect():
                self.connection_pool.close_session_connection(self.session_id_rev_mapping[request.sid])

        def put_event(self, room_id, event_name, data):
            room_info = self.connection_pool.get(room_id)
            if room_info is None:
                return None

            sio.emit(event_name, data, room=room_info.session_id)

    return FunctionalSocketIOConnectionImpl()


MilliSecond = int


class MasterFanPipeImpl(MasterFanPipe):
    def __init__(self, inj):
        self.socket_conn = inj.require(SocketIOConnection)  # type: SocketIOConnection
        self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool

    def start_supply(self, room_id: int, speed: FanSpeed, mode: AirMode):
        """
        开始送风，什么模式
        由MasterAirCond调用，不是由从控调用，向从控送风
        """
        return self.socket_conn.put_event(room_id, 'start_supply', (speed.value, mode.value))

    def supply_once(self, room_id: int, duration: MilliSecond):
        """
        送一次风，送了多久（毫秒）
        由MasterAirCond调用，不是由从控调用，向从控送风
        """
        return self.socket_conn.put_event(room_id, 'supply_once', (duration,))

    def stop_supply(self, room_id: int):
        """
        停止送风
        由MasterAirCond调用，不是由从控调用，向从控送风
        """
        return self.socket_conn.put_event(room_id, 'stop_supply', None)


if __name__ == '__main__':
    inj = Injector()
    inj.build(ConnectionPool, MemoryConnectionPoolImpl)
    conn_pool = inj.require(ConnectionPool)  # type: ConnectionPool
    conn_pool.put(1, 1, False)

    socket_io_conn = functional_socket_io_connection_impl(inj)
    inj.provide(SocketIOConnection, socket_io_conn)
    # web.run_app(app, port=9002)
    pipe = MasterFanPipeImpl(inj)

    socket_io_conn.sio.run(app, port=9002, debug=True)
