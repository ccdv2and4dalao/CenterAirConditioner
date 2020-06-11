from abstract.model.model import Model
from abc import abstractmethod
from typing import List

class Metric:
    '''
    8.	中央空调能够实时监测各房间的温度和状态，并要求实时刷新的频率能够进行配置
    '''
    table_name = 'metric'
    metric_id_key = 'metric_id'
    room_id_key = 'room_id'
    timestamp_key = 'timestamp'
    fan_speed_key = 'fan_speed'
    temperature_key = 'temperature'
    def __init__(self):
        self.metric_id = 0 # type: int
        self.room_id = '' # type: str
        self.timestamp = '' # type: str
        self.fan_speed = '' # type: str
        self.temperature = 0.0 # type: float

class MetricModel(Model):
    @abstractmethod
    def create(self, *args) -> bool:
        pass

    @abstractmethod
    def insert(self, metric: Metric) -> int:
        pass

    @abstractmethod
    def query_by_time_interval(self, room_id, start_time: str, stop_time: str) -> List[Metric]:
        pass

