from sqlalchemy.orm import Session
from models.user import User
from schemas.user import *
from core.security import *
from fastapi import HTTPException

def call_validate(password,user):
    if password is not None:
        validate_result = validate_password(password)
        if validate_result['status'] is not True:
            raise HTTPException(status_code=400, detail=validate_result['message'])
        user.password = get_password_hash(password)


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict())
    db.add(db_user)
    db.flush()  # Assigns an ID before commit
    db_user.introducer = db_user.id
    db_user.last_modifier = db_user.id
    call_validate(db_user.password,db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(User).all()


def update_user(db:Session,update_data:UserUpdate,current_user:User):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    fields = ['name','email','dob','phone_number','identity_number','gender']
    for field in fields:
        new_value = getattr(update_data, field, None)
        if new_value is not None:
            setattr(user, field, new_value)

    call_validate(update_data.password,user)

    db.commit()
    db.refresh(user)
    return update_data