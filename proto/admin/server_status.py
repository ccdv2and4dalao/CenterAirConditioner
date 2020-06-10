from proto import Request, Response


class AdminGetServerStatusRequest(Request):
    def __init__(self):
        super().__init__()
        self.admin_token = ''  # type: str


class AdminGetServerStatusResponse(Response):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
