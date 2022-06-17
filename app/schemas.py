from datetime import datetime
import email
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    # name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class config:
        orm_mode = True


class UserLogin(BaseModel):
    # name: str
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None