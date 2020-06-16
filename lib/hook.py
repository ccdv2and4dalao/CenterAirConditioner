
class Hook:
    hook = {}

    @staticmethod
    def get_callee(event: str):
        return Hook.hook[event]

    @staticmethod
    def add_callee(event: str, callee_func):
        Hook.hook[event] = callee_func
