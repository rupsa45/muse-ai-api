from fastapi import APIRouter, Depends
from models.user import UserCreate, UserLogin, UserResponse
from services.user_service import register_user, login_user, get_user_by_id
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from services.user_service import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/users", tags=["users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    return await register_user(user)


@router.post("/login")
async def login(user: UserLogin):
    return await login_user(user)


@router.get("/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return await get_user_by_id(user_id)
