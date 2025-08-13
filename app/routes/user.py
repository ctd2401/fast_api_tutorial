from fastapi import APIRouter, HTTPException, Depends, status, Request
from sqlalchemy.orm import Session
from db.database import get_db

from crud import user as crud_user
from schemas import user as schema_user
from models.user import User
from core.security import verify_password, create_access_token
from core.deps import *

router = APIRouter()


@router.get("/my_ip")
async def ip(request: Request, current_user: User = Depends(get_current_user)):
    client_ip = request.client.host
    return {"client_ip": client_ip}


@router.post("/create/", response_model=schema_user.UserOut)
def create_user(user: schema_user.UserCreate, db: Session = Depends(get_db)):
    return crud_user.create_user(db, user)


@router.put("/update/", response_model=schema_user.UserOut)
def update_user(
    update_data: schema_user.UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return crud_user.update_user(db, update_data, current_user)


@router.get("/me/", response_model=list[schema_user.UserOut])
def read_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return crud_user.get_users(db)
