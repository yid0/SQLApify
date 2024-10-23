from .grant_strategy import GrantStrategy

class Grant:
    def __init__(self, strategy: GrantStrategy):
        self.strategy = strategy

    def generate_create_role(self, role_name: str) -> str:
        return self.strategy.create_role(role_name)

    def generate_grant_permissions(self, role_name: str, schema: str, database: str) -> str:
        return self.strategy.grant_permissions(role_name, schema, database)
