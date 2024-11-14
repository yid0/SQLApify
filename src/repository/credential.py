from urllib.parse import quote

class Credential:

    username: str

    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_credential_str(self) -> str:
        return str(self)

    def __str__(self):
        if self.password:
            return f"{quote(self.username)}:{quote(self.password)}"
        return f"{quote(self.username)}"
