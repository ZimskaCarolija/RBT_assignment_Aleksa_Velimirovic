from flask import Blueprint, request
from flask_injector import inject
from services.vacation_service import VacationService
from dto import (
    CheckOverlapRequest,
    VacationSummaryDTO,
    CreateVacationRequest,
    VacationRecordDTO
)
from utils.response import ApiResponse
from typing import Optional
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('vacation', __name__, url_prefix='/vacation')


@bp.route('/users/<int:user_id>/summary', methods=['GET'])
@inject
def vacation_summary(user_id: int, vacation_service: VacationService):
    """
    GET /vacation/users/1/summary?year=2025
    """
    try:
        year: Optional[int] = request.args.get('year', type=int)
        summary = vacation_service.get_vacation_summary(user_id, year)
        return ApiResponse.success(summary.dict())

    except ValueError as e:
        logger.warning(f"Validation error for user {user_id}: {e}")
        return ApiResponse.error(str(e), 400)

    except Exception as e:
        logger.error(f"Unexpected error in summary for user {user_id}: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)


@bp.route('/users/<int:user_id>/check', methods=['POST'])
@inject
def check_overlap(user_id: int, vacation_service: VacationService):
    """
    POST /vacation/users/1/check
    { "start_date": "2025-07-01", "end_date": "2025-07-05" }
    """
    try:
        data = CheckOverlapRequest(**request.get_json())
    except ValueError as e:
        logger.warning(f"Invalid input for overlap check (user {user_id}): {e}")
        return ApiResponse.error(str(e), 400)

    try:
        result = vacation_service.has_overlap_in_period(
            user_id, data.start_date, data.end_date
        )
        return ApiResponse.success(result.dict())

    except Exception as e:
        logger.error(f"Unexpected error in overlap check (user {user_id}): {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)


@bp.route('/users/<int:user_id>/create', methods=['POST'])
@inject
def create_vacation_record(user_id: int, vacation_service: VacationService):
    """
    POST /vacation/users/1/create
    { "start_date": "2025-07-01", "end_date": "2025-07-05", "note": "Letovanje" }
    """
    try:
        data = CreateVacationRequest(**request.get_json())
        record = vacation_service.create_vacation(user_id, data)
        return ApiResponse.success(record.dict(), status=201)
    except ValueError as e:
        logger.warning(f"Validation error creating vacation for user {user_id}: {e}")
        return ApiResponse.error(str(e), 400)
    except Exception as e:
        logger.error(f"Greška pri kreiranju odmora: {e}", exc_info=True)
        return ApiResponse.error("Interna greška", 500)