from typing import List


class OptionArgument:
    def __init__(self, long_opt: str, help_msg: str,
                 short_opt: str = None, default_value: str = None, convert=None):
        self.long_opt = long_opt
        self.short_opt = short_opt
        self.help_msg = help_msg
        self.default_value = default_value
        self.convert = convert


class OptionContext(object):
    def __init__(self):
        self.arguments = []  # type: List[OptionArgument]
        self.description = ''  # type: str
        self.option_args = None  # type: List[str] or None


option_context = OptionContext()
