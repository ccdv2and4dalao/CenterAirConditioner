from abstract.component import MasterAirCond, Dispatcher
from abstract.service.admin.get_server_status import AdminGetServerStatusService
from proto import FailedResponse
from proto.admin.get_server_status import AdminGetServerStatusRequest, AdminGetServerStatusResponse, ServerState


class AdminGetServerStatusServiceImpl(AdminGetServerStatusService):
    def __init__(self, inj):
        self.dispatcher = inj.require(Dispatcher)  # type: Dispatcher
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def serve(self, req: AdminGetServerStatusRequest) -> AdminGetServerStatusResponse or FailedResponse:
        resp = AdminGetServerStatusResponse()
        resp.mode, resp.current_temperature = self.master_air_cond.get_md_pair()
        resp.mode = resp.mode.value
        resp.update_delay, resp.metric_delay = self.master_air_cond.get_delay_pair()
        resp.is_boot = self.master_air_cond.is_boot
        if self.dispatcher.is_idle():
            resp.work_state = ServerState.Idle.value
        else:
            resp.work_state = ServerState.Working.value

        return resp
