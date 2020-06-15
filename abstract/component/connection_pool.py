from abc import abstractmethod
from datetime import datetime
from typing import Union


class Connection(object):
    room_id: int
    user_id: int
    current_temperature: float
    need_fan: bool
    session_id: Union[str, None]
    fan_speed: str
    last_heart_beat: datetime


class ConnectionPool(object):

    @abstractmethod
    def put(self, room_id: int, user_id: int, need_fan: bool):
        pass

    @abstractmethod
    def put_need_fan(self, room_id: int, need_fan: bool):
        pass

    @abstractmethod
    def put_session_id(self, room_id: int, session_id: str):
        pass

    @abstractmethod
    def close_session_connection(self, room_id: int):
        pass

    @abstractmethod
    def put_heart_beat(self, room_id: int, put_heart_beat: datetime = None):
        pass

    @abstractmethod
    def delete(self, room_id: int):
        pass

    @abstractmethod
    def get(self, room_id: int) -> Connection:
        pass
