from flask import Blueprint, request, current_app
from flask_injector import inject
from services.import_service import ImportService
from werkzeug.utils import secure_filename
from utils.response import ApiResponse
import os
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('import', __name__, url_prefix='/import')


@bp.route('/users', methods=['POST'])
@inject
def import_users(import_service: ImportService):
    if 'file' not in request.files:
        return ApiResponse.error("File required", 400)

    file = request.files['file']
    if not file.filename:
        return ApiResponse.error("Empty file name", 400)

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )
    file.save(upload_path)

    result = import_service.import_users_from_file(upload_path)
    status = 200 if result.success else 400
    return ApiResponse.success(result.dict(), status=status)


@bp.route('/vacations', methods=['POST'])
@inject
def import_vacations(import_service: ImportService):
    if 'file' not in request.files:
        return ApiResponse.error("File required", 400)

    file = request.files['file']
    if not file.filename:
        return ApiResponse.error("Empty file name", 400)

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )
    file.save(upload_path)

    result = import_service.import_vacation_records_from_file(upload_path)
    status = 200 if result.success else 400
    return ApiResponse.success(result.dict(), status=status)


@bp.route('/entitlements', methods=['POST'])
@inject
def import_entitlements(import_service: ImportService):
    if 'file' not in request.files:
        return ApiResponse.error("File required", 400)

    file = request.files['file']
    if not file.filename:
        return ApiResponse.error("Empty file name", 400)

    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )
    file.save(upload_path)

    result = import_service.import_vacation_entitlements_from_file(upload_path)
    status = 200 if result.success else 400
    return ApiResponse.success(result.dict(), status=status)