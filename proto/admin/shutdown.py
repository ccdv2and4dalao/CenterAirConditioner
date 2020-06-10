from proto import Request, Response


class AdminShutdownRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str


class AdminShutdownResponse(Response):
    def __init__(self):
        super().__init__()
