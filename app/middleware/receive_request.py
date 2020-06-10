from abc import abstractmethod

from abstract.component import UUIDGenerator, Dispatcher
from abstract.middleware import ReceiveRequestMiddleware
from abstract.service import Service
from proto import Request, Response


class ReceiveRequestMiddlewareImpl(ReceiveRequestMiddleware):
    class ServiceFunc(Service):

        def __init__(self, fn, context_svc):
            self.serve_fn = fn
            self.context_svc = context_svc

        def serve(self, req: Request) -> Response:
            return self.serve_fn(self.context_svc, req)

    def __init__(self, inj):
        self.uuid_provider = inj.require(UUIDGenerator)  # type: UUIDGenerator
        self.dispatcher = inj.require(Dispatcher)  # type: Dispatcher
        self.dispatcher.on_pop(self.pop_request)
        self.dispatcher.on_fallback(self.fallback_request)

    def generate_tag(self) -> str:
        return self.uuid_provider.generate_uuid()

    def push_request(self, opaque: Request, tag: str) -> Response or None:
        return self.dispatcher.push(opaque, tag)

    @abstractmethod
    def pop_request(self, opaque: Request, tag: str) -> None:
        pass

    @abstractmethod
    def fallback_request(self, opaque: Request, tag: str) -> None:
        pass

    @abstractmethod
    def reply_receipt(self, tag: str) -> None:
        pass

    @abstractmethod
    def update_statistics(self, opaque: Request, tag: str) -> None:
        pass
