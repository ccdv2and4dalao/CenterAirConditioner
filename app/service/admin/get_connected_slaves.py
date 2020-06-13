from typing import List

from abstract.component import ConnectionPool
from abstract.model import RoomModel
from abstract.service.admin.get_connected_slaves import AdminGetConnectedSlavesService
from proto import FailedResponse
from proto.admin.get_connected_slaves import AdminGetConnectedSlavesRequest, AdminGetConnectedSlavesResponse, \
    AdminGetConnectedSlaveResponse


class AdminGetConnectedSlavesServiceImpl(AdminGetConnectedSlavesService):

    def __init__(self, inj):
        self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
        self.room_model = inj.require(RoomModel)  # type: RoomModel

    def serve(self, req: AdminGetConnectedSlavesRequest) -> AdminGetConnectedSlavesResponse or FailedResponse:
        rooms = self.room_model.query_page(req.page_size, req.page_number)  # type: List[any]
        for (i, room) in enumerate(rooms):
            conn = self.connection_pool.get(room.room_id)
            if conn is None:
                rooms[i] = AdminGetConnectedSlaveResponse(
                    inc_id=room.id,
                    room_id=room.room_id,
                    connected=False,
                ).__dict__
            else:
                rooms[i] = AdminGetConnectedSlaveResponse(
                    inc_id=room.id,
                    room_id=room.room_id,
                    connected=True,
                    current_temperature=conn.current_temperature,
                    need_fan=conn.need_fan,
                    fan_speed=conn.fan_speed,
                ).__dict__
        return AdminGetConnectedSlavesResponse(data=rooms)
