from abc import abstractmethod
from typing import List, Tuple

from abstract.model.model import Model


class Statistic:
    """
    详单结构和内容应至少包含：房间号、记录起止时间、起止时间内风速、起止时间内风量大小等。
    """
    table_name = 'statistic'
    id_key = 'id'
    room_id_key = 'room_id'
    checkpoint_key = 'checkpoint'
    # current_fan_speed_key = 'current_fan_speed'
    current_energy_key = 'current_energy'
    current_cost_key = 'current_cost'

    def __init__(self):
        self.id = 0  # type: int
        self.room_id = 0  # type: int
        self.checkpoint = ''  # type: str
        # self.current_fan_speed = ''  # type: str
        self.current_energy = 0.0  # type: float
        self.current_cost = 0.0  # type: float


CurrentEnergy = float
CurrentCost = float


class StatisticModel(Model):
    @abstractmethod
    def create(self, *args) -> bool:
        pass

    @abstractmethod
    def insert(self, room_id: int, energy: float, cost: float, checkpoint=None) -> int:
        pass

    @abstractmethod
    def query_by_time_interval(self, room_id, start_time, stop_time) -> List[Statistic]:
        pass

    @abstractmethod
    def query_sum_by_time_interval(self, room_id, start_time, stop_time) -> Tuple[CurrentEnergy, CurrentCost]:
        pass
