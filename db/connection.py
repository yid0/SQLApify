from db import Credential

class Connection:

    """
        Connection class for database connection statement
    """

    protocol: str 

    host: str

    port: str

    db_name : str

    credential: Credential

    def __init__(self, protocol: str, host: str, port: str, db_name: str, credential: Credential):

        self.protocol = protocol
        self.host = host
        self.port = port
        self.db_name = db_name
        self.credential = credential

    def url(self):
        return self

    def __str__(self):
        return f"{self.protocol}://{Credential.get_credential_str(self.credential)}@{self.host}:{self.port}/{self.db_name}"




