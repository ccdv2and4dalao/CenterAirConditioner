from dateutil.parser import parse

from proto import Request, Response


class AdminGetSlaveStatisticsRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.room_id = 0  # type: int
        self.start_time = ''  # type: str
        self.stop_time = ''  # type: str

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.room_id = int(d['room_id'])
        self.start_time = parse(d['start_time'])
        self.stop_time = parse(d['stop_time'])

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminGetSlaveStatisticsResponse(Response):
    def __init__(self):
        '''
        elements in list:
        {
            'room_id': _id,
            'start_time': '',
            'stop_time': '',
            'fan_speed': '',
            'energy': '',
            'cost': '',
        }
        '''
        super().__init__()
        self.data = []
