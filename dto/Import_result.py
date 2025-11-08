from typing import List, Dict, Any
from pydantic import BaseModel, Field

class ImportResult(BaseModel):
    success: bool = Field(..., description="Whether the import was successful")
    message: str = Field(..., description="Summary message")
    imported: int = Field(0, ge=0, description="Number of successfully imported users")
    errors: List[str] = Field(default_factory=list, description="List of error messages")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        from_attributes = True