from proto import Request, Response


class MetricsRequest(Request):
    def __init__(self):
        super().__init__()
        self.token = ''  # type: str
        self.fan_speed = ''  # type: str
        self.temperature = 0.0  # type: float
        self.checkpoint = None

    def bind_dict(self, d: dict):
        if d is None:
            return
        self.fan_speed = d['fan_speed']
        self.temperature = d['temperature']

    def bind_header(self, h):
        self.token = h['Authorization']


class MetricsResponse(Response):
    def __init__(self):
        super().__init__()
