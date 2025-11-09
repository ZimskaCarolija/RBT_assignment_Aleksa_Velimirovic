from datetime import date
from pydantic import BaseModel, Field

class CheckOverlapRequest(BaseModel):
    start_date: date
    end_date: date

class CheckOverlapResponse(BaseModel):
    overlap: bool
    message: str = Field(..., max_length=200)