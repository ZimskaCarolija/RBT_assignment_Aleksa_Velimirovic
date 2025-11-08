from datetime import date
from pydantic import BaseModel, Field, field_validator

class CheckOverlapRequest(BaseModel):
    start_date: date
    end_date: date

    @field_validator('end_date')
    def validate_dates(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError("end_date cannot be before start_date")
        return v

class CheckOverlapResponse(BaseModel):
    overlap: bool
    message: str = Field(..., max_length=200)