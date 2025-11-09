from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field
from pydantic import BaseModel, Field, ConfigDict

class VacationRecordDTO(BaseModel):
    id: int
    start_date: date
    end_date: date
    days_count: int = Field(..., ge=1)
    note: Optional[str] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True) 