from fastapi import  APIRouter

router = APIRouter()# If we used FastAPI, it would be an instance of FastAPI, but here we use APIRouter to
# create a router for the auth endpoints. This allows us to group related endpoints together


@router.get("/auth")
async def get_user():
    return {'user':'authenticated'}