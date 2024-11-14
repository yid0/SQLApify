from repository.grant import GrantStrategy

from sqlalchemy import text 
 
class PostgresGrant(GrantStrategy):    

    def grant_user_permissions(self, role_name: str, db_name: str) -> str:    
        
        return text(f"GRANT CONNECT ON DATABASE {db_name} TO {role_name}; \
                    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {role_name}; \
                    REVOKE ALL ON SCHEMA public FROM PUBLIC; \
                    GRANT USAGE ON SCHEMA public TO {role_name};")
