from proto import Request, Response


class StopStateControlRequest(Request):
    def __init__(self):
        super().__init__()
        self.token = ''  # type: str


class StopStateControlResponse(Response):
    def __init__(self):
        super().__init__()

