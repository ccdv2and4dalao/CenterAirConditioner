from proto import Request, Response

Mode = str
FanSpeed = str


class StartStateControlRequest(Request):
    def __init__(self):
        super().__init__()
        self.mode = ''  # type: Mode
        self.speed = ''  # type: FanSpeed


class StartStateControlResponse(Response):
    def __init__(self):
        super().__init__()

