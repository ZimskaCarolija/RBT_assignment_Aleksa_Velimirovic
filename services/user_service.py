from typing import Optional, List
from sqlalchemy.orm import Session
from models.user import User
from models.role import Role
from repositories.user_repository import UserRepository
from repositories.role_repository import RoleRepository
from dto import CreateUserRequest, UpdateUserRequest, UserResponse
from utils.password import hash_password
from datetime import datetime, timezone
from constants import RoleNames
import logging

logger = logging.getLogger(__name__)

class UserService:

    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository):
        self.user_repo = user_repo
        self.role_repo = role_repo
        self.session = user_repo.session

    def _ensure_employee_role(self) -> Role:
        role = self.role_repo.get_by_name(RoleNames.EMPLOYEE)
        if not role:
            role = self.role_repo.create(RoleNames.EMPLOYEE)
            self.session.flush()
            logger.info(f"Created default '{RoleNames.EMPLOYEE}' role")
        return role

    def create_user(self, data: CreateUserRequest) -> UserResponse:
        if self.user_repo.get_by_email(data.email):
            raise ValueError("Email already in use")

        employee_role = self._ensure_employee_role()
        password_hash = hash_password(data.password)

        user = User(
            email=data.email,
            password=password_hash,
            full_name=data.full_name,
            role_id=employee_role.id
        )
        self.session.add(user)
        self.session.flush()

        logger.info(f"Created user: {user.email} (ID: {user.id})")
        return UserResponse.from_orm(user)

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = self.user_repo.get_by_id(user_id)
        if not user or user.deleted_at:
            return None
        return UserResponse.from_orm(user)

    def get_all_users(
        self,
        role_name: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> List[UserResponse]:
        query = self.session.query(User).filter(User.deleted_at.is_(None))
        if role_name:
            query = query.join(Role).filter(Role.name == role_name)
        offset = (page - 1) * per_page
        users = query.offset(offset).limit(per_page).all()
        return [UserResponse.from_orm(u) for u in users]

    def update_user(self, user_id: int, data: UpdateUserRequest) -> UserResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user or user.deleted_at:
            raise ValueError("User not found")

        if data.email and data.email != user.email:
            if self.user_repo.get_by_email(data.email):
                raise ValueError("Email already in use")
            user.email = data.email

        if data.full_name:
            user.full_name = data.full_name

        if data.password:
            user.password_hash = hash_password(data.password)

        user.updated_at = datetime.now(timezone.utc)
        self.session.flush()

        logger.info(f"Updated user: {user.id}")
        return UserResponse.from_orm(user)

    def soft_delete_user(self, user_id: int) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user or user.deleted_at:
            raise ValueError("User not found")

        self.user_repo.soft_delete(user)
        self.session.flush()
        logger.info(f"Soft deleted user: {user.id}")