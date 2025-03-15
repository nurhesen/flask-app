from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.config import SECRET_KEY, ALGORITHM
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_user(user: UserCreate):
    """
    Create a new user and return the user data.
    """
    db: Session = next(get_db())
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email already exists"
        )
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserOut.from_orm(new_user)


def authenticate_user(email: str, password: str):
    """
    Verify user's credentials and return a token if valid.
    """
    db: Session = next(get_db())
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    token_data = {"user_id": user.id}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token: str):
    """
    Verify token and return the associated user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            return None
    except jwt.PyJWTError:
        return None
    db: Session = next(get_db())
    user = db.query(User).filter(User.id == user_id).first()
    return user
