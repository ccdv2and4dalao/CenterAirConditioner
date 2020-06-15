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
    GetConnectedSlave = 10
    Disconnect = 11

    AdminSetMode = 101
    AdminSetCurrentTemperature = 102
    AdminGetServerStatus = 103
    AdminGetSlaveStatistics = 104
    AdminGetRoomCount = 105
    AdminGetReport = 106
    AdminSetMetricsDelay = 107
    AdminSetUpdateDelay = 108

    AdminLogin = 1001
    AdminBoot = 1002
    AdminShutdown = 1003
