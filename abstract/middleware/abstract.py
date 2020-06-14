from abc import abstractmethod
from typing import Union

from abstract.service import Service
from proto import Response


class Middleware(object):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> Union[Response, None]:
        pass
