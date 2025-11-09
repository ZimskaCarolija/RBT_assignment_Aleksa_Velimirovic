import base64
from functools import wraps
from flask import request, jsonify, current_app
from typing import Tuple, Optional
from repositories import UserRepository

def decode_basic_auth(auth_header: str) -> Optional[Tuple[str, str]]:
    """
    Dekodira Basic Auth header i vraća (email, password)
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

def basic_auth_required(f):
    """
    Middleware za Basic autentifikaciju
    Provjerava da li su credentials ispravni i da li korisnik postoji
    """
    @wraps(f)
    def decorated(*args, **kwargs):
    
        auth_header = request.headers.get('Authorization')
        credentials = decode_basic_auth(auth_header)
        
        if not credentials:
            return jsonify({
                'error': 'Authorization required',
                'message': 'Provide valid Basic Auth credentials'
            }), 401
        
        email, password = credentials
        
        # Provjera korisnika
        user_repo = UserRepository(db.session)
        user = user_repo.get_by_email(email)
        
        if not user:
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'User not found'
            }), 401
        
        # Provjera passworda
        if not user.check_password(password):
            return jsonify({
                'error': 'Invalid credentials',
                'message': 'Wrong password'
            }), 401
        
        # Dodaj korisnika u request context za kasniju upotrebu
        request.current_user = user
        request.user_id = user.id
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """
    Middleware koji provjerava da li je korisnik admin
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        from .user_repository import UserRepository
        from . import db
        
        # Prvo provjeri basic auth
        if not hasattr(request, 'current_user'):
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please authenticate first'
            }), 401
        
        user_repo = UserRepository(db.session)
        
        # Provjeri da li je admin
        if not user_repo.is_admin(request.current_user.id):
            return jsonify({
                'error': 'Forbidden',
                'message': 'Admin privileges required'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated

def ownership_required(f):
    """
    Middleware koji provjerava da li korisnik pristupa vlastitim podacima
    ili je admin
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        from .user_repository import UserRepository
        from . import db
        
        if not hasattr(request, 'current_user'):
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please authenticate first'
            }), 401
        
        user_repo = UserRepository(db.session)
        current_user_id = request.current_user.id
        
        # Dohvati user_id iz route parametara
        target_user_id = kwargs.get('user_id')
        if target_user_id is None:
            # Ako nema user_id u ruti, provjeri query parametre ili body
            target_user_id = request.args.get('user_id') or request.json.get('user_id') if request.json else None
        
        if target_user_id is None:
            return jsonify({
                'error': 'Bad request',
                'message': 'User ID not specified'
            }), 400
        
        try:
            target_user_id = int(target_user_id)
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Bad request',
                'message': 'Invalid user ID'
            }), 400
        
        # Provjeri da li je korisnik admin ILI pristupa vlastitim podacima
        if not user_repo.is_admin(current_user_id) and current_user_id != target_user_id:
            return jsonify({
                'error': 'Forbidden',
                'message': 'You can only access your own data'
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated