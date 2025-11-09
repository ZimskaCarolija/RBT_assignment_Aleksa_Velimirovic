import base64
from functools import wraps
from flask import request, g
from typing import Tuple, Optional
from models import db
from repositories.user_repository import UserRepository
from utils.response import ApiResponse
from constants import RoleIds

def decode_basic_auth(auth_header: str) -> Optional[Tuple[str, str]]:
    """
    Format: Authorization: Basic base64(email:password)
    """
    try:
        if not auth_header or not auth_header.startswith('Basic '):
            return None
            
        encoded_credentials = auth_header.split(' ')[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        email, password = decoded_credentials.split(':', 1)
        return email, password
    except (ValueError, IndexError, UnicodeDecodeError, base64.binascii.Error):
        return None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        credentials = decode_basic_auth(auth_header)
        
        if not credentials:
            return ApiResponse.error('Authorization required. Provide valid Basic Auth credentials (email:password base64 encoded)', 401)
        
        email, password = credentials
    
        user_repo = UserRepository(g.db_session)
        user = user_repo.get_by_email(email)
        
        if not user:
            return ApiResponse.error('Invalid credentials - User not found', 401)
        
        if not user.check_password(password):
            return ApiResponse.error('Invalid credentials - Wrong password', 401)
        
        request.current_user = user
        request.user_id = user.id
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return ApiResponse.error('Authentication required. Please authenticate first using login_required middleware', 401)
        
        user_repo = UserRepository(g.db_session)
        current_user_id = request.current_user.id
        
        if not user_repo.is_admin(current_user_id):
            return ApiResponse.error('Admin privileges required', 403)
        
        return f(*args, **kwargs)
    
    return decorated

def admin_or_owner_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return ApiResponse.error('Authentication required. Please authenticate first using login_required middleware', 401)
        
        user_repo = UserRepository(g.db_session)
        current_user_id = request.current_user.id
        
        target_user_id = kwargs.get('user_id')
        if target_user_id is None:
            target_user_id = request.args.get('user_id')
            if target_user_id is None and request.is_json:
                target_user_id = request.json.get('user_id') if request.json else None
        
        if target_user_id is None:
            return ApiResponse.error('User ID not specified in route, query params or body', 400)
        
        try:
            target_user_id = int(target_user_id)
        except (ValueError, TypeError):
            return ApiResponse.error('Invalid user ID format', 400)
        
        is_admin = user_repo.is_admin(current_user_id)
        is_owner = current_user_id == target_user_id
        
        if not is_admin and not is_owner:
            return ApiResponse.error('You can only access your own data or must be an admin', 403)
        
        return f(*args, **kwargs)
    
    return decorated