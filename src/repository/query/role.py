from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text
from typing import Optional
from repository import SQLStatementAdapter
from .query import Query

# TODO: Fix logger


class QueryRole(Query):
    """
    Class to handle role-related queries in the database.
    """

    def __init__(
        self,
        session: AsyncSession,
        engine,
        adapter: SQLStatementAdapter,
        scope="app_user",
    ):
        """
        Initialize QueryRole with a session and SQL statement adapter.
        Args:
            session (Session): SQLModel session object.
            adapter (SQLStatementAdapter): Adapter to generate SQL statements.
        """

        super().__init__(session=session, engine=engine, adapter=adapter, scope=scope)
        self.logger.name = self.__class__.__name__

    async def create(self, role_name: str, password: str) -> Optional[str]:
        """
        Create a role in the database with the specified name and password.

        Args:
            role_name (str): The name of the role to create.
            password (str): The password for the role.

        Returns:
            bool: True if the role was created successfully, False otherwise.
        """
        try:
            async with self.engine.connect() as connection:
                self.logger.debug(f"CONNECTION OBJ ID: {str(id(connection))}")
                check_role_exists: False

                self.logger.debug(f"QUERY REQUEST FOR: {str(role_name)} role")
                check_role_exists = await connection.execute(
                    text(self.adapter.check_role_exists(role_name=role_name))
                )
                exist_role = check_role_exists.scalars()

                if role_name in list(exist_role):
                    self.logger.debug(f"CHECK ROLE EXISTANCE: {str(exist_role)}")
                    return
                else:
                    query = self.adapter.create_role_statement(role_name, password)
                    await connection.execute(query)
                    await connection.commit()
                    self.logger.info(f"Role '{role_name}' was created successfully.")
                return role_name
        except ProgrammingError as e:
            error_message = str(e.__cause__)
            if "exists" in error_message:
                self.logger.debug(f"ERROR ProgrammingError: {error_message}")
                return role_name
        except Exception as e:
            error_message = str(e.__cause__) if e.__cause__ else str(e)
            self.logger.debug(f"ERROR: {e}")
            return None

        finally:
            await self.engine.dispose()
            return role_name

    async def grant(self, role_name: str, schema: str = "public") -> bool:
        self.logger.info(f"GRANT permissions to role {role_name}")
        try:
            async with self.engine.connect() as connection:
                self.logger.debug(f"CONNECTION OBJ ID: {str(id(connection))}")
                async with connection.begin():
                    queries = self.adapter.grant_role(role_name, self.scope, schema)
                    for query in queries:
                        await connection.execute(query)
                    if self.scope == "super_user":
                        super_admin_grant = (
                            self.adapter.grant_role_tmp_permissions_statement(
                                role_name=role_name
                            )
                        )
                        for query in super_admin_grant:
                            await connection.execute(query)
                await connection.close()
            self.logger.info(f"GRANTED permissions role: {role_name}.")
            return True
        except ProgrammingError as e:
            error_message = str(e.__cause__)
            if "exists" in error_message:
                print(f"ERROR: {error_message}")
                return False
            self.logger.debug(f"ERROR ProgrammingError: {error_message}")
        except Exception as e:
            error_message = str(e.__cause__) if e.__cause__ else str(e)
            self.logger.debug(f"ERROR: {e}")
            raise e
        finally:
            await self.engine.dispose()
            return role_name

    async def grant_connection(self, role_name: str, db_name: str) -> bool:
        print(f"GRANT grant_connection to role {role_name} on {db_name} db.")
        try:
            async with self.engine.connect() as connection:
                self.logger.debug(f"CONNECTION OBJ ID: {str(id(connection))}")
                query = self.adapter.grant_role_connection(role_name, db_name)
                await connection.execute(query)
                await connection.commit()
                print(f"GRANTED permissions role'{role_name}'.")
                return True
        except ProgrammingError as e:
            error_message = str(e.__cause__)
            print(f"ProgrammingError: {error_message}")
        except Exception as e:
            error_message = str(e.__cause__) if e.__cause__ else str(e)
            self.logger.error(f"ERROR: {error_message}")
        finally:
            await self.engine.dispose()

    async def revoke_permissions(self, role_name: str) -> bool:
        print(f"REVOKE permissions to role {role_name}.")
        try:
            async with self.engine.connect() as connection:
                queries = self.adapter.revoke_permissions(role_name)
                for query in queries:
                    await connection.execute(query)
                    await connection.commit()
                    print(f"REVOKED permissions role'{role_name}'.")
                return True
        except ProgrammingError as e:
            error_message = str(e.__cause__)
            print(f"ERROR: {error_message}")
            return False
        except Exception as e:
            error_message = str(e.__cause__) if e.__cause__ else str(e)
            print(f"ERROR: {error_message}")
            raise e
        finally:
            await self.engine.dispose()
