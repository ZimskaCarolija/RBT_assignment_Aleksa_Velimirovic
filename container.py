from typing import Optional
from sqlalchemy.orm import Session
from repositories.role_repository import RoleRepository
from repositories.user_repository import UserRepository
from repositories.vacation_entitlement_repository import VacationEntitlementRepository
from repositories.vacation_record_repository import VacationRecordRepository


class Container:
    def __init__(self):
        self._db_session: Optional[Session] = None

        self._role_repository: Optional[RoleRepository] = None
        self._user_repository: Optional[UserRepository] = None
        self._entitlement_repository: Optional[VacationEntitlementRepository] = None
        self._record_repository: Optional[VacationRecordRepository] = None

    def init_db(self, db_session: Session):
        """Pozovi iz app.py ili testova"""
        self._db_session = db_session

    @property
    def role_repository(self) -> RoleRepository:
        if self._role_repository is None:
            self._role_repository = RoleRepository(self._db_session)
        return self._role_repository

    @property
    def user_repository(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = UserRepository(self._db_session)
        return self._user_repository

    @property
    def entitlement_repository(self) -> VacationEntitlementRepository:
        if self._entitlement_repository is None:
            self._entitlement_repository = VacationEntitlementRepository(self._db_session)
        return self._entitlement_repository

    @property
    def record_repository(self) -> VacationRecordRepository:
        if self._record_repository is None:
            self._record_repository = VacationRecordRepository(self._db_session)
        return self._record_repository

    def reset(self):
        self._db_session = None
        self._role_repository = None
        self._user_repository = None
        self._entitlement_repository = None
        self._record_repository = None


container = Container()