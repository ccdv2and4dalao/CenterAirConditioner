from proto import Request, Response


class StopStateControlRequest(Request):
    def __init__(self):
        super().__init__()
        self.token = ''  # type: str
        self.room_id = 0  # type: int

    def bind_dict(self, d):
        if d is None:
            return
        super().bind_dict(d)
        # self.room_id = d['room_id']

    def bind_header(self, h):
        if h is None:
            return
        super().bind_header(h)
        self.token = h['Authorization']


class StopStateControlResponse(Response):
    def __init__(self):
        super().__init__()

