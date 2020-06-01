from abc import abstractmethod

from proto import Request, Response


class ReceiveRequestService(object):

    def receive_request(self, request: Request) -> Response:
        pass
