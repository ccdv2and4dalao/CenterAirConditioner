from proto import Request, Response


class DisConnectionRequest(Request):
    def __init__(self):
        super().__init__()
        self.token = '' # type: str

    def bind_dict(self, d):
        if d is None:
            return
        super().bind_dict(d)

    def bind_header(self, h):
        if h is None:
            return
        super().bind_header(h)
        self.token = h['Authorization']

class DisConnectionResponse(Response):
    def __init__(self):
        super().__init__()