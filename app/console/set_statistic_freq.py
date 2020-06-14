from abstract.consensus import ConsolePrefix
from abstract.console import SetStatisticFrequencyConsole
from app.console.base_subconsole import BaseSubConsoleImpl


class SetStatisticFrequencyConsoleImpl(SetStatisticFrequencyConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.set_statistic_freq)

    def __call__(self, *args):
        print('process set statistic freq')
        raise NotImplementedError
