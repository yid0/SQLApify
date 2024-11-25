from repository import Connection
from repository import Credential
from config import Configuration


class PostgresConnection(Connection):
    """
    Connection class for database connection statement for postgres
    """

    protocol: str = "postgresql"

    host: str

    port: str

    db_name: str

    credential: Credential

    def __init__(
        self,
        protocol: str,
        host: str,
        port: str,
        db_name: str = None,
        credential: Credential = None,
    ):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.db_name = db_name
        self.credential = credential

    def url(self) -> str:
        return str(self)

    @classmethod
    def super_user(self) -> dict:
        superuser_config = Configuration.get_instance(key="postgres")
        env_vars = superuser_config.load()
        return PostgresConnection(
            protocol=env_vars["protocol"],
            host=env_vars["host"],
            port=env_vars["port"],
            db_name=env_vars["database"],
            credential=Credential(
                username=env_vars["username"], password=env_vars["password"]
            ),
        )

    @classmethod
    def app_user(self):
        app_user_config = Configuration.get_instance(key="application")
        env_vars = app_user_config.load()
        return PostgresConnection(
            protocol=self.super_user().protocol,
            host=self.super_user().host,
            port=self.super_user().port,
            db_name=env_vars["database"],
            credential=Credential(
                username=env_vars["username"], password=env_vars["password"]
            ),
        )

    @classmethod
    def management_user(self):
        return self.app_user()

    def __str__(self):
        return f"{self.protocol}://{self.credential}@{self.host}:{self.port}/{self.db_name}"
