from proto import Request, Response

Mode = str
FanSpeed = str


class StartStateControlRequest(Request):
    def __init__(self):
        super().__init__()
        self.mode = ''  # type: Mode
        self.speed = ''  # type: FanSpeed
        self.token = ''  # type: str

    def bind_dict(self, d):
        if d is None:
            return
        super().bind_dict(d)
        self.mode = d['mode']
        self.speed = d['speed']

    def bind_header(self, h):
        if h is None:
            return
        super().bind_header(h)
        self.token = h['token']

class StartStateControlResponse(Response):
    def __init__(self):
        super().__init__()

