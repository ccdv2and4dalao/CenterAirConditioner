import enum


class AirMode(enum.Enum):
    Heat = 'heat'
    Cool = 'cool'
    Stop = 'stop'

    underlying_type = str
