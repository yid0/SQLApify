from fastapi import APIRouter, HTTPException
from dto import CreateUserRoleDTO, BaseResponse
from service import DatabaseService
from config.logger import AppLogger

router = APIRouter(
    prefix="/user",
    tags=["user"],)

logger = AppLogger("router(/user)").get_logger()

@router.post("", response_model=BaseResponse)
async def create_user(dto: CreateUserRoleDTO):
    """HTTP endpoint for creating an application user that will interact with the DBMS."""
    try:
        logger.debug("Executng create_user method *** ")
        service = DatabaseService()
        await service.execute(dto)
        return BaseResponse(status_code=201, message="User created successfully.")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while creating the user.")