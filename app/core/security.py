from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import re
import os,secrets
from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_SECONDS = os.getenv('JWT_ACCESS_TOKEN_EXPIRATION_TIME')
REFRESH_TOKEN_EXPIRE_DAYS = os.getenv('JWT_REFRESH_TOKEN_EXPIRATION_TIME')

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def validate_password(password):
    ### atleast 1 special character , minimum 8 char and 1 letter
    pattern = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    match = re.match(pattern, password)
    return {
        "status":bool(match),
        "message":"Password must be at least 8 character,1 letter 1 number and 1 special character"
    }

def create_refresh_token():
    return secrets.token_urlsafe(32)

    
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(seconds=int(ACCESS_TOKEN_EXPIRE_SECONDS)))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)