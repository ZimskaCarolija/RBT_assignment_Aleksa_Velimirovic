from flask import Blueprint, request, jsonify
from container import container
from dto import CheckOverlapRequest, VacationSummaryDTO,CreateVacationRequest,VacationRecordDTO
from utils.response import ApiResponse
from typing import Optional
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('vacation', __name__, url_prefix='/vacation')

@bp.route('/users/<int:user_id>/summary', methods=['GET'])
def vacation_summary(user_id: int):

    try:
        year: Optional[int] = request.args.get('year', type=int)
        summary = container.vacation_service.get_vacation_summary(user_id, year)
        return ApiResponse.success(summary.dict())
    
    except ValueError as e:
        logger.warning(f"Validation error for user {user_id}: {e}")
        return ApiResponse.error(str(e), 400)
    
    except Exception as e:
        logger.error(f"Unexpected error in summary for user {user_id}: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)


@bp.route('/users/<int:user_id>/check', methods=['POST'])
def check_overlap(user_id: int):

    try:
        data = CheckOverlapRequest(**request.get_json())
    except ValueError as e:
        logger.warning(f"Invalid input for overlap check (user {user_id}): {e}")
        return ApiResponse.error(str(e), 400)

    try:
        result = container.vacation_service.has_overlap_in_period(
            user_id, data.start_date, data.end_date
        )
        return ApiResponse.success(result.dict())
    
    except Exception as e:
        logger.error(f"Unexpected error in overlap check (user {user_id}): {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)
    
@bp.route('/users/<int:user_id>/create', methods=['POST'])
def create_vacation_record(user_id: int):

    try:
        data = CreateVacationRequest(**request.get_json())
        record = container.vacation_service.create_vacation(user_id, data)
        return ApiResponse.success(record.dict(), status=201)
    except ValueError as e:
        return ApiResponse.error(str(e), 400)
    except Exception as e:
        logger.error(f"Greška pri kreiranju odmora: {e}")
        return ApiResponse.error("Interna greška", 500)