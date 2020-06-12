import inspect
import json
import logging
from logging import StreamHandler, FileHandler

from abstract.component import Logger

_ = StreamHandler
_ = FileHandler


def create_program_friendly_msg(skip: int = 1, filename=False, function=False, lineno=False):
    if filename or function or lineno:
        def serializer(msg: str, args: dict):
            caller = inspect.getouterframes(inspect.currentframe(), 2)[skip]  # type: inspect.FrameInfo
            args['_msg'] = msg
            if filename:
                args['_filename'] = caller.filename
            if function:
                args['_function'] = caller.function
            if lineno:
                args['_lineno'] = caller.lineno
            return json.dumps(args)
    else:
        def serializer(msg: str, args: dict):
            args['_msg'] = msg
            return json.dumps(args)
    return serializer


class StdLoggerImpl(Logger):

    def __init__(self, name='air_conditional',
                 level=logging.NOTSET, filename=True, function=True, lineno=True):
        self.logger = logging.Logger(name=name, level=level)
        self.serializer = create_program_friendly_msg(
            2,
            filename=filename, function=function, lineno=lineno)

    def info(self, msg: str, args: dict = None):
        self.logger.info(self.serializer(msg, args or {}))

    def warn(self, msg: str, args: dict = None):
        self.logger.warning(self.serializer(msg, args or {}))

    def debug(self, msg: str, args: dict = None):
        self.logger.debug(self.serializer(msg, args or {}))

    def error(self, msg: str, args: dict = None):
        self.logger.error(self.serializer(msg, args or {}))

    def fatal(self, msg: str, args: dict = None):
        self.logger.critical(self.serializer(msg, args or {}))


if __name__ == '__main__':
    logger = StdLoggerImpl(filename=True)
    logger.logger.addHandler(logging.StreamHandler())
    logger.info('233', {'a': 1, "b": 22})
