from threading import Lock

from abstract.component.connection_pool import ConnectionPool, Connection


class ConnectionImpl:
    def __init__(self, room_id, user_id, need_fan):
        self.room_id = room_id
        self.user_id = user_id
        self.need_fan = need_fan


class MemoryConnectionPoolImpl(ConnectionPool):

    def __init__(self, *_):
        self.cache = dict()

    def put(self, token: str, room_id: int, user_id: int, need_fan: bool):
        self.cache[token] = ConnectionImpl(room_id=room_id, user_id=user_id, need_fan=need_fan)

    def put_need_fan(self, token: str, need_fan: bool):
        self.cache[token][2] = need_fan

    def delete(self, token: str):
        self.cache.pop(token)

    def get(self, token: str) -> Connection:
        return self.cache[token]


class SafeMemoryConnectionPoolImpl(MemoryConnectionPoolImpl):

    def __init__(self, *_):
        super().__init__(*_)
        self.mutex = Lock()

    def put(self, token: str, room_id: int, user_id: int, need_fan: bool):
        self.mutex.acquire()
        super().put(token, room_id, user_id, need_fan)
        self.mutex.release()

    def put_need_fan(self, token: str, need_fan: bool):
        self.mutex.acquire()
        super().put_need_fan(token, need_fan)
        self.mutex.release()

    def delete(self, token: str):
        self.mutex.acquire()
        super().delete(token)
        self.mutex.release()

    def get(self, token: str) -> Connection:
        self.mutex.acquire()
        conn = super().get(token)
        self.mutex.release()
        return conn
