import jwt

from abstract.component import ConfigurationProvider
from abstract.component.jwt import JWT


class PyJWTImpl(JWT):
    def __init__(self, inj):
        self.cfg = inj.require(ConfigurationProvider)  # type: ConfigurationProvider
        self.algorithm = 'HS256'

        # HS256对称加密
        self.encode_key = self.cfg.get().admin_config.app_key
        self.decode_key = self.encode_key

    def authenticate(self, encoded: str) -> dict or Exception:
        try:
            return jwt.decode(encoded, self.decode_key, algorithm=self.algorithm)
        except Exception as e:
            return e

    def create_jwt_token(self, payload: dict):
        return jwt.encode(payload, self.encode_key, algorithm=self.algorithm).decode()

    def decode_jwt_token(self, encoded: str) -> dict:
        return jwt.decode(encoded, self.decode_key, algorithm=self.algorithm)
