from sqlmodel import Session
from db import SQLStatementAdapter

class QueryRole:
    def __init__(self, session: Session, adapter: SQLStatementAdapter):
        self.session = session
        self.adapter = adapter

    def create_role(self, role_name: str):
        query = self.adapter.create_role_statement(role_name)
        self.session.execute(query)
        self.session.commit()
        self.session.close()
        print(f"Rôle {role_name} créé avec succès.")
