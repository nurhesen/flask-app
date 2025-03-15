from fastapi import Depends, HTTPException, status, Header
from app.services import auth_service


def get_current_user(token: str = Header(...)):
    """
    Check for a valid token.
    """
    user = auth_service.verify_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")
    return user
