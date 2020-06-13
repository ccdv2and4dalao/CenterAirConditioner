from proto import Request, Response


class StopStateControlRequest(Request):
    def __init__(self):
        super().__init__()
        self.room_id = 0  # type: int


class StopStateControlResponse(Response):
    def __init__(self):
        super().__init__()

