from flask import Blueprint, request
from flask_injector import inject
from services.user_service import UserService
from dto import CreateUserRequest, UpdateUserRequest
from utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['POST'])
@inject
def create_user(user_service: UserService):
    """
    POST /user
    { "email": "velimirovicaleksa001@gmail.com", "password": "aleksa123456", "full_name":"aleksa velimirovic"}
    """
    try:
        data = CreateUserRequest(**request.get_json())
        user = user_service.create_user(data)
        user_service.session.commit()
        return ApiResponse.success(user.model_dump(), 201)
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ApiResponse.error(str(e), 400)
    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)


@bp.route('/<int:user_id>', methods=['GET'])
@inject
def get_user(user_id: int, user_service: UserService):
    """
    GET /user/1
    """
    try:
        user = user_service.get_user(user_id)
        if not user:
            return ApiResponse.error("User not found", 404)
        return ApiResponse.success(user.model_dump(),201)
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)


@bp.route('', methods=['GET'])
@inject
def get_users(user_service: UserService):
    """
    GET /user?page=1?per_page=20
    """
    try:
        role = request.args.get('role')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        users = user_service.get_all_users(role_name=role, page=page, per_page=per_page)
        return ApiResponse.success([u.model_dump() for u in users],201)
    except Exception as e:
        logger.error(f"Error listing users: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)


@bp.route('/<int:user_id>', methods=['PATCH'])
@inject
def update_user(user_id: int, user_service: UserService):
    try:
        data = UpdateUserRequest(**request.get_json())
        user = user_service.update_user(user_id, data)
        user_service.session.commit()
        return ApiResponse.success(user.model_dump())
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ApiResponse.error(str(e), 400)
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)


@bp.route('/<int:user_id>', methods=['DELETE'])
@inject
def delete_user(user_id: int, user_service: UserService):
    try:
        user_service.soft_delete_user(user_id)
        return ApiResponse.success({"message": "User deleted"})
    except ValueError as e:
        return ApiResponse.error(str(e), 404)
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)