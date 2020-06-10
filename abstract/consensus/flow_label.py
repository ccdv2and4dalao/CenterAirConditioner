import enum


class FlowLabel(enum.Enum):
    Ping = 1
    Connect = 2
    StartStateControl = 3
    StopStateControl = 4
    Metrics = 5
    GenerateStatistics = 6
