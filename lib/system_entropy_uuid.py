from abstract.component import SystemEntropyProvider, UUIDGenerator


class SystemEntropyUUIDGeneratorImpl(UUIDGenerator):

    def __init__(self, inj):
        self.random_source = inj.require(SystemEntropyProvider)  # type: SystemEntropyProvider

    def generate_uuid(self) -> str:
        return self.random_source.get_entropy(64)
