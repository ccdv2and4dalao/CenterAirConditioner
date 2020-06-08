from abc import abstractmethod


class Dispatcher:
    @abstractmethod
    def push(self, opaque, tag: str):
        pass

    @abstractmethod
    async def schedule(self):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def fallback(self):
        pass

    @abstractmethod
    def start_schedule(self):
        pass

    @abstractmethod
    def stop_schedule(self):
        pass

    @abstractmethod
    def register(self, exec_type: str, s, function):
        '''
        登记对应的处理方法: m[exec_type] = (s, function)
        s.function(opaque, tag)
        '''
        pass