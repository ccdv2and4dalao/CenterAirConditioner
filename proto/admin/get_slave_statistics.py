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
        self.room_id = d['room_id']
        self.start_time = d['start_time']
        self.stop_time = d['stop_time']

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminGetSlaveStatisticsResponse(Response):
    def __init__(self):
        super().__init__()
