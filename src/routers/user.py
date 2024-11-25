from fastapi import APIRouter, HTTPException
from dto import CreateUserRoleDTO, BaseResponse
from service import DatabaseService
from config.logger import AppLogger

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

logger = AppLogger("UserController").get_logger()


@router.post("/", response_model=BaseResponse)
async def create_user(dto: CreateUserRoleDTO):
    """HTTP endpoint for creating an application user that will interact with the DBMS."""
    try:
        logger.info("Handle create_user method *** ")
        service = DatabaseService()
        service_response = await service.execute(dto)
        if service_response is not None:
            return BaseResponse(status_code=200, detail=f"{service_response}")
        else:
            return BaseResponse(status_code=400)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the user."
        )
