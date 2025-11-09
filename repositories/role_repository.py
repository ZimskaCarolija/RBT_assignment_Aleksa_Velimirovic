from typing import Optional
from models.role import Role 
from sqlalchemy.orm import Session

class RoleRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_name(self, name: str) -> Optional[Role]:
        return self.session.query(Role).filter_by(name=name).first()

    def create(self, name: str) -> Role:
        role = Role(name=name)
        self.session.add(role)
        return role

    def get_all(self):
        return self.session.query(Role).all()