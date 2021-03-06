from abc import abstractmethod
from datetime import datetime
from typing import List, Optional, Union

from abstract.model.model import Model


class EventType:
    Connect = 'c'
    Disconnect = 'd'
    StartControl = 'sa'
    StopControl = 'so'


class Event:
    table_name = 'event'
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
    def query_by_time_interval(self, room_id, start_time: Union[str, datetime], stop_time: Union[str, datetime]) -> \
            List[Event]:
        pass

    @abstractmethod
    def query_control_events_by_time_interval(self, room_id, start_time: str, stop_time: str) -> \
            List[Event]:
        pass

    @abstractmethod
    def query_last_connect_event(self, room_id) -> Optional[Event]:
        pass
