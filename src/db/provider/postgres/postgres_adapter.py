from sqlalchemy import text 

from db.statement_adapter import SQLStatementAdapter

class PostgresAdapter(SQLStatementAdapter):
    
    def create_schema_statement(self, schema_name: str) -> str:
        return text(f"CREATE SCHEMA IF NOT EXISTS {schema_name};")

    def create_user_statement(self, username: str, password: str) -> str:
        return text(f"CREATE USER {username} WITH PASSWORD '{password}';")

    def create_role_statement(self, role_name: str) -> str:
        return text(f"CREATE ROLE {role_name};")
    
