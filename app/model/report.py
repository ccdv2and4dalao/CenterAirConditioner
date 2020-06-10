from abstract.model import Report, ReportModel
from app.database import sqlDatabase
from typing import List

class ReportModelImpl(ReportModel):
    def __init__(self):
        self.db = sqlDatabase
        self.max_report_no = None

    def create(self):
        sql = f'''
        CREATE TABLE IF NOT EXISTS {Report.table_name} (
            {Report.report_no_key}           INT PRIMARY KEY,
            {Report.room_id_key}             CHAR(20) REFERENCE ROOM,
            {Report.start_time_key}          DATETIME,
            {Report.stop_time_key}           DATETIME,
            {Report.start_temperature_key}   FLOAT,
            {Report.end_temperature_key}     FLOAT,
            {Report.energy_key}              FLOAT,
            {Report.cost_key}                FLOAT
        )
        '''
        self.db.create(sql)

    def __query_max_report_no(self):
        sql = f'''
        SELECT MAX({Report.report_no_key}) FROM {Report.table_name}
        '''
        ret = self.db.select(sql)
        self.max_report_no = ret[0][0]

    def insert(self, report: Report) -> int:
        if self.max_report_no is None:
            self.__query_max_report_no()
        insert_no = self.max_report_no + 1
        report.report_no = insert_no
        sql = f'''
        INSERT INTO {Report.table_name} (
        {Report.report_no_key}, {Report.room_id_key}, 
        {Report.start_time_key}, {Report.stop_time_key},
        {Report.start_temperature_key}, {Report.end_temperature_key}, 
        {Report.energy_key}, {Report.cost_key}) 
        VALUES
        ({report.report_no}, '{report.room_id}', 
        '{report.start_time}', '{report.stop_time}', 
        {report.start_temperature}, {report.end_temperature}, 
        {report.energy}, {report.cost})
        '''
        if self.db.insert(sql):
            self.max_report_no = insert_no
            return insert_no
        else:
            return -1

    def query_by_report_no(self, report_no: int) -> Report or None:
        sql = f'''
        SELECT * FROM {Report.table_name} WHERE {Report.report_no_key} = {report_no}
        '''
        result = self.db.select(sql)
        if result:
            r = Report()
            r.report_no, r.room_id, r.start_time, r.stop_time, r.start_temperature, r.end_temperature,\
            r.energy, r.cost = *result[0]
        else:
            return None

    def query_by_conditions(self, room_id='', start_time='', stop_time='') -> List[Report]:
        room_id_str = None if room_id == '' else f'''{Report.room_id_key} = '{room_id}' '''
        time_str = None
        start_time_str = None if start_time == '' else  f'''{Report.start_time_key} >= '{start_time}' '''
        stop_time_str = None if stop_time == '' else f'''{Report.end_time_key} <= '{stop_time}' '''
            
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

        sql = 'SELECT * FROM {} {}'.format(Report.table_name, where_str)
        results = self.db.select(sql)
        ret = []
        if results:
            for result in results:
                r = Report()
                r.report_no, r.room_id, r.start_time, r.stop_time, \
                r.start_temperature, r.end_temperature,\
                r.energy, r.cost = *result
                ret.append(r)
        return ret

    def delete_by_report_no(self, report_no) -> bool:
        sql = f'''
        DELETE FROM {Report.table_name} WHERE {Report.report_no_key} = {report_no}
        '''
        return self.db.delete(sql)

    def generate_report(self, stop_time: str, report_duration: str):
        if report_duration not in ['day', 'month', 'week']:
            raise ValueError('report duraion should in [day, month, week]')
        sql = f'''
        SELECT * FROM {Report.table_name} 
        WHERE {Report.stop_time_key} BETWEEN 
        date_sub({stop_time}, interval 1 {report_duration}) AND {stop_time}
        '''
        results = self.db.select(sql)
        ret = []
        if results:
            for result in results:
                r = Report()
                r.report_no, r.room_id, r.start_time, r.stop_time, \
                r.start_temperature, r.end_temperature,\
                r.energy, r.cost = *result
                ret.append(r)
        return ret
