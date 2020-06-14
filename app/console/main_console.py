from threading import Thread

from abstract.console import MainConsole
from lib.std_logging import StdLoggerImpl


class MainConsoleImpl(MainConsole, Thread):
    def __init__(self):
        super().__init__()
        self.m = {}
        self.m['help'] = self.help
        self.logger = StdLoggerImpl()
        self.setDaemon(True)

    def parse(self, cmd: str):
        args = cmd.split(' ')
        try:
            self.m[args[0].lower()](*args[1:])
        except KeyError as e:
            # self.logger.warn('Unexpected command {}\ninput help for all available command'.format(e))
            print('Unexpected command {}\ninput help for all available command'.format(e))
        except Exception as e:
            # self.logger.error(e)
            print(e)

    def run(self):
        print('Welcome to MasterAirConditioner V0.0.1')
        while True:
            cmd = input('> ')
            self.parse(cmd)
            print('')

    def register(self, prefix, obj):
        self.m[prefix] = obj

    def help(self, *args):
        print(self.m.keys())


if __name__ == '__main__':
    pass
'''
    from lib.injector import Injector
    from abstract.console import BootConsole, MetricConsole, ReportConsole, \
        SetMetricFrequencyConsole, SetModeConsole, SetStatisticFrequencyConsole, \
        SetTemperatureConsole, ShutdownConsole, StatusConsole
    from app.console import BootConsoleImpl, MetricConsoleImpl, ReportConsoleImpl, \
        SetMetricFrequencyConsoleImpl, SetModeConsoleImpl, SetStatisticFrequencyConsoleImpl, \
        SetTemperatureConsoleImpl, ShutdownConsoleImpl, StatusConsoleImpl
    inj = Injector()
    m = MainConsoleImpl()
    inj.provide(MainConsole, m)
    inj.build(BootConsole, BootConsoleImpl)
    inj.build(MetricConsole, MetricConsoleImpl)
    inj.build(ReportConsole, ReportConsoleImpl)
    inj.build(SetMetricFrequencyConsole, SetMetricFrequencyConsoleImpl)
    inj.build(SetModeConsole, SetModeConsoleImpl)
    inj.build(SetStatisticFrequencyConsole, SetStatisticFrequencyConsoleImpl)
    inj.build(SetTemperatureConsole, SetTemperatureConsoleImpl)
    inj.build(ShutdownConsole, ShutdownConsoleImpl)
    inj.build(StatusConsole, StatusConsoleImpl)

    m.start()
'''
