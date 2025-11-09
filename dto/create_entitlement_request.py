from pydantic import BaseModel

class CreateEntitlementRequest(BaseModel):
    year: int
    total_days: int