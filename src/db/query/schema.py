from sqlmodel import Session
from db import SQLStatementAdapter

class QuerySchema:
    def __init__(self, session: Session, adapter: SQLStatementAdapter):
        self.session = session
        self.adapter = adapter

    def create_schema(self, schema_name: str):
        query = self.adapter.create_schema_statement(schema_name)
        self.session.execute(query)
        self.session.commit()
        self.session.close()
        print(f"Schéma {schema_name} créé avec succès.")
