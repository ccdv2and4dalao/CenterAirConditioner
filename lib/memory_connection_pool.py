import time
from datetime import datetime, timedelta
from threading import Lock
from typing import Dict

from abstract.component.connection_pool import ConnectionPool, Connection
from app.component.bootable import BootableImpl


class ConnectionImpl(Connection):
    def __init__(self, room_id, user_id, current_temperature, need_fan, fan_speed, last_heart_beat):
        self.room_id = room_id
        self.user_id = user_id
        self.current_temperature = current_temperature
        self.need_fan = need_fan
        self.fan_speed = fan_speed
        self.session_id = ''
        self.last_heart_beat = last_heart_beat


class MemoryConnectionPoolImpl(BootableImpl, ConnectionPool):

    def __init__(self, *_):
        self.cache = dict()  # type: Dict[int, Connection]
        super().__init__(self._check_pool, daemonic=True)

    def _check_pool(self):
        while True:
            time.sleep(60)
            self.__check_pool()

    def __check_pool(self):
        check_now = datetime.now()
        d = timedelta(minutes=2)

        to_pop = []
        for k, r in self.cache.items():
            if (r.last_heart_beat - check_now) > d:
                to_pop.append(k)
        for k in to_pop:
            self.cache.pop(k)

    def put(self, room_id: int, user_id: int, need_fan: bool):
        self.cache[room_id] = ConnectionImpl(room_id=room_id, user_id=user_id,
                                             current_temperature=0, need_fan=need_fan, fan_speed='',
                                             last_heart_beat=datetime.now())

    def put_need_fan(self, room_id: int, need_fan: bool):
        self.cache[room_id].need_fan = need_fan

    def put_session_id(self, room_id: int, session_id: str):
        self.cache[room_id].session_id = session_id

    def close_session_connection(self, room_id: int):
        self.cache[room_id].session_id = None

    def put_heart_beat(self, room_id: int, last_heart_beat=datetime.now()):
        self.cache[room_id].last_heart_beat = last_heart_beat

    def delete(self, room_id: int):
        self.cache.pop(room_id)

    def get(self, room_id: int) -> Connection:
        return self.cache.get(room_id)

    def put_fan_speed(self, room_id: int, fan_speed: str):
        self.cache[room_id].fan_speed = fan_speed


class SafeMemoryConnectionPoolImpl(MemoryConnectionPoolImpl):

    def __init__(self, *_):
        super().__init__(*_)
        self.mutex = Lock()

    def __check_pool(self):
        self.mutex.acquire()
        try:
            self.__check_pool()
        finally:
            self.mutex.release()

    def put(self, room_id: int, user_id: int, need_fan: bool):
        self.mutex.acquire()
        try:
            super().put(room_id, user_id, need_fan)
        finally:
            self.mutex.release()

    def put_need_fan(self, room_id: int, need_fan: bool):
        self.mutex.acquire()
        try:
            super().put_need_fan(room_id, need_fan)
        finally:
            self.mutex.release()

    def put_session_id(self, room_id: int, session_id: str):
        self.mutex.acquire()
        try:
            super().put_session_id(room_id, session_id)
        finally:
            self.mutex.release()

    def close_session_connection(self, room_id: int):
        self.mutex.acquire()
        try:
            super().close_session_connection(room_id)
        finally:
            self.mutex.release()

    def put_heart_beat(self, room_id: int, last_heart_beat=datetime.now()):
        self.mutex.acquire()
        try:
            super().put_heart_beat(room_id, last_heart_beat)
        finally:
            self.mutex.release()

    def delete(self, room_id: int):
        self.mutex.acquire()
        try:
            super().delete(room_id)
        finally:
            self.mutex.release()

    def get(self, room_id: int) -> Connection:
        self.mutex.acquire()
        try:
            conn = super().get(room_id)
        finally:
            self.mutex.release()
        return conn

    def put_fan_speed(self, room_id, fan_speed):
        self.mutex.acquire()
        try:
            super().put_fan_speed(room_id, fan_speed)
        finally:
            self.mutex.release()
