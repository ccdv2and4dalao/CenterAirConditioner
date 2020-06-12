from typing import List

from abstract.model.event import EventModel, Event
from app.model.model import SQLModel


class EventModelImpl(SQLModel, EventModel):

    def create(self, *args) -> bool:
        pass

    def insert_connect_event(self, room_id: int, checkpoint=None) -> int:
        pass

    def insert_disconnect_event(self, room_id: int, checkpoint=None) -> int:
        pass

    def insert_stop_state_control_event(self, room_id: int, checkpoint=None) -> int:
        pass

    def insert_start_state_control_event(self, room_id: int, fan_speed: str, checkpoint=None) -> int:
        pass

    def query_by_time_interval(self, room_id, start_time: str, stop_time: str) -> List[Event]:
        pass
