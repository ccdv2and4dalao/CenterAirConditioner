from abc import abstractmethod


class UUIDGenerator(object):

    @abstractmethod
    def generate_uuid(self) -> str:
        pass
