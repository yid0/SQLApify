from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def read_items():
    return [{"item_name": "item1"}, {"item_name": "item2"}]