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
            {Metric.id_key} integer autoincrement primary key,
            {Metric.room_id_key} varchar(19),
            {Metric.checkpoint_key} timestamp default CURRENT_TIMESTAMP,
            {Metric.fan_speed_key} varchar(5),
            {Metric.temperature_key} decimal(15, 2)
        )""")

    def insert(self, room_id: str, fan_speed: str, temperature: float, checkpoint=None) -> int:
        if checkpoint is None:
            return self.db.insert(f'''
            insert into {Metric.table_name} (
            {Metric.room_id_key},
            {Metric.fan_speed_key}, 
            {Metric.temperature_key})
            values
            (%s, %s, %s)
            ''', room_id, fan_speed, temperature)
        return self.db.insert(f'''
        insert into {Metric.table_name} (
        {Metric.room_id_key},
        {Metric.checkpoint_key},
        {Metric.fan_speed_key}, 
        {Metric.temperature_key})
        values
        (%s, %s, %s, %s)
        ''', room_id, checkpoint, fan_speed, temperature)

    def query_by_time_interval(self, room_id: str, start_time: str, stop_time: str):
        data = self.db.select(f'''
        select * from {Metric.table_name} where
            {Metric.room_id_key} = %s and {Metric.checkpoint_key} between %s and %s
        ''', room_id, start_time, stop_time)
        if data is None:
            return None

        return list(map(MetricsTupleProxy, data))
