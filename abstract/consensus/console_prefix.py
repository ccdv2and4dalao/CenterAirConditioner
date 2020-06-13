import enum


class ConsolePrefix(enum.Enum):
    boot = 'boot'
    metric = 'metric'
    report = 'report'
    set_metric_freq = 'metricfreq'
    set_mode = 'mode'
    set_statistic_freq = 'statisticfreq'
    set_temperature = 'temperature'
    shutdown = 'shutdown'
    status = 'status'
    underlying_type = str
