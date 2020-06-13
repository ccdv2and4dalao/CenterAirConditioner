import enum


class FanSpeed(enum.Enum):
    High = 'high'
    Mid = 'mid'
    Low = 'low'
    Non = 'non'

    underlying_type = str
