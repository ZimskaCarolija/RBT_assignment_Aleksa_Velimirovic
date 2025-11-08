import base64
from typing import List, Optional
from .base_repository import BaseRepository
from models.user import User

class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(session, User)

    def is_admin(self, user_id: int) -> bool:
            user = self.get_by_id(user_id)
            if not user or not user.role:
                return False
            return user.role_id == 1

    def get_by_email_and_password_hash(
        self, email: str, password_hash: str
    ) -> Optional[User]:
        return (
            self.session.query(User)
            .filter(User.email == email)
            .filter(User.password_hash == password_hash)
            .first()
        )
