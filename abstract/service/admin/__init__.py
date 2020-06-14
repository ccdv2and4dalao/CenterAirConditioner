from .boot import AdminBootMasterService
from .generate_report import AdminGenerateReportService
from .get_connected_slaves import AdminGetConnectedSlavesService, AdminGetConnectedSlaveService
from .get_server_status import AdminGetServerStatusService
from .get_slave_statistics import AdminGetSlaveStatisticsService
from .login import AdminLoginService
from .set_current_temperature import AdminSetCurrentTemperatureService
from .set_mode import AdminSetModeService
from .shutdown import AdminShutdownMasterService
from .set_metric_delay import AdminSetMetricDelayService
from .set_update_delay import AdminSetUpdateDelayService

__all__ = [
    'AdminBootMasterService',
    'AdminShutdownMasterService',
    'AdminLoginService',
    'AdminGenerateReportService',
    'AdminGetConnectedSlavesService',
    'AdminGetConnectedSlaveService',
    'AdminGetServerStatusService',
    'AdminGetSlaveStatisticsService',
    'AdminSetCurrentTemperatureService',
    'AdminSetModeService',
    'AdminSetMetricDelayService',
    'AdminSetUpdateDelayService'
]
