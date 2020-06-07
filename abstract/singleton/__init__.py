
from .context import *


def register_singletons(injector):
    option_context.description = injector.require('app_description')

    injector.provide(OptionContext, option_context)
    return injector
