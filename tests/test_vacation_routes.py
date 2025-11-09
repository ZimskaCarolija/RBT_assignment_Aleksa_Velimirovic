import pytest
import json
from datetime import date, datetime


class TestVacationRoutes:

    # GET /vacation/users/<id>/summary - success
    def test_get_vacation_summary_success(self, client, admin_auth_headers, employee_user, vacation_entitlement, vacation_record):
        response = client.get(f'/vacation/users/{employee_user.id}/summary?year=2025', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'total_days' in data['data']

    # GET /vacation/users/<id>/summary - fail
    def test_get_vacation_summary_forbidden(self, client, employee_auth_headers, another_employee_user):
        response = client.get(f'/vacation/users/{another_employee_user.id}/summary?year=2025', headers=employee_auth_headers)
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False

    # POST /vacation/users/<id>/check - success
    def test_check_overlap_success(self, client, admin_auth_headers, employee_user, vacation_record):
        check_data = {
            "start_date": "2025-08-01",
            "end_date": "2025-08-05"
        }
        
        response = client.post(
            f'/vacation/users/{employee_user.id}/check',
            data=json.dumps(check_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # POST /vacation/users/<id>/check - fail
    def test_check_overlap_missing_fields(self, client, admin_auth_headers, employee_user):
        check_data = {
            "start_date": "2025-08-01"
        }
        
        response = client.post(
            f'/vacation/users/{employee_user.id}/check',
            data=json.dumps(check_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # POST /vacation/users/<id>/create - success
    def test_create_vacation_record_success(self, client, admin_auth_headers, employee_user, vacation_entitlement):
        vacation_data = {
            "start_date": "2025-08-01",
            "end_date": "2025-08-05",
            "note": "Summer vacation"
        }
        
        response = client.post(
            f'/vacation/users/{employee_user.id}/create',
            data=json.dumps(vacation_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True

    # POST /vacation/users/<id>/create - fail
    def test_create_vacation_record_overlap(self, client, admin_auth_headers, employee_user, vacation_entitlement, vacation_record):
        vacation_data = {
            "start_date": "2025-07-03",
            "end_date": "2025-07-10",
            "note": "Overlapping vacation"
        }
        
        response = client.post(
            f'/vacation/users/{employee_user.id}/create',
            data=json.dumps(vacation_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # POST /vacation/users/<id>/entitlements - success
    def test_create_entitlement_success(self, client, admin_auth_headers, employee_user):
        entitlement_data = {
            "year": 2026,
            "total_days": 25
        }
        
        response = client.post(
            f'/vacation/users/{employee_user.id}/entitlements',
            data=json.dumps(entitlement_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # POST /vacation/users/<id>/entitlements - fail
    def test_create_entitlement_missing_fields(self, client, admin_auth_headers, employee_user):
        entitlement_data = {
            "year": 2026
        }
        
        response = client.post(
            f'/vacation/users/{employee_user.id}/entitlements',
            data=json.dumps(entitlement_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # GET /vacation/users/<id>/records - success
    def test_get_vacation_records_success(self, client, admin_auth_headers, employee_user, vacation_record):
        response = client.get(
            f'/vacation/users/{employee_user.id}/records?from_date=2025-07-01&to_date=2025-07-31',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # GET /vacation/users/<id>/records - fail
    def test_get_vacation_records_missing_dates(self, client, admin_auth_headers, employee_user):
        response = client.get(
            f'/vacation/users/{employee_user.id}/records',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
