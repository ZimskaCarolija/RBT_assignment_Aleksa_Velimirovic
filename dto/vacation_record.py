from pydantic import BaseModel
from datetime import date
from typing import Optional
class VacationRecordDTO(BaseModel):
    id: int
    start_date: date
    end_date: date
    days_count: int
    year: int
    note: Optional[str]

    class Config:
        from_attributes = True