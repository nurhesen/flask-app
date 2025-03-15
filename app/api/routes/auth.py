from fastapi import APIRouter, HTTPException, status
from app.schemas import user as user_schema
from app.services import auth_service

router = APIRouter()


@router.post("/signup", response_model=user_schema.UserOut)
def signup(user: user_schema.UserCreate):
    created_user = auth_service.create_user(user)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Signup failed")
    return created_user


@router.post("/login")
def login(user: user_schema.UserLogin):
    token = auth_service.authenticate_user(user.email, user.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"token": token}
