from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from repository import BaseDatabase
from .postgres_adapter import PostgresAdapter
from .postgres_connection import PostgresConnection
from .postgres_engine import PostgresEngine


class PostgresDatabase(BaseDatabase):
    _instance = None

    def __init__(self, connection: PostgresConnection):
        self.connection = connection
        self.url = self.get_connection_url()
        self.engine = PostgresEngine.get_engine(self.url)
        self.async_session = async_sessionmaker(
            bind=self.engine, expire_on_commit=False, class_=AsyncSession
        )

    def connect(self, mode="sync"):
        try:
            if mode == "async":
                return self.async_session
            else:
                raise NotImplementedError("Only async mode is currently supported.")
        except Exception as e:
            raise Exception(f"PostgreSQL Connection Error: {str(e)}")

    def get_connection_url(self) -> str:
        return self.connection.url()

    def get_sql_adapter(self) -> PostgresAdapter:
        return PostgresAdapter()

    async def dispose(self):
        """Dispose the database engine."""
        if self.engine:
            await self.engine.dispose()
