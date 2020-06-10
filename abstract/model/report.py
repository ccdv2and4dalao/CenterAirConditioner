from abc import abstractmethod
from typing import List
from .model import Model

class Report:
    table_name = 'report'
    report_no_key = 'report_no'
    room_id_key = 'room_id'
    start_time_key = 'start_time'
    stop_time_key = 'stop_time'
    start_temperature_key = 'start_temperature'
    end_temperature_key = 'end_temperature'
    energy_key = 'energy'
    cost_key = 'cost'

    def __init__(self):
        self.report_no = 0 # type: int
        self.room_id = '' # type: str 
        self.start_time = '1999-01-01 00:00:00' # type: str
        self.stop_time = '1999-01-01 00:00:00' # type: str
        self.start_temperature = 27.0 # type: float
        self.end_temperature = 21.0 # type: float
        self.energy = 0.0 # type: float
        self.cost = 0.0 # type: float


class ReportModel(Model):
    '''
    操作report表
    '''
    @abstractmethod
    def create(self) -> bool:
        pass

    @abstractmethod
    def insert(self, report: Report) -> int:
        '''
        插入一条报表（report_no不用指定）
        @return: 插入报表的report_no（数据库中唯一，按插入时间升序），插入失败则返回-1
        '''
        pass

    @abstractmethod
    def query_by_report_no(self, report_no: int) -> Report:
        pass

    @abstractmethod
    def query_by_conditions(self, room_id='', start_time='', stop_time='') -> List[Report]:
        '''
        按指定条件查询
        '''
        pass

    @abstractmethod
    def delete_by_report_no(self, report_no: int) -> bool:
        pass

    @abstractmethod
    def get_reports(self, stop_time: str, report_duration: str) -> List[Report]:
        '''
        查询到stop_time为止的报表
        @stop_time: 截止时间
        @report_duration: 报表选取时间范围
        @return: Report的列表
        '''
        pass
