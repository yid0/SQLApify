from repository import Connection
from repository import Credential

class PostgresConnection(Connection):

    """
        Connection class for database connection statement for postgres
    """

    protocol: str = "postgresql"

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

    def url(self) -> str:
        return str(self)

    def __str__(self):
        return f"{self.protocol}://{self.credential}@{self.host}:{self.port}/{self.db_name}"