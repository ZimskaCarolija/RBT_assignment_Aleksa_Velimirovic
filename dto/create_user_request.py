from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CreateUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: Optional[str] = None
