from flask import Blueprint, request, jsonify
from container import container
from dto import CreateUserRequest, UpdateUserRequest
from utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['POST'])
def create_user():
    try:
        data = CreateUserRequest(**request.get_json())
        user = container.user_service.create_user(data)
        return ApiResponse.success(user.dict(), status=201)
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        return ApiResponse.error(str(e), 400)
    except Exception as e:
        logger.error(f"Error creating user: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)

@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id: int):
    try:
        user = container.user_service.get_user(user_id)
        if not user:
            return ApiResponse.error("User not found", 404)
        return ApiResponse.success(user.dict())
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        return ApiResponse.error("Internal server error", 500)

@bp.route('', methods=['GET'])
def get_users():
    try:
        role = request.args.get('role')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        users = container.user_service.get_all_users(role_name=role, page=page, per_page=per_page)
        return ApiResponse.success([u.dict() for u in users])
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        return ApiResponse.error("Internal server error", 500)

@bp.route('/<int:user_id>', methods=['PATCH'])
def update_user(user_id: int):
    try:
        data = UpdateUserRequest(**request.get_json())
        user = container.user_service.update_user(user_id, data)
        return ApiResponse.success(user.dict())
    except ValueError as e:
        return ApiResponse.error(str(e), 400)
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        return ApiResponse.error("Internal server error", 500)

@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id: int):
    try:
        container.user_service.soft_delete_user(user_id)
        return ApiResponse.success({"message": "User deleted"})
    except ValueError as e:
        return ApiResponse.error(str(e), 404)
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        return ApiResponse.error("Internal server error", 500)