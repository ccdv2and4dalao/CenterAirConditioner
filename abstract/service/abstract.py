from abc import abstractmethod

from proto import Request, Response


class Service(object):

    @abstractmethod
    def serve(self, req: Request) -> Response:
        pass
