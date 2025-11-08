from typing import Optional
from repositories import RoleRepository


class Container:
    def __init__(self):
        self._db_session = None 
        self._role_repository: Optional[RoleRepository] = None

    def init_db(self, db_session):
        """Pozovi ovo iz app.py nakon db.init_app(app)"""
        self._db_session = db_session

    @property
    def role_repository(self) -> RoleRepository:
        if not self._role_repository and self._db_session:
            self._role_repository = RoleRepository(self._db_session)
        return self._role_repository

container = Container()