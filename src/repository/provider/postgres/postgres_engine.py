from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from typing import Optional
from repository.engine import Engine


class PostgresEngine(Engine):
    _engine: Optional[AsyncEngine] = None

    @classmethod
    def get_engine(self, connection_url: str) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(
                connection_url, echo=True, pool_pre_ping=True, future=True
            )
        return self._engine

    @classmethod
    async def dispose_engine(self):
        if self._engine:
            await self._engine.dispose()
            self._engine = None
