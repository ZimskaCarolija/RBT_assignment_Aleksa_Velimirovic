from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)
    full_name: Optional[str] = None
