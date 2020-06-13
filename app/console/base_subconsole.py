from abstract.console import BaseSubConsole, MainConsole


class BaseSubConsoleImpl(BaseSubConsole):
    def __init__(self, inj):
        self.main_console = inj.require(MainConsole)

    def register(self, prefix):
        if type(prefix) is not str:
            prefix = prefix.value
        self.main_console.register(prefix, self)
