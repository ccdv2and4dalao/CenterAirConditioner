from proto import Request, Response


class AdminGetServerStatusRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str

    def bind_header(self, h):
        self.jwt_token = h['Authorization']


class AdminGetServerStatusResponse(Response):
    def __init__(self):
        super().__init__()
        self.server_state = ''  # type: str
        self.mode = ''  # type: str
