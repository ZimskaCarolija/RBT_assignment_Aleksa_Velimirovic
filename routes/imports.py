from flask import Blueprint, request, current_app
from flask_injector import inject
from services.import_service import ImportService
from werkzeug.utils import secure_filename
from utils.response import ApiResponse
from utils.file_helper import save_uploaded_file
from middleware.auth import login_required, admin_required
import os
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('import', __name__, url_prefix='/import')

@bp.route('/users', methods=['POST'])
@login_required
@admin_required
@inject
def import_users(import_service: ImportService):
    try:
        if 'file' not in request.files:
            return ApiResponse.error("File required", 400)

        file = request.files['file']
        if not file.filename:
            return ApiResponse.error("Empty file name", 400)

        upload_path = save_uploaded_file(file)

        result = import_service.import_users_from_file(upload_path)
        import_service.session.commit()
        status = 200 if result.success else 400
        return ApiResponse.success(result.model_dump(), status)
    except Exception as e:
        logger.error(f"Error in /users import: {e}")
        return ApiResponse.error(f"Server error: {str(e)}", 500)

@bp.route('/vacations', methods=['POST'])
@login_required
@admin_required
@inject
def import_vacations(import_service: ImportService):
    try:
        if 'file' not in request.files:
            return ApiResponse.error("File required", 400)

        file = request.files['file']
        if not file.filename:
            return ApiResponse.error("Empty file name", 400)

        upload_path = save_uploaded_file(file)

        result = import_service.import_vacation_records_from_file(upload_path)
        import_service.session.commit()
        status = 200 if result.success else 400
        return ApiResponse.success(result.model_dump(), status)
    except Exception as e:
        logger.error(f"Error in /vacations import: {e}")
        return ApiResponse.error(f"Server error: {str(e)}", 500)

@bp.route('/entitlements', methods=['POST'])
@login_required
@admin_required
@inject
def import_entitlements(import_service: ImportService):
    try:
        if 'file' not in request.files:
            return ApiResponse.error("File required", 400)

        file = request.files['file']
        if not file.filename:
            return ApiResponse.error("Empty file name", 400)

        upload_path = save_uploaded_file(file)

        result = import_service.import_vacation_entitlements_from_file(upload_path)
        import_service.session.commit()
        status = 200 if result.success else 400
        return ApiResponse.success(result.model_dump(), status)
    except Exception as e:
        logger.error(f"Error in /entitlements import: {e}")
        return ApiResponse.error(f"Server error: {str(e)}", 500)