from abstract.console import SetMetricFrequencyConsole
from app.console.base_subconsole import BaseSubConsoleImpl
from abstract.consensus import ConsolePrefix


class SetMetricFrequencyConsoleImpl(SetMetricFrequencyConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.set_metric_freq)

    def __call__(self, *args):
        print('process set metric freq')
        raise NotImplementedError