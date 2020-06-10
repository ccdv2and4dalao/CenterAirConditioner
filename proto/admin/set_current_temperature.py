from proto import Request, Response


class AdminSetCurrentTemperatureRequest(Request):
    def __init__(self):
        super().__init__()
        self.jwt_token = ''  # type: str
        self.target = 0.0  # type: float


class AdminSetCurrentTemperatureResponse(Response):
    def __init__(self):
        super().__init__()
