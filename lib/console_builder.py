from abstract.console import MainConsole, BootConsole, MetricConsole, ReportConsole, \
    SetMetricFrequencyConsole, SetModeConsole, SetStatisticFrequencyConsole, \
    SetTemperatureConsole, ShutdownConsole, StatusConsole
from app.console import MainConsoleImpl, BootConsoleImpl, MetricConsoleImpl, ReportConsoleImpl, \
    SetMetricFrequencyConsoleImpl, SetModeConsoleImpl, SetStatisticFrequencyConsoleImpl, \
    SetTemperatureConsoleImpl, ShutdownConsoleImpl, StatusConsoleImpl
from lib.injector import Injector


def build_and_run_console(inj: Injector):
    inj.provide(MainConsole, MainConsoleImpl())
    inj.build(BootConsole, BootConsoleImpl)
    inj.build(MetricConsole, MetricConsoleImpl)
    inj.build(ReportConsole, ReportConsoleImpl)
    inj.build(SetMetricFrequencyConsole, SetMetricFrequencyConsoleImpl)
    inj.build(SetModeConsole, SetModeConsoleImpl)
    inj.build(SetStatisticFrequencyConsole, SetStatisticFrequencyConsoleImpl)
    inj.build(SetTemperatureConsole, SetTemperatureConsoleImpl)
    inj.build(ShutdownConsole, ShutdownConsoleImpl)
    inj.build(StatusConsole, StatusConsoleImpl)

    console = inj.require(MainConsole)
    console.start()
