from proto import Request, Response


class AdminLoginRequest(Request):
    def __init__(self):
        super().__init__()
        self.admin_token = ''  # type: str


class AdminLoginResponse(Response):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
