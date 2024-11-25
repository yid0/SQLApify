from abc import ABC, abstractmethod
from repository import DbType
from config.logger import AppLogger
from repository import SQLStatementAdapter


class Query(ABC):
    db_type: DbType
    logger = AppLogger(name=None).get_logger()

    def __init__(self, session, engine, adapter: SQLStatementAdapter, scope=None):
        self.session = session
        self.adapter = adapter
        self.engine = engine
        self.scope = scope

    @abstractmethod
    def create(**kwargs) -> str:
        pass

    @abstractmethod
    def grant(self, db_role: str, db_name: str) -> bool:
        pass
