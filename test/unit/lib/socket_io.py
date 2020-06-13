# import asyncio
#
# # from aiohttp import web
# # import socketio
# # import aiohttp_cors
# from abc import abstractmethod
#
# from flask import Flask
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from flask_socketio import send, emit
# from flask import request, session
# from datetime import timedelta, datetime
# from threading import Lock
# import time
# import threading
#
# # sio = socketio.AsyncServer(cors_allowed_origins='http://localhost:9000')
# from abstract.component import ConnectionPool
# from abstract.consensus import FanSpeed, AirMode
# from app.component.fan_pipe import MasterFanPipe
# from lib.injector import Injector
# from lib.memory_connection_pool import MemoryConnectionPoolImpl
#
# app = Flask(__name__)
# CORS(app)
#
#
# # cors = aiohttp_cors.setup(app, defaults={
# #     # Allow all to read all CORS-enabled resources from
# #     # http://client.example.org.
# #     "http://localhost:9000": aiohttp_cors.ResourceOptions(
# #         allow_credentials=True,
# #         expose_headers="*",
# #         allow_headers="*",
# #     ),
# #     "http://127.0.0.1:9000": aiohttp_cors.ResourceOptions(
# #         allow_credentials=True,
# #         expose_headers="*",
# #         allow_headers="*",
# #     ),
# # })
#
# # sio.attach(app)
#
#
# # class BackgroundTask(object):
# #     def __init__(self):
# #         self.task = dict()
# #         self.mutex = Lock()
# #
# #     def put(self, sid):
# #         self.task[sid] = 0
# #         threading.Thread(target=self._work, args=(sid,)).start()
# #
# #     def _work(self, sid):
# #         self.work(sid)
# #
# #     def lock(self):
# #         self.mutex.release()
# #
# #     def work(self, sid):
# #         while True:
# #             if self.task[sid] == 3:
# #                 self.task.pop(sid)
# #                 socketio.emit('state_control_stopped')
# #                 return
# #             socketio.emit('fan_request', {'fan_speed': 'high', 'duration': 1000})
# #             time.sleep(1)
# #             print(datetime.now())
# #             self.task[sid] += 1
#
#
# # tm = BackgroundTask()
#
#
# pipe = None
#
#
# MilliSecond = int
#
# def xxx(connection_pool):
#     print(connection_pool)
#     while True:
#         x = connection_pool.get(1)
#         print(x)
#         if x.session_id == '':
#             time.sleep(3)
#             continue
#         pipe.start_supply(1, FanSpeed.High, AirMode.Cool)
#         print(datetime.now(), 'pipe.start_supply(1, FanSpeed.High, AirMode.Cool)')
#         time.sleep(1)
#         print(datetime.now(), 'time.sleep(1)')
#         pipe.supply_once(1, 500)
#         print(datetime.now(), 'pipe.supply_once(1, 500)')
#         time.sleep(1)
#         print(datetime.now(), 'time.sleep(1)')
#         pipe.supply_once(1, 500)
#         print(datetime.now(), 'pipe.supply_once(1, 500)')
#         time.sleep(1)
#         print(datetime.now(), 'time.sleep(1)')
#         pipe.supply_once(1, 500)
#         print(datetime.now(), 'pipe.supply_once(1, 500)')
#         pipe.stop_supply(1)
#         print(datetime.now(), 'pipe.stop_supply(1)')
#         time.sleep(5)
#
#
# if __name__ == '__main__':
#     # inj = Injector()
#     # inj.build(ConnectionPool, MemoryConnectionPoolImpl)
#     # conn_pool = inj.require(ConnectionPool)  # type: ConnectionPool
#     # conn_pool.put(1, 1, False)
#
#     # socket_io_conn = functional_socket_io_connection_impl(inj)
#     # inj.provide(WebsocketConn, socket_io_conn)
#     # # web.run_app(app, port=9002)
#     # pipe = MasterFanPipeImpl(inj)
#     #
#     # threading.Thread(target=xxx, args=(conn_pool, ), daemon=True).start()
#     #
#     # socket_io_conn.sio.run(app, port=9002, debug=True)
