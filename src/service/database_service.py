from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from abc import ABC
from src.repository.database_factory import DatabaseFactory
from repository.connection_factory import ConnectionFactory
from repository.query import QueryRole, QueryDb
from config.app_user_config import ApplicationUserConfig
from utils import get_env
from config.logger import AppLogger


class DatabaseService(ABC):
    _instance = None
    count = 0

    def __new__(cls, super_user=False):
        if cls._instance is None:
            instance = super(DatabaseService, cls).__new__(cls)
            cls.logger = AppLogger(instance.__class__.__name__).get_logger()
            cls.db_type = get_env(ApplicationUserConfig.APP_BUILD_TARGET.env_name)
            cls.super_user = super_user
            cls.scope = "super_user" if super_user else "app_user"
            cls._instance = instance
            cls.logger.debug(
                f"SINGLETON NEW DATABASE SERVICE INSTANCE: {id(cls._instance)}"
            )

        cls.logger.debug(
            f"SINGLETON EXISTING DATABASE SERVICE INSTANCE: {id(cls._instance)}"
        )
        return cls._instance

    def __init__(self, super_user=False):
        """Init the service by loading DB configurtaions and create the database object"""

        self.logger.info("initilize db connection")

        connection = ConnectionFactory.create_connection(
            db_type=self.db_type, scope=self.scope
        )

        self.logger.debug(f"CONNECTION STRING : [{connection}]")

        self.database = DatabaseFactory(
            db_type=get_env(ApplicationUserConfig.APP_BUILD_TARGET.env_name),
            connection=connection,
        ).database

    async def execute(self, dto):
        """Execute query based on the Data Object Transfer"""
        try:
            self.logger.debug(
                f"EXECUTE Query as user : [ {dto.username} , Query scope  : [{str(self.scope)} ]"
            )
            self.logger.debug(f"Query scope  : [{str(self.scope)}]")

            role_name = await self.create_role(
                role_name=dto.username, password=dto.password
            )

            if role_name:
                db_name = await self.create_db(
                    db_name=dto.database, role_name=dto.username
                )

                if db_name:
                    await self.grant_role_connection(
                        role_name=role_name, db_name=db_name
                    )
                    result = await self.grant_role(role_name)

                    if result and self.super_user:
                        result = await self.revoke_role(role_name=role_name)
                    return result

        except Exception as e:
            self.logger.error(f"ERROR: [{e}]")
            raise e

    async def create_role(self, role_name: str, password: str) -> Optional[str]:
        """Creates a role in the database with the specified name and password."""
        self.query = QueryRole(
            session=self.database.async_session,
            engine=self.database.engine,
            adapter=self.database.get_sql_adapter(),
            scope=self.scope,
        )

        self.logger.debug(f"EXECUTE Query : [{self.query}]")

        role_name = await self.query.create(role_name=role_name, password=password)
        self.logger.debug(f"CREATED OR EXISTING ROLE: [{role_name}]")
        return role_name

    async def create_db(self, db_name: str, role_name: str) -> Optional[str]:
        """Creates a database in the DBMS, with the specified role as the owner."""
        self.query: None
        self.query = QueryDb(
            session=self.database.async_session,
            engine=self.database.engine,
            adapter=self.database.get_sql_adapter(),
            scope=None,
        )
        db_name = await self.query.create(db_name=db_name, owner=role_name)
        return db_name

    async def grant_role(self, role_name: str) -> Optional[str]:
        """Grant a role in the database with the specified name."""
        return await self.query.grant(role_name)

    async def revoke_role(self, role_name: str) -> Optional[str]:
        """Revoke a role in with the specified name"""
        try:
            self.database.connect(mode="async")
            async with self.database.async_session() as session:
                sql_adapter = self.database.get_sql_adapter()
                query_role = QueryRole(
                    session=session, engine=self.database.engine, adapter=sql_adapter
                )
                return await query_role.revoke_permissions(role_name)

        except SQLAlchemyError as e:
            print(f"Error creating role {role_name}: {e}")
            raise Exception(f"{e}")

    async def grant_role_connection(
        self, role_name: str, db_name: str
    ) -> Optional[str]:
        """Grant a DB connection to role {role_name} in the database with the specified name."""
        self.query: None
        self.query = QueryRole(
            session=self.database.async_session,
            engine=self.database.engine,
            adapter=self.database.get_sql_adapter(),
            scope=self.scope,
        )

        return await self.query.grant_connection(role_name=role_name, db_name=db_name)
