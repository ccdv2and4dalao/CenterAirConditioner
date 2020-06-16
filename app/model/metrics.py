from collections import namedtuple

from abstract.model.metric import MetricModel, Metric
from app.model.model import SQLModel

MetricsTupleProxy = namedtuple('MetricsTupleProxy', [
    Metric.id_key,
    Metric.room_id_key,
    Metric.checkpoint_key,
    Metric.fan_speed_key,
    Metric.temperature_key,
])


class MetricsModelImpl(SQLModel, MetricModel):
    def create(self, *args) -> bool:
        return self.db.create(f"""
        create table if not exists {Metric.table_name} (
            {Metric.id_key} integer primary key {self.db.auto_increment},
            {Metric.room_id_key} integer,
            {Metric.checkpoint_key} timestamp default CURRENT_TIMESTAMP,
            {Metric.fan_speed_key} varchar(5),
            {Metric.temperature_key} decimal(15, 8)
        )""")

    def insert(self, room_id: int, fan_speed: str, temperature: float, checkpoint=None) -> int:
        if checkpoint is None:
            return self.db.insert(f'''
            insert into {Metric.table_name} (
            {Metric.room_id_key},
            {Metric.fan_speed_key}, 
            {Metric.temperature_key})
            values
            ({self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder})
            ''', room_id, fan_speed, temperature)
        return self.db.insert(f'''
        insert into {Metric.table_name} (
        {Metric.room_id_key},
        {Metric.checkpoint_key},
        {Metric.fan_speed_key}, 
        {Metric.temperature_key})
        values
        ({self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder})
        ''', room_id, checkpoint, fan_speed, temperature)

    def query_by_time_interval(self, room_id: int, start_time: str, stop_time: str):
        data = self.db.select(f'''
        select * from {Metric.table_name} where
            {Metric.room_id_key} = {self.db.placeholder} and {Metric.checkpoint_key} between {self.db.placeholder} and {self.db.placeholder}
        ''', room_id, start_time, stop_time)
        if data is None:
            return None

        return [MetricsTupleProxy(*d) for d in data]
