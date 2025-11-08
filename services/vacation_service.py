from datetime import date
from container import container
from dto import (
    VacationSummaryDTO,
    VacationRecordDTO,
    VacationListResponse,
    CheckOverlapResponse,
    CreateVacationRequest
)
import logging
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

class VacationService:
    def __init__(self):
        self.record_repo = container.record_repository
        self.entitlement_repo = container.entitlement_repository

    def get_vacation_summary(self, user_id: int, year: int | None = None) -> VacationSummaryDTO:
        if year is None:
            year = date.today().year

        entitlement = self.entitlement_repo.get_by_user_year(user_id, year)
        total_days = entitlement.total_days if entitlement else 0
        used_days = self.record_repo.get_used_days_in_year(user_id, year)
        available_days = max(0, total_days - used_days)

        return VacationSummaryDTO(
            total_days=total_days,
            used_days=used_days,
            available_days=available_days,
            year=year
        )

    def get_vacations_in_period(
        self,
        user_id: int,
        from_date: date,
        to_date: date,
        page: int = 1,
        per_page: int = 20
    ) -> VacationListResponse:
        records = self.record_repo.get_by_date_range(
            user_id=user_id,
            from_date=from_date,
            to_date=to_date,
            page=page,
            per_page=per_page
        )
        total = self.record_repo.count_by_date_range(user_id, from_date, to_date)
        data = [VacationRecordDTO.model_validate(r) for r in records]
        return VacationListResponse(
            data=data,
            total=total,
            page=page,
            per_page=per_page,
            has_next=(page * per_page) < total,
            has_prev=page > 1
        )

    def has_overlap_in_period(
        self,
        user_id: int,
        start_date: date,
        end_date: date
    ) -> CheckOverlapResponse:
        overlap = self.record_repo.has_overlap(user_id, start_date, end_date)
        message = "Overlap exists." if overlap else "The period is free."
        return CheckOverlapResponse(overlap=overlap, message=message)
    
    def create_vacation(
        self,
        user_id: int,
        data: CreateVacationRequest
    ) -> VacationRecordDTO:

        if self.record_repo.has_overlap(user_id, data.start_date, data.end_date):
            raise ValueError("There is already vacation in this time period")

        year = data.start_date.year
        summary = self.get_vacation_summary(user_id, year)
        days_needed = (data.end_date - data.start_date).days + 1

        if summary.available_days < days_needed:
            raise ValueError(
                f"You dont have enought days left: {days_needed}, "
                f"available: {summary.available_days}"
            )

        try:
            record = self.record_repo.create_record(
                user_id=user_id,
                start_date=data.start_date,
                end_date=data.end_date,
                note=data.note or ""
            )
            self.record_repo.session.flush()
            logger.info(f"vacation is created for user {user_id}: {data.start_date} - {data.end_date}")
            return VacationRecordDTO.model_validate(record)
        except IntegrityError as e:
            self.record_repo.session.rollback()
            logger.error(f"error while creating vacation : {e}")
            raise ValueError("error while creating vacation")