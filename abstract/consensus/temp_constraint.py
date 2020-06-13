from .air_mode import AirMode


class AirconTempConstraint(object):
    def __init__(self):
        self.temp_constraint = {
            AirMode.Cool.value: range(18, 25 + 1),
            AirMode.Heat.value: range(25, 30 + 1)
        }

    def get_contraint(self, mode: AirMode):
        return self.temp_constraint[mode]
