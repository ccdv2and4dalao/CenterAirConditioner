from proto import Request, Response


class GenerateStatisticRequest(Request):
    def __init__(self):
        super().__init__()


class GenerateStatisticResponse(Response):
    def __init__(self):
        super().__init__()
        self.energy = 0.0
        self.cost = 0.0

    def __dict__(self):
        pass
