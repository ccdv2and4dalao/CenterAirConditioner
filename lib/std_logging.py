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
                 level=logging.NOTSET, filename=False, function=False, lineno=False):
        self.logger = logging.Logger(name=name, level=level)
        self.serializer = create_program_friendly_msg(
            2,
            filename=filename, function=function, lineno=lineno)

    def info(self, msg: str, args: dict):
        self.logger.info(self.serializer(msg, args))

    def warn(self, msg: str, args: dict):
        self.logger.warning(self.serializer(msg, args))

    def debug(self, msg: str, args: dict):
        self.logger.debug(self.serializer(msg, args))

    def error(self, msg: str, args: dict):
        self.logger.error(self.serializer(msg, args))

    def fatal(self, msg: str, args: dict):
        self.logger.critical(self.serializer(msg, args))


if __name__ == '__main__':
    logger = StdLoggerImpl(filename=True)
    logger.logger.addHandler(logging.StreamHandler())
    logger.info('233', {'a': 1, "b": 22})
