from abc import abstractmethod


class JWT(object):

    @abstractmethod
    def authenticate(self, encoded: str) -> dict or Exception:
        pass

    @abstractmethod
    def create_jwt_token(self, payload: dict):
        pass

    @abstractmethod
    def decode_jwt_token(self, encoded: str) -> dict:
        pass
