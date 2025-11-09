from typing import List
from pydantic import BaseModel
from .vacation_record_dto import VacationRecordDTO

class VacationListResponse(BaseModel):
    data: List[VacationRecordDTO]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool