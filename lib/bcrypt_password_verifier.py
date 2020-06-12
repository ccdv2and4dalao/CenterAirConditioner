import bcrypt

from abstract.component import ConfigurationProvider
from abstract.component.password_verifier import PasswordVerifier


class BCryptPasswordVerifier(PasswordVerifier):

    def __init__(self, inj):
        self.cfg_provider = inj.require(ConfigurationProvider)  # type: ConfigurationProvider

    def create(self, raw_password: str) -> str:
        return bcrypt.hashpw(raw_password.encode(), self.cfg_provider.get().server_config.bcrypt_salt).decode()

    def verify(self, raw_password: str, encrypted_password: str) -> bool:
        return bcrypt.checkpw(raw_password.encode(), encrypted_password.encode())
