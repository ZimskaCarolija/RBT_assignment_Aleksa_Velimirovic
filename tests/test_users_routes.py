import pytest
import json
from datetime import datetime


class TestUsersRoutes:

    # POST /users - success
    def test_create_user_success(self, client, admin_auth_headers, employee_role):
        user_data = {
            "email": "newuser@test.com",
            "password": "password123",
            "full_name": "New User"
        }
        
        response = client.post(
            '/users',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] is True

    # POST /users - fail
    def test_create_user_duplicate_email(self, client, admin_auth_headers, employee_user):
        user_data = {
            "email": employee_user.email,
            "password": "password123",
            "full_name": "Duplicate User"
        }
        
        response = client.post(
            '/users',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # GET /users - success
    def test_get_users_success(self, client, admin_auth_headers, employee_user, admin_user):
        response = client.get('/users', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)

    # GET /users - fail
    def test_get_users_unauthorized(self, client):
        response = client.get('/users')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False

    # GET /users/<id> - success
    def test_get_user_by_id_success(self, client, admin_auth_headers, employee_user):
        response = client.get(f'/users/{employee_user.id}', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == employee_user.id

    # GET /users/<id> - fail
    def test_get_user_by_id_not_found(self, client, admin_auth_headers):
        response = client.get('/users/99999', headers=admin_auth_headers)
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['success'] is False

    # PATCH /users/<id> - success
    def test_update_user_success(self, client, admin_auth_headers, employee_user):
        update_data = {
            "email": "updated@test.com",
            "full_name": "Updated Name"
        }
        
        response = client.patch(
            f'/users/{employee_user.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True