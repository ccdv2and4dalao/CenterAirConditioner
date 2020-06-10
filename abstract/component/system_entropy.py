from abc import abstractmethod


class SystemEntropyProvider(object):

    @abstractmethod
    def get_entropy(self, entropy_len: int) -> str:
        pass
