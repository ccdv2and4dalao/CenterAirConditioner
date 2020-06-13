import datetime
from typing import List, Dict, Tuple

from abstract.model import EventModel, StatisticModel, Event, EventType, RoomModel, MetricModel
from abstract.model import Report, ReportModel
from app.model.model import SQLModel
from lib.injector import Injector


class ReportModelImpl(SQLModel, ReportModel):
    def __init__(self, inj: Injector):
        super().__init__(inj)
        self.event_model = inj.require(EventModel)
        self.statistic_model = inj.require(StatisticModel)
        self.metric_model = inj.require(MetricModel)
        self.room_model = inj.require(RoomModel)


    def create(self):
        return True
        raise DeprecationWarning('this model could only use get_reports')
        sql = f"""
        CREATE TABLE IF NOT EXISTS {Report.table_name} (
            {Report.report_no_key} INT AUTO_INCREMENT PRIMARY KEY,
            {Report.room_id_key} VARCHAR(20),
            {Report.start_time_key} DATETIME,
            {Report.stop_time_key} DATETIME,
            {Report.start_temperature_key} FLOAT,
            {Report.end_temperature_key} FLOAT,
            {Report.energy_key} FLOAT,
            {Report.cost_key} FLOAT
        )
        """

        return self.db.create(sql)

    def insert(self, report: Report) -> int:
        raise DeprecationWarning('this model could only use get_reports')
        sql = f'''
        INSERT INTO {Report.table_name} (
        {Report.room_id_key}, 
        {Report.start_time_key}, {Report.stop_time_key},
        {Report.start_temperature_key}, {Report.end_temperature_key}, 
        {Report.energy_key}, {Report.cost_key}) 
        VALUES
        ({self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder},
        {self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder}, {self.db.placeholder})
        '''
        return self.db.insert(sql,
                              report.room_id, report.start_time, report.stop_time,
                              report.start_temperature, report.end_temperature, report.energy, report.cost)

    def query_by_report_no(self, report_no: int):
        raise DeprecationWarning('this model could only use get_reports')
        sql = f'''
        SELECT * FROM {Report.table_name} WHERE {Report.report_no_key} = {self.db.placeholder}
        '''
        result = self.db.select(sql, report_no)
        if result:
            r = Report()
            r.report_no, r.room_id, r.start_time, r.stop_time, r.start_temperature, r.end_temperature, \
            r.energy, r.cost = result[0]
        else:
            return

    def query_by_conditions(self, room_id='', start_time='', stop_time='') -> List[Report]:
        raise DeprecationWarning('this model could only use get_reports')
        values = []
        if room_id != '':
            room_id_str = f'{Report.room_id_key} = {self.db.placeholder}'
            values.append(room_id)
        else:
            room_id_str = None

        time_str = None
        if start_time != '':
            start_time_str = f'{Report.start_time_key} >= {self.db.placeholder}'
            values.append(start_time)
        else:
            start_time_str = None

        if stop_time != '':
            stop_time_str = '{Report.stop_time_key} <= {self.db.placeholder}'
            values.append(stop_time)
        else:
            stop_time_str = None

        if start_time_str and stop_time_str:
            time_str = '{} AND {}'.format(start_time_str, stop_time_str)
        elif start_time_str:
            time_str = start_time_str
        elif stop_time_str:
            time_str = stop_time_str
        else:
            time_str = None

        where_str = ''
        if room_id_str and time_str:
            where_str = 'WHERE {} AND {}'.format(room_id_str, time_str)
        elif room_id_str:
            where_str = 'WHERE {}'.format(room_id_str)
        elif time_str:
            where_str = 'WHERE {}'.format(time_str)
        else:
            where_str = ''

        sql = f'SELECT * FROM {Report.table_name} {where_str}'
        results = self.db.select(sql, *values)
        ret = []
        if results:
            for result in results:
                r = Report()
                r.report_no, r.room_id, r.start_time, r.stop_time, \
                r.start_temperature, r.end_temperature, \
                r.energy, r.cost = result
                ret.append(r)
        return ret

    def delete_by_report_no(self, report_no) -> bool:
        raise DeprecationWarning('this model could only use get_reports')
        sql = f'''
        DELETE FROM {Report.table_name} WHERE {Report.report_no_key} = {self.db.placeholder}
        '''
        return self.db.delete(sql, report_no)

    def get_reports(self, stop_time: datetime.datetime, report_duration: str) -> Tuple[List[Report], List[Event], Dict[int, str]]:
        report_duration = report_duration.lower()
        if report_duration not in ['day', 'month', 'week']:
            raise ValueError('report duration should in [day, month, week]')
        
        days = 1 if report_duration == 'day' else 7 if report_duration == 'week' else 30
        start_time = stop_time - datetime.timedelta(days=days)
        events = self.event_model.query_by_time_interval(None, start_time, stop_time) 

        room_event = {}
        for event in events:
            if event.room_id not in room_event.keys():
                room_event[event.room_id] = []
            room_event[event.room_id].append(event)

        events = []
        for e in room_event.values():
            while e[0].event_type != EventType.Connect:
                e.pop(0)
            while e[-1].event_type != EventType.Disconnect:
                e.pop()
            events.extend(e)


        reports = []
        id2room_id = {}
        for room, l in room_event.keys():
            room_name = self.room_model.query_by_room_id(room).room_id 
            id2room_id[room] = room_name
            left, right = 0, 1
            while left < len(l):
                while l[right].event_type != EventType.Disconnect: right += 1
                for i in (left + 1, right, 2):
                    r = Report()
                    r.room_id = room_name
                    r.start_time, r.stop_time = l[i].checkpoint, l[i + 1].checkpoint
                    if l[i].event_type != EventType.StartControl:
                        raise ValueError('event mismatch: missing {}'.format(EventType.StartControl), l[i])
                    if l[i + 1].event_type != EventType.StopControl:
                        raise ValueError('event mismatch: missing {}'.format(EventType.StopControl), l[i + 1])
                    r.energy, r.cost = self.statistic_model.query_sum_by_time_interval(room, l[i][0], l[i + 1][0])
                    metrics = self.metric_model.query_by_time_interval(room, l[i][0], l[i + 1][0])
                    r.start_temperature, r.end_temperature = metrics[0].temperature, metrics[-1].temperature
                    reports.append(r)
                left, right = right + 1, right + 2
        return reports, events, id2roomid



if __name__ == '__main__':
    pass
    # import sys

    # r = ReportModelImpl(inj)
    # r.db.connect(host=sys.argv[1], port=int(sys.argv[2]), user=sys.argv[3], password=sys.argv[4], database='backend')
    # print('create table\n', r.create())
    # repo = Report()
    # repo.cost = 998
    # id = r.insert(repo)
    # print('insert id\n', id)
    # print('delete id\n', r.delete_by_report_no(id))
    # print('delete id + 1\n', r.delete_by_report_no(id + 1))
    # repo.stop_time = '1999-01-01 00:00:00'
    # r.insert(repo)
    # repo.stop_time = '1999-01-05 00:01:00'
    # r.insert(repo)
    # repo.stop_time = '1999-01-05 00:02:00'
    # r.insert(repo)
    #
    # print('day repo\n', r.get_reports('1999-01-06', 'day'))
    # print('month repo\n', r.get_reports('1999-01-06', 'month'))
