from abstract.model.model import Model
from abc import abstractmethod
from typing import List

class Statistic:
    '''
    详单结构和内容应至少包含：房间号、记录起止时间、起止时间内风速、起止时间内风量大小等。
    '''
    table_name = 'statistic'
    metric_id_key = 'statistic_id'
    room_id_key = 'room_id'
    timestamp_key = 'timestamp'
    current_fan_speed_key = 'current_fan_speed'
    current_energy_key = 'current_energy'
    current_cost_key = 'current_cost'
    def __init__(self):
        self.metric_id = 0 # type: int
        self.room_id = '' # type: str
        self.timestamp = '' # type: str
        self.current_fan_speed = '' # type: str
        self.current_energy = 0.0 # type: float
        self.current_cost = 0.0 # type: float

class StatisticModel(Model):
    @abstractmethod
    def create(self, *args) -> bool:
        pass

    @abstractmethod
    def insert(self, metric: Metric) -> int:
        pass

    @abstractmethod
    def query_by_time_interval(self, room_id, start_time: str, stop_time: str) -> List[Metric]:
        pass

