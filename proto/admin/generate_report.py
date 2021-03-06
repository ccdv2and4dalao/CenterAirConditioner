﻿from proto import Request, Response


class AdminGenerateReportRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.type = ''  # type: str # one of ['day', 'week' 'month']
        self.stop_time = ''  # type: str
        self.room_id = None # type: int or None

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.type = d['type']
        self.stop_time = d.get('stop_time', '')
        self.room_id = d.get('room_id', None)

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminGenerateReportResponse(Response):
    def __init__(self):
        '''
        format of self.data:
        {
            room_id: 'A123',
            count: 0,
            items: [Report, ...],
            total_energy: 0.0,
            total_cost: 0.0
        }
        '''
        super().__init__()
        self.data = {}
