from typing import List, Union

from abstract.component import ConnectionPool
from abstract.model import RoomModel, Room
from abstract.service.admin.get_connected_slaves import AdminGetConnectedSlavesService, AdminGetConnectedSlaveService
from proto import FailedResponse, MasterAirCondNotAlive
from proto.admin.get_connected_slaves import AdminGetConnectedSlavesRequest, AdminGetConnectedSlavesResponse, \
    AdminGetConnectedSlaveResponseItem, AdminGetConnectedSlaveResponse, AdminGetConnectedSlaveRequest
from abstract.component import MasterAirCond


class BasicAdminGetConnectedSlaveServiceImpl(object):

    def __init__(self, inj):
        self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
        self.room_model = inj.require(RoomModel)  # type: RoomModel
        self.master_air_cond = inj.require(MasterAirCond)  # type: MasterAirCond

    def query(self, room: Room):
        conn = self.connection_pool.get(room.id)
        if conn is None:
            return AdminGetConnectedSlaveResponseItem(
                inc_id=room.id,
                room_id=room.room_id,
                connected=False,
            ).__dict__
        return AdminGetConnectedSlaveResponseItem(
            inc_id=room.id,
            room_id=room.room_id,
            connected=True,
            current_temperature=conn.current_temperature,
            need_fan=conn.need_fan,
            fan_speed=conn.fan_speed,
        ).__dict__


class AdminGetConnectedSlaveServiceImpl(BasicAdminGetConnectedSlaveServiceImpl, AdminGetConnectedSlaveService):

    def serve(self, req: AdminGetConnectedSlaveRequest) -> AdminGetConnectedSlaveResponse or FailedResponse:
        if not self.master_air_cond.is_boot:
            return MasterAirCondNotAlive("master aircon is off")
        room = self.room_model.query_by_id(req.inc_id)  # type: Union[dict, Room]
        return AdminGetConnectedSlaveResponse(item=self.query(room))


class AdminGetConnectedSlavesServiceImpl(BasicAdminGetConnectedSlaveServiceImpl, AdminGetConnectedSlavesService):

    def serve(self, req: AdminGetConnectedSlavesRequest) -> AdminGetConnectedSlavesResponse or FailedResponse:
        if not self.master_air_cond.is_boot:
            return MasterAirCondNotAlive("master aircon is off")
        rooms = self.room_model.query_page(req.page_size, req.page_number)  # type: List[Union[dict, Room]]
        for (i, room) in enumerate(rooms):
            rooms[i] = self.query(room)
        return AdminGetConnectedSlavesResponse(data=rooms)
