from proto import Request, Response


class AdminShutdownRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminShutdownResponse(Response):
    def __init__(self):
        super().__init__()
