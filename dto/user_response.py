from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str]
    role_name: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

    @staticmethod
    def from_orm(user):
        return UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role_id=user.role_id,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
