from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
import uvloop
import sys
import asyncio
from .service import DatabaseService
from config.logger import AppLogger
from .routers import user
from utils import JsonObject


@asynccontextmanager
async def lifespans(app: FastAPI):
    """background task starts at statrup"""
    await asyncio.create_task(init_app_user())
    yield


app = FastAPI(lifespan=lifespans)
app.include_router(user.router)
logger = AppLogger("MAIN").get_logger()

# app.add_middleware(LoggingMiddleware)


@app.get("/status")
def status():
    logger.info("request /status")
    return {"status": "SQLApify is running"}


# @app.on_event("startup")
# def startup_event():
#     pass


async def init_app_user():
    """Init user management"""
    role_name: str = None
    try:
        from config import Configuration

        logger.info("***************** Starting SQLAPify *********************")
        app_user_config = Configuration.get_instance(key="application")
        app_config_dict = app_user_config.load()

        logger.debug(f"APP CONFIG: {app_config_dict}")

        database_service = DatabaseService(super_user=True)

        data = JsonObject(
            {
                "username": app_config_dict["username"],
                "password": app_config_dict["password"],
                "database": app_config_dict["database"],
            }
        )

        await database_service.execute(dto=data)

        logger.info("Setup Finished")
    except Exception as e:
        logger.info(f"EXCEPTION: {str(role_name)}")
        raise Exception(f"Setup {e}")


def main():
    server = uvicorn.Server()
    server.serve()


if __name__ == "__main__":
    if sys.version_info >= (3, 10):
        with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
            runner.run(main())
    else:
        uvloop.install()
        asyncio.run(main())
