from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    client_ip: str = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str