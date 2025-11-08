from sqlalchemy import func
from datetime import date
from typing import List
from .base_repository import BaseRepository
from models.vacation_record import VacationRecord

class VacationRecordRepository(BaseRepository[VacationRecord]):
    def __init__(self, session):
        super().__init__(session, VacationRecord)

    def create_record(self, user_id: int,start_date: date,end_date: date, note: str = "") -> VacationRecord:
        days_count = (end_date - start_date).days + 1
        year = start_date.year

        record = VacationRecord(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            days_count=days_count,
            year=year,
            note=note
        )
        self.session.add(record)
        return record
    
    def get_used_days_in_year(self, user_id: int, year: int) -> int:
        result = (
            self.session.query(func.sum(VacationRecord.days_count))
            .filter(
                VacationRecord.user_id == user_id,
                VacationRecord.year == year
            )
            .scalar()
        )
        return result or 0
    
    def has_overlap(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> bool:
        query = self.session.query(VacationRecord).filter(
            VacationRecord.user_id == user_id,
            VacationRecord.start_date <= end_date,
            VacationRecord.end_date >= start_date
        )
        return query.first() is not None

    def get_by_date_range(
        self,
        user_id: int,
        from_date: date,
        to_date: date,
        page: int = 1,
        per_page: int = 20
    ) -> List[VacationRecord]:
        offset = (page - 1) * per_page
        return (
            self.session.query(VacationRecord)
            .filter(
                VacationRecord.user_id == user_id,
                VacationRecord.start_date >= from_date,
                VacationRecord.end_date <= to_date
            )
            .order_by(VacationRecord.start_date.desc())
            .offset(offset)
            .limit(per_page)
            .all()
        )