from abstract.model import RoomModel
from abstract.service.admin.get_room_count import AdminGetRoomCountService
from proto.admin.get_room_count import AdminGetRoomCountRequest, AdminGetRoomCountResponse


class AdminGetRoomCountServiceImpl(AdminGetRoomCountService):
    def __init__(self, inj):
        self.room_model = inj.require(RoomModel)  # type: RoomModel
        pass

    def serve(self, req: AdminGetRoomCountRequest) -> AdminGetRoomCountResponse:
        return AdminGetRoomCountResponse(self.room_model.query_total_count())
