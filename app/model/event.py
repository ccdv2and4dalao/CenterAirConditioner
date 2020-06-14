from typing import List, Optional

from abstract.model.event import EventModel, Event, EventType
from app.model.model import SQLModel
import lib.dateutil
from collections import namedtuple

EventTupleProxy = namedtuple('MetricsTupleProxy', [
    Event.id_key,
    Event.room_id_key,
    Event.checkpoint_key,
    Event.event_type_key,
    Event.str_arg_key,
])



class EventModelImpl(SQLModel, EventModel):
    def create(self, *args) -> bool:
        sql = f'''
        CREATE TABLE IF NOT EXISTS {Event.table_name} (
        {Event.id_key}          INT {self.db.auto_increment} PRIMARY KEY,
        {Event.room_id_key}     INT,
        {Event.checkpoint_key}  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        {Event.event_type_key}  VARCHAR(5), 
        {Event.str_arg_key}     VARCHAR(255)
        )
        '''
        return self.db.create(sql)

    def __insert_state_event(self, room_id: int, event_type: str, checkpoint=None):
        if checkpoint is None:
            sql = f'''
            INSERT INTO {Event.table_name} (
                {Event.room_id_key},
                {Event.event_type_key}
            ) VALUES (
                {self.db.placeholder},
                {self.db.placeholder}
            )
            '''
            return self.db.insert(sql, room_id, event_type)
        else:
            sql = f'''
            INSERT INTO {Event.table_name} (
                {Event.room_id_key},
                {Event.checkpoint_key},
                {Event.event_type_key}
            ) VALUES (
                {self.db.placeholder},
                {self.db.placeholder},
                {event_type}
            )
            '''
            return self.db.insert(sql, room_id, event_type, checkpoint)

    def insert_connect_event(self, room_id: int, checkpoint=None) -> int:
        return self.__insert_state_event(room_id, EventType.Connect, checkpoint=checkpoint)

    def insert_disconnect_event(self, room_id: int, checkpoint=None) -> int:
        return self.__insert_state_event(room_id, EventType.Disconnect, checkpoint=checkpoint)

    def insert_stop_state_control_event(self, room_id: int, checkpoint=None) -> int:
        return self.__insert_state_event(room_id, EventType.StopControl, checkpoint=checkpoint)

    def insert_start_state_control_event(self, room_id: int, fan_speed: str, checkpoint=None) -> int:
        if checkpoint is None:
            sql = f'''
            INSERT INTO {Event.table_name} (
                {Event.room_id_key},
                {Event.event_type_key},
                {Event.str_arg_key}
            ) VALUES (
                {self.db.placeholder},
                {self.db.placeholder},
                {self.db.placeholder}
            )
            '''
            return self.db.insert(sql, room_id, EventType.StartControl, fan_speed)
        else:
            sql = f'''
            INSERT INTO {Event.table_name} (
                {Event.room_id_key},
                {Event.checkpoint_key},
                {Event.event_type_key},
                {Event.str_arg_key}
            ) VALUES (
                {self.db.placeholder},
                {self.db.placeholder},
                {self.db.placeholder},
                {self.db.placeholder}
            )
            '''
            return self.db.insert(sql, room_id, EventType.StartControl, checkpoint, fan_speed)

    def query_by_time_interval(self, room_id, start_time, stop_time) -> List[Event]:
        if type(start_time) is not str:
            start_time = lib.dateutil.to_local(start_time)
        if type(stop_time) is not str:
            stop_time = lib.dateutil.to_local(stop_time)
        if room_id is None:
            sql = f'''
            SELECT * FROM {Event.table_name}
            WHERE {Event.checkpoint_key} BETWEEN {self.db.placeholder} AND {self.db.placeholder}
            '''
            data = self.db.select(sql, start_time, stop_time)
        else:
            sql = f'''
            SELECT * FROM {Event.table_name}
            WHERE {Event.checkpoint_key} BETWEEN {self.db.placeholder} AND {self.db.placeholder}
            AND {Event.room_id_key} = {self.db.placeholder}
            '''
            data = self.db.select(sql, start_time, stop_time, room_id)
        if data is None:
            return None

        return [EventTupleProxy(*d) for d in data]

    def query_last_connect_event(self, room_id) -> Optional[Event]:
        sql = f'''
        SELECT * FROM {Event.table_name}
        WHERE {Event.event_type_key} = {self.db.placeholder} 
        AND {Event.room_id_key} = {self.db.placeholder}
        '''
        data = self.db.select(sql, EventType.Connect, room_id)
        return EventTupleProxy(*data[-1]) if data is not None else None


if __name__ == '__main__':
    pass

"""
    from lib.injector import Injector
    from lib.serializer import Serializer, JSONSerializer
    from abstract.database import SQLDatabase
    from app.database.database import sqlDatabase
    from time import sleep
    import sys
    from datetime import datetime
    sqlDatabase.connect(host=sys.argv[1], port=int(sys.argv[2]), user=sys.argv[3], password=sys.argv[4], database=sys.argv[5])
    inj = Injector()
    inj.provide(SQLDatabase, sqlDatabase)
    inj.provide(Serializer, JSONSerializer())
    em = EventModelImpl(inj)
    print(em.create())
    sleep(2)
    print(em.insert_connect_event(1))
    sleep(3)
    print(em.insert_start_state_control_event(1, 'high'))
    sleep(2)
    print(em.insert_stop_state_control_event(1))
    sleep(2)
    print(em.insert_disconnect_event(1))
    print(lib.dateutil.to_utc(datetime(2020, 6, 12, 22, 00, 00)))
    print(em.query_by_time_interval(None, datetime(2020, 6, 12, 22, 00, 00), 
                                    datetime(2020, 6, 12, 23, 00, 00)))
"""