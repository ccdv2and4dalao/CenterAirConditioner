import enum


class FanSpeed(enum.Enum):
    low = 'low'
    mid = 'mid'
    high = 'high'
    none = 'none'
    underlying_type = str
