from sqlalchemy import text
from repository.statement_adapter import SQLStatementAdapter


class PostgresAdapter(SQLStatementAdapter):
    queries: set

    def __init__(self):
        self.queries = set()

    def check_role_exists(self, role_name):
        code = QueryCode.qc1()(role_name=role_name)
        print(f"SQL CODE TO BE EXECUTED: {code}")
        return code

    def check_db_exists(self, db_name):
        code = QueryCode.qc2()(db_name=db_name)
        print(f"SQL CODE TO BE EXECUTED: {code}")
        return code

    def create_db_statement(self, db_name: str, owner: str):
        code = QueryCode.qc0()(db_name, owner)
        print(f"SQL CODE TO BE EXECUTED: {code}")
        return code

    def create_schema_statement(self, schema_name: str) -> str:
        return text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")

    def create_user_statement(self, username: str, password: str) -> str:
        return text(f"CREATE USER {username} WITH PASSWORD '{password}';")

    def create_role_statement(self, role_name: str, user_password: str) -> str:
        return text(f"CREATE ROLE {role_name} WITH LOGIN PASSWORD '{user_password}';")

    def grant_role_tmp_permissions_statement(self, role_name):
        return [
            text(f"ALTER ROLE {role_name} WITH CREATEDB;"),
            text(f"ALTER ROLE {role_name} WITH CREATEROLE;"),
        ]

    def grant_role(self, role_name: str, scope: str, schema: str = "public") -> str:
        queries = [
            text(
                f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {schema} TO {role_name};"
            ),
            text(f"REVOKE ALL ON SCHEMA {schema} FROM PUBLIC;"),
            text(f"GRANT USAGE ON SCHEMA {schema} TO {role_name};"),
        ]

        return queries

    def grant_role_connection(self, role_name: str, db_name: str):
        return text(f"GRANT CONNECT ON DATABASE {db_name} TO {role_name};")

    def revoke(self, role_name: str, db_name: str, schema: str = "public") -> str:
        return text(f"GRANT CONNECT ON DATABASE {db_name} TO {role_name}; \
                    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {schema} TO {role_name}; \
                    REVOKE ALL ON SCHEMA {schema} FROM PUBLIC; \
                    GRANT USAGE ON SCHEMA {schema} TO {role_name}; \
                    ALTER ROLE {role_name} WITH CREATEDB; \
                    ALTER ROLE {role_name} WITH CREATEROLE;")

    def revoke_permissions(self, role_name):
        return [
            text(f"ALTER ROLE {role_name} WITH NOCREATEDB;"),
            text(f"ALTER ROLE {role_name} WITH NOCREATEROLE;"),
        ]


class QueryCode:
    @classmethod
    def __get_attr(kwagrs, attr: str):
        return kwagrs["kwargs"][attr]

    """
        CREATE A NEW DATABASE
    """

    @classmethod
    def qc0(*kwagrs):
        return lambda table_name, owner: f"CREATE DATABASE {table_name} OWNER '{owner}'"

    @classmethod
    def qc1(*kwagrs):
        return lambda role_name: f"SELECT 1 FROM pg_roles WHERE rolname = '{role_name}'"

    @classmethod
    def qc2(*kwagrs):
        return lambda db_name: f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"
