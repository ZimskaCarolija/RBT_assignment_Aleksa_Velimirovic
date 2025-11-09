from models import db
from flask_injector import FlaskInjector
from injector import singleton


from repositories.user_repository import UserRepository
from repositories.role_repository import RoleRepository
from repositories.vacation_record_repository import VacationRecordRepository
from repositories.vacation_entitlement_repository import VacationEntitlementRepository


from services.user_service import UserService
from services.vacation_service import VacationService
from services.import_service import ImportService

class Container:
    def __init__(self,db_session):
        self.db_session = db_session

        self.user_repository = UserRepository(self.db_session)
        self.role_repository = RoleRepository(self.db_session)
        self.vacation_record_repository = VacationRecordRepository(self.db_session)
        self.vacation_entitlement_repository = VacationEntitlementRepository(self.db_session)

        self.user_service = UserService(
            user_repo=self.user_repository,
            role_repo=self.role_repository
        )
        self.vacation_service = VacationService(
            record_repo=self.vacation_record_repository,
            entitlement_repo=self.vacation_entitlement_repository
        )

        self.import_service = ImportService(
            session=self.db_session,
            user_service=self.user_service,
            vacation_service=self.vacation_service,
            user_repository=self.user_repository,
            vacation_record_repository=self.vacation_record_repository,
            vacation_entitlement_repository=self.vacation_entitlement_repository
        )

    def bind_services(self, binder):
        binder.bind(UserService, to=self.user_service, scope=singleton)
        binder.bind(VacationService, to=self.vacation_service, scope=singleton)
        binder.bind(ImportService, to=self.import_service, scope=singleton)
        binder.bind(UserRepository, to=self.user_repository, scope=singleton)
        binder.bind(RoleRepository, to=self.role_repository, scope=singleton)
        binder.bind(VacationRecordRepository, to=self.vacation_record_repository, scope=singleton)
        binder.bind(VacationEntitlementRepository, to=self.vacation_entitlement_repository, scope=singleton)
