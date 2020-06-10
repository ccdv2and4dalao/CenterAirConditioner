from abc import ABC

from abstract.middleware.abstract import Middleware


# aborted
class ReceiveRequestMiddleware(Middleware, ABC):
    pass
