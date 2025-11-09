from flask import Blueprint, request
from flask_injector import inject
from services.vacation_service import VacationService
from dto import (
    CheckOverlapRequest,
    VacationSummaryDTO,
    CreateVacationRequest,
    VacationRecordDTO,
    CreateEntitlementRequest
)
from utils.response import ApiResponse
from typing import Optional
from datetime import datetime
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
        return ApiResponse.success(summary.model_dump())

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
        return ApiResponse.success(result.model_dump())

    except Exception as e:
        logger.error(f"Unexpected error in overlap check (user {user_id}): {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)


@bp.route('/users/<int:user_id>/create', methods=['POST'])
@inject
def create_vacation_record(user_id: int, vacation_service: VacationService):
    """
    POST /vacation/users/1/create
    { "start_date": "2025-07-01", "end_date": "2025-07-05", "note": "Summer" }
    """
    try:
        data = CreateVacationRequest(**request.get_json())
        record = vacation_service.create_vacation(user_id, data)
        vacation_service.session.commit()
        return ApiResponse.success(record.model_dump(), 201)
    except ValueError as e:
        vacation_service.session.rollback()
        logger.warning(f"Validation error creating vacation for user {user_id}: {e}")
        return ApiResponse.error(str(e), 400)
    except Exception as e:
        vacation_service.session.rollback()
        logger.error(f"Error while creatint vacation: {e}", exc_info=True)
        return ApiResponse.error("Error", 500)
    
@bp.route('/users/<int:user_id>/entitlements', methods=['POST'])
@inject
def create_entitlement(user_id: int, vacation_service: VacationService):
    """
    POST /vacation/users/1/entitlements
    {
      "year": 2025,
      "total_days": 25
    }
    """
    try:
        data = CreateEntitlementRequest(**request.get_json())
        entitlement = vacation_service.create_entitlement(user_id, data.year, data.total_days)
        vacation_service.session.commit()
        return ApiResponse.success(entitlement.model_dump())

    except ValueError as e:
        vacation_service.session.rollback()
        logger.warning(f"Validation error creating entitlement for user {user_id}: {e}")
        return ApiResponse.error(str(e), 400)

    except Exception as e:
        vacation_service.session.rollback()
        logger.error(f"Error creating entitlement: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)
@bp.route('/users/<int:user_id>/records', methods=['GET'])
@inject
def get_vacation_records(user_id: int, vacation_service: VacationService):
    """
    GET /vacation/users/1/records?from_date=2025-07-01&to_date=2025-07-31&page=1&per_page=20
    """
    try:
        from_date_str: Optional[str] = request.args.get('from_date')
        to_date_str: Optional[str] = request.args.get('to_date')
        page: int = request.args.get('page', 1, type=int)
        per_page: int = request.args.get('per_page', 20, type=int)

        if not from_date_str or not to_date_str:
            return ApiResponse.error("from_date and to_date query parameters are required", 400)

        from_date = datetime.strptime(from_date_str, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date_str, "%Y-%m-%d").date()

        vacations = vacation_service.get_vacations_in_period(
            user_id=user_id,
            from_date=from_date,
            to_date=to_date,
            page=page,
            per_page=per_page
        )

        return ApiResponse.success(vacations.model_dump())

    except ValueError as e:
        logger.warning(f"Invalid input for vacation records (user {user_id}): {e}")
        return ApiResponse.error(str(e), 400)
    except Exception as e:
        logger.error(f"Unexpected error fetching vacation records for user {user_id}: {e}", exc_info=True)
        return ApiResponse.error("Internal server error", 500)