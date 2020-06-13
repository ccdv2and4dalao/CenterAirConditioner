import enum


class FanSpeed(enum.Enum):
    Low = "low"
    Medium = "medium"
    High = "high"

    underlying_type = str
