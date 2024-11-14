from fastapi import FastAPI
from config.logger import AppLogger
from middleware import LoggingMiddleware
from .routers  import user

app = FastAPI()
app.include_router(user.router)
logger = AppLogger("main").get_logger()

app.add_middleware(LoggingMiddleware)


@app.get("/status")
def status():
    logger.info("request /status")
    return {"status": "SQLApify is running"}
    
@app.on_event("startup")
def startup_event():
    """ Init user management"""
    try:
        from repository.setup import Setup
        from config import Configuration, ApplicationUserConfig
        from config.postgres import PostgresAdminConfig

        logger.info(f"***************** Starting SQLAPify {user.router.routes}*********************")
        print(f"{user.router.routes}")
        db_type  = ApplicationUserConfig.get_env(ApplicationUserConfig.APP_BUILD_TARGET.env_name)
                
        postgres_admin_config = Configuration(PostgresAdminConfig)
        postgres_admin_config.load()
        
        app_user_config = Configuration(ApplicationUserConfig)
        app_user_config_dict = app_user_config.load()
        
        setup_postgres_admin = Setup(db_type= db_type, config= postgres_admin_config)
        role_name = setup_postgres_admin.create_management_role(role_name=app_user_config_dict[ApplicationUserConfig.SQLAPIFY_DB_USER.alias], 
                                                                password=app_user_config_dict[ApplicationUserConfig.SQLAPIFY_DB_PASSWORD.alias])
        
        setup_postgres_admin.create_management_db(db_name=app_user_config_dict[ApplicationUserConfig.SQLAPIFY_DB_NAME.alias], role_name=role_name)
        setup_postgres_admin.reset_all()
        
    except Exception as e:
        raise Exception(f"{e}")