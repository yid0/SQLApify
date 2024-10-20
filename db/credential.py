class Credential:

    username: str

    password: str

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def get_credential_str(self):
        return self

    def __str__(self):
        if self.password:
            return f"{self.username}:{self.password}"
        return f"{self.username}"
