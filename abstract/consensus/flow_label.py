import enum


class FlowLabel(enum.Enum):
    Ping = 1
    Connect = 2
    StartStateControl = 3
    StopStateControl = 4
    Metrics = 5
    GenerateStatistics = 6
    GetServerStatus = 7
    UpdateMetrics = 8
    GetConnectedSlaves = 9

    AdminSetMode = 7
    AdminSetCurrentTemperature = 8
    AdminGetServerStatus = 9

    AdminLogin = 1001
    AdminBoot = 1002
    AdminShutdown = 1003
