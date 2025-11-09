from pydantic import BaseModel, Field, ConfigDict,field_validator

class VacationSummaryDTO(BaseModel):
    total_days: int 
    used_days: int 
    available_days: int = Field(..., ge=0)
    year: int = Field(..., ge=1900, le=2100)
    model_config = ConfigDict(from_attributes=True)
