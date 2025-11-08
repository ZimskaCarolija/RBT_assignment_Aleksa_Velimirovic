from flask import Blueprint, request, current_app
import os
from container import container
from werkzeug.utils import secure_filename
from utils.response import ApiResponse
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('import', __name__, url_prefix='/import')

@bp.route('/import/users', methods=['POST'])
def import_users():
    if 'file' not in request.files:
        return ApiResponse.error("File required", 400)
    file = request.files['file']
    if not file.filename:
        return ApiResponse.error("File required", 400)
    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )
    file.save(upload_path)
    result = container.import_service.import_users_from_file(file)
    status = 200 if result.success else 400
    return ApiResponse.success(result.dict(),status)

@bp.route('/import/vacations', methods=['POST'])
def import_vacations():
    if 'file' not in request.files:
        return ApiResponse.error("File required", 400)
    file = request.files['file']
    if not file.filename:
        return ApiResponse.error("File required", 400)
    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )
    file.save(upload_path)
    result = container.import_service.import_vacation_records_from_file(file)
    status = 200 if result.success else 400
    return ApiResponse.success(result.dict(),status)

@bp.route('/import/entitlments', methods=['POST'])
def import_entitlements():
    if 'file' not in request.files:
        return ApiResponse.error("File required", 400)
    file = request.files['file']
    if not file.filename:
        return ApiResponse.error("File required", 400)
    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )
    file.save(upload_path)
    result = container.import_service.import_vacation_entitlements_from_file(file)
    status = 200 if result.success else 400
    return ApiResponse.success(result.dict(),status)