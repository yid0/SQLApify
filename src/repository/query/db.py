from sqlalchemy import text
from typing import Optional
from repository import SQLStatementAdapter
from .query import Query


class QueryDb(Query):
    """
    Class to handle database-related queries in the database management system.
    """

    def __init__(self, session, engine, adapter: SQLStatementAdapter, scope="app_user"):
        """
        Initialize QueryDb with a session and SQL statement adapter.

        Args:
            session (Session): SQLModel session object.
            adapter (SQLStatementAdapter): Adapter to generate SQL statements.
        """
        super().__init__(session=session, engine=engine, adapter=adapter, scope=scope)
        self.logger.name = self.__class__.__name__

    async def create(self, db_name: str, owner: str) -> Optional[str]:
        """
        Create a database in the DBMS with the specified name and owner.

        Args:
            db_name (str): The name of the database to create.
            owner (str): The owner of the new database.

        Returns:
            bool: True if the database was created successfully, False otherwise.
        """
        try:
            async with self.engine.connect() as connection:
                self.logger.debug(f"CONNECTION OBJ ID: {str(id(connection))}")
                await connection.execution_options(isolation_level="AUTOCOMMIT")

                result = await connection.execute(
                    text(self.adapter.check_db_exists(db_name))
                )
                exists = result.scalars()
                if 1 in exists:
                    self.logger.debug(f"DB '{db_name}' already exists.")
                    return db_name
                else:
                    query = self.adapter.create_db_statement(db_name, owner)
                    await connection.execute(text(query))
                    self.logger.info(f"DB '{db_name}' was created successfully.")
                return db_name
        except Exception as e:
            error_message = str(e.__cause__) if e.__cause__ else str(e)
            if "exists" in error_message:
                self.logger.error(f"ERROR ProgrammingError: {error_message}")
                return db_name
        finally:
            await self.engine.dispose()

    def grant():
        pass
