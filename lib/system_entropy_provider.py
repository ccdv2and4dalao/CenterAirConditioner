import os

from abstract.component import SystemEntropyProvider


def get_entropy(entropy_len: int) -> str:
    if (entropy_len & 1) == 0:
        # 在linux上相当于读取/dev/random, 在windows上相当于调用CryptGenRandom
        return os.urandom(entropy_len >> 1).hex()
    raise ValueError(f'entropy_len should be even, got {entropy_len}')


class SystemEntropyProviderImpl(SystemEntropyProvider):

    # noinspection PyMethodMayBeStatic
    def get_entropy(self, entropy_len: int) -> str:
        return get_entropy(entropy_len)
