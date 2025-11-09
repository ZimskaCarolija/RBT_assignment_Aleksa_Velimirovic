from pydantic import BaseModel
from typing import Optional
class EntitlementDTO(BaseModel):
    user_id: int
    year: int
    total_days: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_orm(cls, obj):
        return cls(
            user_id=obj.user_id,
            year=obj.year,
            total_days=obj.total_days,
            created_at=obj.created_at.isoformat() if obj.created_at else None,
            updated_at=obj.updated_at.isoformat() if obj.updated_at else None
        )