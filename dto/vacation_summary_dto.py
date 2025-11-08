from pydantic import BaseModel, Field, ConfigDict,field_validator

class VacationSummaryDTO(BaseModel):
    total_days: int = Field(..., ge=0)
    used_days: int = Field(..., ge=0)
    available_days: int = Field(..., ge=0)
    year: int = Field(..., ge=1900, le=2100)
    model_config = ConfigDict(from_attributes=True)

    @field_validator('available_days')
    def validate_available(cls, v, values):
        if 'total_days' in values and 'used_days' in values:
            if v != values['total_days'] - values['used_days']:
                raise ValueError("available_days must equal total_days minus used_days")
        return v