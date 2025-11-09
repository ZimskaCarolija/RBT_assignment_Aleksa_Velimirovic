from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class CreateVacationRequest(BaseModel):
    start_date: date = Field(..., description="Vacation start date")
    end_date: date = Field(..., description="Vacation end date")
    note: Optional[str] = Field(None, max_length=500)

    def model_post_init(self, __context):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be after or same as start_date")