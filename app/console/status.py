from abstract.console import StatusConsole
from app.console.base_subconsole import BaseSubConsoleImpl
from abstract.consensus import ConsolePrefix
from abstract.service.admin import AdminGetServerStatusService
from proto.admin.get_server_status import AdminGetServerStatusRequest, AdminGetServerStatusResponse

class StatusConsoleImpl(StatusConsole, BaseSubConsoleImpl):
    def __init__(self, inj):
        super().__init__(inj)
        self.register(ConsolePrefix.status)
        self.server_status_service = inj.require(AdminGetServerStatusService)

    def __call__(self, *args):
        r = AdminGetServerStatusRequest()
        ret = self.server_status_service.serve(r)
        if type(ret) is AdminGetServerStatusResponse:
            print('Server Status:\n')
            print(f'\tmode: {ret.mode}')
            print(f'\twork state: {ret.work_state}')
            print(f'\tcurrent temperature: {ret.current_temperature}')
            print(f'\tmetric delay: {ret.metric_delay}')
            print(f'\tupdate delay: {ret.update_delay}')
