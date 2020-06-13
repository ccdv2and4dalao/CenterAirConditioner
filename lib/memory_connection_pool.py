from threading import Lock

from abstract.component.connection_pool import ConnectionPool, Connection


class ConnectionImpl:
    def __init__(self, room_id, user_id, current_temperature, need_fan, fan_speed):
        self.room_id = room_id
        self.user_id = user_id
        self.current_temperature = current_temperature
        self.need_fan = need_fan
        self.fan_speed = fan_speed


class MemoryConnectionPoolImpl(ConnectionPool):

    def __init__(self, *_):
        self.cache = dict()

    def put(self, room_id: int, user_id: int, need_fan: bool):
        self.cache[room_id] = ConnectionImpl(room_id=room_id, user_id=user_id,
                                             current_temperature=0, need_fan=need_fan, fan_speed='')

    def put_need_fan(self, room_id: int, need_fan: bool):
        self.cache[room_id].need_fan = need_fan

    def delete(self, room_id: int):
        self.cache.pop(room_id)

    def get(self, room_id: int) -> Connection:
        return self.cache.get(room_id)


class SafeMemoryConnectionPoolImpl(MemoryConnectionPoolImpl):

    def __init__(self, *_):
        super().__init__(*_)
        self.mutex = Lock()

    def put(self, room_id: int, user_id: int, need_fan: bool):
        self.mutex.acquire()
        super().put(room_id, user_id, need_fan)
        self.mutex.release()

    def put_need_fan(self, room_id: int, need_fan: bool):
        self.mutex.acquire()
        super().put_need_fan(room_id, need_fan)
        self.mutex.release()

    def delete(self, room_id: int):
        self.mutex.acquire()
        super().delete(room_id)
        self.mutex.release()

    def get(self, room_id: int) -> Connection:
        self.mutex.acquire()
        conn = super().get(room_id)
        self.mutex.release()
        return conn
