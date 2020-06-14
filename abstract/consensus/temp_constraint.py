from .air_mode import AirMode

class Interval(object):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper

    def __contains__(self, item):
        return self.lower <= item <= self.upper

class AirconTempConstraint(object):
    temp_constraint = {
        AirMode.Cool.value: Interval(18, 25),
        AirMode.Heat.value: Interval(25, 30)
    }
    def __init__(self):
        pass

    @staticmethod
    def get_contraint(mode: AirMode):
        return AirconTempConstraint.temp_constraint[mode]
