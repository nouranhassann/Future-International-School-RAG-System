from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import LoginRequest, Token
from app.services.auth_service import get_user
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(request: LoginRequest):
    user = get_user(request.email)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user["email"], role=user["role"])
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}
