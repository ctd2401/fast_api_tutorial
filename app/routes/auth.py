from fastapi import APIRouter, Depends, HTTPException, status , Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from core.security import create_access_token, create_refresh_token, verify_password
from schemas.token import Token, RefreshTokenRequest
from models.user import User
from models.token import RefreshToken
from db.database import get_db
from schemas import user , token
router = APIRouter()

@router.post("/login", response_model=token.Token)
def login_user(request:Request,user_cred: user.UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == user_cred.email).first()
    if not user or not verify_password(user_cred.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token()

    expires_at = datetime.utcnow() + timedelta(days=7)
    token_entry = RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at,
    )
    
    client_ip = request.client.host

    db.add(token_entry)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "client_ip": client_ip
    }

@router.post("/refresh", response_model=Token)
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    stored_token = db.query(RefreshToken).filter(RefreshToken.token == data.refresh_token, RefreshToken.is_active == True).first()

    if not stored_token or stored_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = stored_token.user
    new_access = create_access_token(data={"sub": user.email})
    return {
        "access_token": new_access,
        "refresh_token": data.refresh_token  # reuse same refresh token
    }

@router.post("/logout")
def logout(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    token = db.query(RefreshToken).filter(RefreshToken.token == data.refresh_token).first()
    if not token:
        raise HTTPException(status_code=404, detail="Token not found")

    token.is_active = False
    db.commit()
    return {"message": "Logged out"}
