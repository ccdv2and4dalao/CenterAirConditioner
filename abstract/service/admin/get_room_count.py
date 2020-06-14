from abc import abstractmethod, ABC

from abstract.service import Service
from proto import FailedResponse
from proto.admin.get_room_count import AdminGetRoomCountRequest, AdminGetRoomCountResponse


class AdminGetRoomCountService(Service, ABC):

    @abstractmethod
    def serve(self, req: AdminGetRoomCountRequest) -> AdminGetRoomCountResponse or FailedResponse:
        pass
