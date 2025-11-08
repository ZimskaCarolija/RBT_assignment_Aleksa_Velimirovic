from typing import Optional
from sqlalchemy.orm import Session
from models.vacation_entitlement import VacationEntitlement

class VacationEntitlementRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_user_year(self, user_id: int, year: int) -> Optional[VacationEntitlement]:
        return (
            self.session.query(VacationEntitlement)
            .filter(
                VacationEntitlement.user_id == user_id,
                VacationEntitlement.year == year
            )
            .first()
        )
    def create_vacation_entitlement(
            self,
            user_id: int,
            year: int,
            total_days: int
        ) -> VacationEntitlement:
            entitlement = VacationEntitlement(
                user_id=user_id,
                year=year,
                total_days=total_days
            )
            return entitlement