from abc import abstractmethod, ABC

from abstract.middleware import ReceiveRequestMiddleware
from proto import Request, Response


class BaseReceiveRequestMiddlewareImpl(ReceiveRequestMiddleware, ABC):

    @abstractmethod
    def generate_tag(self) -> str:
        pass

    @abstractmethod
    def push_request(self, opaque: Request, tag: str) -> Response or None:
        pass

    @abstractmethod
    def pop_request(self, opaque: Request, tag: str) -> None:
        pass

    @abstractmethod
    def reply_receipt(self, tag: str) -> None:
        pass

    @abstractmethod
    def fallback_request(self, opaque: Request, tag: str) -> None:
        pass

    @abstractmethod
    def update_statistics(self, opaque: Request, tag: str) -> None:
        pass
