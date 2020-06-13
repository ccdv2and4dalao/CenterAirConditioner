from abc import abstractmethod
from typing import List

from abstract.model.model import Model


class Metric:
    """
    8.	中央空调能够实时监测各房间的温度和状态，并要求实时刷新的频率能够进行配置
    """
    table_name = 'metric'
    id_key = 'id'
    room_id_key = 'room_id'
    checkpoint_key = 'checkpoint'
    fan_speed_key = 'fan_speed'
    temperature_key = 'temperature'

    def __init__(self):
        self.id = 0  # type: int
        self.room_id = 0  # type: int
        self.checkpoint = ''  # type: str
        self.fan_speed = ''  # type: str
        self.temperature = 0.0  # type: float


class MetricModel(Model):
    @abstractmethod
    def create(self, *args) -> bool:
        pass

    @abstractmethod
    def insert(self, room_id: int, fan_speed: str, temperature: float, checkpoint=None) -> int:
        pass

    @abstractmethod
    def query_by_time_interval(self, room_id: int, start_time: str, stop_time: str) -> List[Metric]:
        pass
