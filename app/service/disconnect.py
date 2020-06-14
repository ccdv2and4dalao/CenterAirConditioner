from abstract.model import EventModel
from abstract.service import DisConnectionService
from proto import FailedResponse
from proto.disconnect import DisConnectionRequest, DisConnectionResponse
from abstract.component import ConnectionPool

class DisConnectionServiceImpl(DisConnectionService):
    def __init__(self, inj):
        self.event_model = inj.require(EventModel) # type: EventModel
        self.connection_pool = inj.require(ConnectionPool)

    def serve(self, req: DisConnectionRequest) -> DisConnectionResponse or FailedResponse:
        self.event_model.insert_disconnect_event(req.room_id)
        self.connection_pool.delete(req.room_id)
        return DisConnectionResponse()