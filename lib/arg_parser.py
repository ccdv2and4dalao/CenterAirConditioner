import argparse

from abstract.component.option import OptionProvider
from abstract.singleton import OptionContext
from lib.injector import Injector


class StdArgParser(OptionProvider):

    def __init__(self, injector: Injector):
        self.option_context = injector.require(OptionContext)  # type: OptionContext
        self.parser = argparse.ArgumentParser(
            description=self.option_context.description)
        for option_argument in self.option_context.arguments:
            option_string = []
            if option_argument.long_opt:
                option_string.append('--' + option_argument.long_opt)
            if option_argument.short_opt:
                option_string.append('-' + option_argument.short_opt)

            self.parser.add_argument(
                *option_string,
                default=option_argument.default_value,
                help=option_argument.help_msg)

        self.namespace = self.parser.parse_args(self.option_context.option_args)

    def find(self, key: str) -> str:
        return getattr(self.namespace, key)
