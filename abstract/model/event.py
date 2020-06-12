from abc import abstractmethod
from typing import List

from abstract.model import Model


class EventType:
    Connect = 'c'
    Disconnect = 'd'
    StartControl = 'sa'
    StopControl = 'so'


class Event:
    table_name = ''
    id_key = 'id'
    room_id_key = 'room_id'
    checkpoint_key = 'checkpoint'
    event_type_key = 'event_type'
    str_arg_key = 'str_arg'

    def __init__(self):
        self.id = 0  # type: int
        self.room_id = 0  # type: int
        self.checkpoint = ''  # type: str
        self.event_type = ''  # type: str
        self.str_arg = ''  # type: str


class EventModel(Model):
    @abstractmethod
    def create(self, *args) -> bool:
        pass

    @abstractmethod
    def insert_connect_event(self, room_id: int, checkpoint=None) -> int:
        pass

    @abstractmethod
    def insert_disconnect_event(self, room_id: int, checkpoint=None) -> int:
        pass

    @abstractmethod
    def insert_stop_state_control_event(self, room_id: int, checkpoint=None) -> int:
        pass

    @abstractmethod
    def insert_start_state_control_event(self, room_id: int, fan_speed: str, checkpoint=None) -> int:
        pass

    @abstractmethod
    def query_by_time_interval(self, room_id, start_time: str, stop_time: str) -> List[Event]:
        pass
