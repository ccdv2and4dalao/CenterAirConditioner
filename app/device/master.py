from abstract.device import MasterAirconDevice
from abstract.consensus import AirMode
from abstract.consensus import FanSpeed
import threading


class MasterAirconDeviceImpl(MasterAirconDevice):
    """
    member:
        is_running: is on working -> type: bool
        current mode: current aircon mode -> type: AirMode
        current_temp: current temperature of three aircon core -> type: list[float]
        target_temp: target temperature of each core -> type: list[float]
        routine: updating temperature routine for each core -> type: list[threading.Timer]
        effiency: time consumption to increase or decrease per Celsius degree -> type: float
    """

    core_num = 3

    def __init__(self):
        self.is_running = False
        self.current_mode = AirMode.Cool
        self.current_temp = [self.get_default_temperature(self.current_mode)] * self.core_num
        self.target_temp = [None] * 3
        self.effiency = 1
        self.routine = [threading.Timer(None, None)] * self.core_num

    def update_temperature(self, core_id):
        if self.target_temp[core_id] > self.current_temp[core_id]:
            self.current_temp[core_id] = min(
                self.get_temp_constraint(self.current_mode).stop - 1,
                self.current_temp[core_id] + min(1, self.target_temp[core_id] - self.current_temp[core_id]))
        elif self.target_temp[core_id] < self.current_temp[core_id]:
            self.current_temp[core_id] = min(
                self.get_temp_constraint(self.current_mode).start,
                self.current_temp[core_id] + min(1, self.target_temp[core_id] - self.current_temp[core_id]))
        if self.target_temp[core_id] != self.current_temp[core_id]:
            self.fresh_routine(core_id)

    def get_temp_constraint(self, mode):
        tc = {
            AirMode.Cool: range(18, 25+1),
            AirMode.Heat: range(25, 30+1)
        }
        return tc[mode]

    def get_default_temperature(self, mode):
        dt = {
            AirMode.Cool: 22,
            AirMode.Heat: 28
        }
        return dt[mode]

    def get_currrent_temperature(self):
        return self.current_temp

    def fresh_routine(self, core_id):
        """
        reschedule next update
        """
        if self.routine[core_id] and self.routine[core_id].is_alive():
            self.routine[core_id].cancel()
        self.routine[core_id] = threading.Timer(
            self.effiency, self.update_temperature, (core_id,))
        self.routine[core_id].start()

    def suppy_to(self, target_temp: float):
        for i in range(self.core_num):
            if not self.routine[i].is_alive():
                self.target_temp[i] = target_temp
                self.fresh_routine(i)
                return

    def boot(self):
        self.is_running = True

    def shutdown(self):
        self.is_running = False
