from db.grant import GrantStrategy
class PostgresGrant(GrantStrategy):
    def create_role(self, role_name: str) -> str:
        return f"CREATE ROLE {role_name};"

    def grant_permissions(self, role_name: str, schema: str, database: str) -> str:
        return (
            f"GRANT CONNECT ON DATABASE {database} TO {role_name};\n"
            f"GRANT USAGE ON SCHEMA {schema} TO {role_name};\n"
            f"GRANT SELECT ON ALL TABLES IN SCHEMA {schema} TO {role_name};"
        )
