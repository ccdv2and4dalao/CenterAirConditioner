from typing import List, Union


class Injector:
    def __init__(self):
        self.mapping = dict()

    def provide(self, proto: Union[type, str, tuple], impl: object):
        if isinstance(proto, type) and not isinstance(impl, proto):
            raise NotImplementedError(f'impl {type(impl)} not implement proto {proto}')
        if proto in self.mapping:
            raise AssertionError(f'proto {proto} is already provided')
        self.mapping[proto] = impl

    def build(self, proto: type, impl: type):
        impl_instance = impl(self)
        if not isinstance(impl_instance, proto):
            raise NotImplementedError(f'impl {type(impl_instance)} not implement proto {proto}')
        if proto in self.mapping:
            raise AssertionError(f'proto {proto} is already provided')
        self.mapping[proto] = impl_instance

    def require(self, proto: Union[type, str, tuple]):
        return self.mapping[proto]

    def weak_require(self, proto: Union[type, str, tuple], default_value=None):
        return self.mapping.get(proto, default_value)

    def requires(self, prototypes: List[type]):
        return tuple([self.require(proto) for proto in prototypes])


if __name__ == '__main__':
    injector = Injector()
    # injector.provide(int, '')
    injector.provide(int, 1)
    print(injector.require(int))
