import lib.dateutil
from abstract.model.statistic import StatisticModel, Statistic
from app.model.model import SQLModel


class StatisticTupleProxy:

    def __init__(self, tup):
        self.tup = tup
        # self.id = 0  # type: int
        # self.room_id = 0  # type: int
        # self.checkpoint = ''  # type: str
        # # self.current_fan_speed = ''  # type: str
        # self.current_energy = 0.0  # type: float
        # self.current_cost = 0.0  # type: float

    @property
    def id(self):
        return self.tup[0]

    @property
    def room_id(self):
        return self.tup[1]

    @property
    def checkpoint(self):
        return self.tup[2]

    @property
    def current_energy(self):
        return self.tup[3]

    @property
    def current_cost(self):
        return self.tup[4]


class StatisticModelImpl(SQLModel, StatisticModel):
    def create(self, *args) -> bool:
        return self.db.create(f"""
        create table if not exists {Statistic.table_name} (
            {Statistic.id_key} integer primary key {self.db.auto_increment},
            {Statistic.room_id_key} integer,
            {Statistic.checkpoint_key} timestamp default CURRENT_TIMESTAMP,
            {Statistic.current_energy_key} decimal(15, 2),
            {Statistic.current_cost_key} decimal(15, 2)
        )
        """)

    def insert(self, room_id: int, energy: float, cost: float, checkpoint=None) -> int:
        if checkpoint is not None:
            return self.db.insert(f'''
            insert into {Statistic.table_name} (
            {Statistic.room_id_key},
            {Statistic.checkpoint_key},
            {Statistic.current_energy_key}, 
            {Statistic.current_cost_key})
            values
            ({self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder})
            ''', room_id, checkpoint, energy, cost)
        return self.db.insert(f'''
        insert into {Statistic.table_name} (
        {Statistic.room_id_key},
        {Statistic.current_energy_key}, 
        {Statistic.current_cost_key})
        values
        ({self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder})
        ''', room_id, energy, cost)

    def query_by_time_interval(self, room_id, start_time, stop_time):
        data = self.db.select(f'''
        select * from {Statistic.table_name} where
            {Statistic.room_id_key} = {self.db.placeholder} and {Statistic.checkpoint_key} between {self.db.placeholder} and {self.db.placeholder}
        ''', room_id, lib.dateutil.to_local(start_time), lib.dateutil.to_local(stop_time))
        if data is None:
            return None

        return list(map(StatisticTupleProxy, data))

    def query_sum_by_time_interval(self, room_id, start_time, stop_time):
        data = self.db.select(f'''
        select sum({Statistic.current_energy_key}), sum({Statistic.current_cost_key}) from {Statistic.table_name} where
            {Statistic.room_id_key} = {self.db.placeholder} and {Statistic.checkpoint_key} between {self.db.placeholder} and {self.db.placeholder}
        ''', room_id, start_time, stop_time)
        if data is None:
            return None
        return data[0]
