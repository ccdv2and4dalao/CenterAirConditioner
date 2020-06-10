from abstract.model import Report, ReportModel
from app.database import sqlDatabase
from typing import List

class ReportModelImpl(ReportModel):
    def __init__(self):
        self.db = sqlDatabase

    def create(self):
        sql = f'''
        CREATE TABLE IF NOT EXISTS %s (
            %s INT AUTO_INCREMENT PRIMARY KEY,
            %s VARCHAR(20) REFERENCE ROOM,
            %s DATETIME,
            %s DATETIME,
            %s FLOAT,
            %s FLOAT,
            %s FLOAT,
            %s FLOAT
        )
        '''.replace('\n', '')
        return self.db.create(sql, Report.table_name,
                       Report.report_no_key, Report.room_id_key, Report.start_time_key, Report.stop_time_key,
                       Report.start_temperature_key, Report.end_temperature_key, Report.energy_key, Report.cost_key)

    def insert(self, report: Report) -> int:
        sql = '''
        INSERT INTO %s (
        %s, 
        %s, %s,
        %s, %s, 
        %s, %s) 
        VALUES
        (%s, %s, %s,
        %s, %s, %s, %s)
        '''
        return self.db.insert(sql, Report.table_name,
                          Report.room_id_key, 
                          Report.start_time_key, Report.stop_time_key, 
                          Report.start_temperature_key, Report.end_temperature_key, 
                          Report.energy_key, Report.cost_key, 
                          report.room_id, report.start_time, report.stop_time,
                          report.start_temperature, report.end_temperature, report.energy, report.cost)
    
    def query_by_report_no(self, report_no: int) -> Report or None:
        sql = f'''
        SELECT * FROM %s WHERE %s = %s
        '''
        result = self.db.select(sql, Report.table_name, Report.report_no_key, report_no)
        if result:
            r = Report()
            r.report_no, r.room_id, r.start_time, r.stop_time, r.start_temperature, r.end_temperature,\
            r.energy, r.cost = result[0]
        else:
            return None

    def query_by_conditions(self, room_id='', start_time='', stop_time='') -> List[Report]:
        values = []
        if room_id != '':
            room_id_str = '%s = %s'
            values.append(Report.room_id_key)
            values.append(room_id)
        else:
            room_id_str = None

        time_str = None
        if start_time != '':
            start_time_str = '%s >= %s'
            values.append(Report.start_time_key)
            values.append(start_time)
        else:
            start_time_str = None

        if stop_time != '':
            stop_time_str = '%s <= %s'
            values.append(Report.stop_time_key)
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

        sql = 'SELECT * FROM %s {}'.format(where_str)
        results = self.db.select(sql, Report.table_name, *values)
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
        sql = '''
        DELETE FROM %s WHERE %s = %s
        '''
        return self.db.delete(sql, Report.table_name, Report.report_no_key, report_no)

    def get_reports(self, stop_time: str, report_duration: str):
        if report_duration.lower() not in ['day', 'month', 'week']:
            raise ValueError('report duraion should in [day, month, week]')
        sql = '''
        SELECT * FROM %s
        WHERE %s BETWEEN 
        date_sub(%s, interval 1 %s) AND %s
        '''
        results = self.db.select(sql, Report.table_name, Report.stop_time_key, 
                                 stop_time, report_duration, stop_time)
        ret = []
        if results:
            for result in results:
                r = Report()
                r.report_no, r.room_id, r.start_time, r.stop_time, \
                r.start_temperature, r.end_temperature,\
                r.energy, r.cost = result
                ret.append(r)
        return ret


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