from typing import List

from abstract.model import Report, ReportModel
from app.model.model import SQLModel


class ReportModelImpl(SQLModel, ReportModel):
    def __init__(self, inj):
        super().__init__(inj)

    def create(self):
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
        sql = f'''
        INSERT INTO {Report.table_name} (
        {Report.room_id_key}, 
        {Report.start_time_key}, {Report.stop_time_key},
        {Report.start_temperature_key}, {Report.end_temperature_key}, 
        {Report.energy_key}, {Report.cost_key}) 
        VALUES
        (%s, %s, %s,
        %s, %s, %s, %s)
        '''
        return self.db.insert(sql,
                          report.room_id, report.start_time, report.stop_time,
                          report.start_temperature, report.end_temperature, report.energy, report.cost)

    def query_by_report_no(self, report_no: int):
        sql = f'''
        SELECT * FROM {Report.table_name} WHERE {Report.report_no_key} = %s
        '''
        result = self.db.select(sql, report_no)
        if result:
            r = Report()
            r.report_no, r.room_id, r.start_time, r.stop_time, r.start_temperature, r.end_temperature, \
            r.energy, r.cost = result[0]
        else:
            return

    def query_by_conditions(self, room_id='', start_time='', stop_time='') -> List[Report]:
        values = []
        if room_id != '':
            room_id_str = f'{Report.room_id_key} = %s'
            values.append(room_id)
        else:
            room_id_str = None

        time_str = None
        if start_time != '':
            start_time_str = f'{Report.start_time_key} >= %s'
            values.append(start_time)
        else:
            start_time_str = None

        if stop_time != '':
            stop_time_str = '{Report.stop_time_key} <= %s'
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
                r.start_temperature, r.end_temperature,\
                r.energy, r.cost = result
                ret.append(r)
        return ret

    def delete_by_report_no(self, report_no) -> bool:
        sql = f'''
        DELETE FROM {Report.table_name} WHERE {Report.report_no_key} = %s
        '''
        return self.db.delete(sql, report_no)

    def get_reports(self, stop_time: str, report_duration: str):
        if report_duration.lower() not in ['day', 'month', 'week']:
            raise ValueError('report duraion should in [day, month, week]')
        sql = f'''
        SELECT * FROM {Report.table_name}
        WHERE {Report.stop_time_key} BETWEEN 
        date_sub(%s, interval 1 {report_duration}) AND %s
        '''
        results = self.db.select(sql, stop_time, stop_time)
        ret = []
        if results is not None:
            for result in results:
                r = Report()
                r.report_no, r.room_id, r.start_time, r.stop_time, \
                r.start_temperature, r.end_temperature,\
                r.energy, r.cost = result
                ret.append(r)
            return ret
        else:
            return None


if __name__ == '__main__':
    import sys
    r = ReportModelImpl()
    r.db.connect(host=sys.argv[1], port=int(sys.argv[2]), user=sys.argv[3], password=sys.argv[4], database='backend')
    print('create table\n', r.create())
    repo = Report()
    repo.cost = 998
    id = r.insert(repo)
    print('insert id\n', id)
    print('delete id\n', r.delete_by_report_no(id))
    print('delete id + 1\n', r.delete_by_report_no(id + 1))
    repo.stop_time = '1999-01-01 00:00:00'
    r.insert(repo)
    repo.stop_time = '1999-01-05 00:01:00'
    r.insert(repo)
    repo.stop_time = '1999-01-05 00:02:00'
    r.insert(repo)

    print('day repo\n', r.get_reports('1999-01-06', 'day'))
    print('month repo\n', r.get_reports('1999-01-06', 'month'))