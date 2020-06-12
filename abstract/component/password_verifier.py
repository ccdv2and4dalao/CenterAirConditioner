from abc import abstractmethod


class PasswordVerifier(object):
    @abstractmethod
    def create(self, raw_password: str) -> str:
        pass

    @abstractmethod
    def verify(self, raw_password: str, encrypted_password: str) -> bool:
        pass
