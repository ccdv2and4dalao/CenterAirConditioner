from typing import List


class Injector:
    def __init__(self):
        self.mapping = dict()

    def provide(self, proto: type, impl: object):
        if not isinstance(impl, proto):
            raise NotImplementedError(f'impl {type(impl)} not implement proto {proto}')
        if proto in self.mapping:
            raise AssertionError(f'proto {proto} is already provided')
        self.mapping[proto] = impl

    def require(self, proto: type):
        return self.mapping[proto]

    def requires(self, prototypes: List[type]):
        return tuple([self.require(proto) for proto in prototypes])


if __name__ == '__main__':
    injector = Injector()
    # injector.provide(int, '')
    injector.provide(int, 1)
    print(injector.require(int))
