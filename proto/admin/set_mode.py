from proto import Request, Response


class AdminSetModeRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.mode = ''  # type: str


class AdminSetModeResponse(Response):
    def __init__(self):
        super().__init__()
