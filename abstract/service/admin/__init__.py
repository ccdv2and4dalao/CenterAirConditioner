from .boot import AdminBootMasterService
from .generate_report import AdminGenerateReportService
from .get_connected_slaves import AdminGetConnectedSlavesService
from .get_server_status import AdminGetServerStatusService
from .get_slave_statistics import AdminGetSlaveStatisticsService
from .login import AdminLoginService
from .set_current_temperature import AdminSetCurrentTemperatureService
from .set_mode import AdminSetModeService
from .shutdown import AdminShutdownMasterService

__all__ = [
    'AdminBootMasterService',
    'AdminShutdownMasterService',
    'AdminLoginService',
    'AdminGenerateReportService',
    'AdminGetConnectedSlavesService',
    'AdminGetServerStatusService',
    'AdminGetSlaveStatisticsService',
    'AdminSetCurrentTemperatureService',
    'AdminSetModeService',
]
