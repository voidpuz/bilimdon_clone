from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class AuthRegistration(BaseModel):
    email: EmailStr
    password: str

class AuthRegistrationResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_staff: bool
    is_superuser: bool

class AuthLogin(BaseModel):
    email: str
    password: str

