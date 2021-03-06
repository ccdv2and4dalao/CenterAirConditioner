﻿from abc import abstractmethod

from .base_subconsole import BaseSubConsole


class BootConsole(BaseSubConsole):
    @abstractmethod
    def __call__(self, *args):
        pass
