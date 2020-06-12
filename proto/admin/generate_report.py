from proto import Request, Response
from typing import Dict

class AdminGenerateReportRequest(Request):
    def __init__(self):
        super().__init__()
        self.type = '' # type: str ['day', 'week' 'month']
        self.stop_time = '' # type: str

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.type = d['type']
        self.stop_time = d['stop_time']

    def bind_header(self, h):
        self.jwt_token = h['Authorization']

class AdminGenerateReportResponse(Response):
    def __init__(self):
        '''
        format of the elements in self.room_list:
        {
            room_id: 'A123',
            items: [Report, ...]
            total_energy: 0.0,
            total_cost: 0.0,
            events: [Event, ...]
        }
        '''
        super().__init__()
        self.room_list = []

