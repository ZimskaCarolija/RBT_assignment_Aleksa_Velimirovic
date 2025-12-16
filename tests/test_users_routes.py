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

    # PATCH /users/<id> - fail (unauthorized employee)
    def test_update_user_unauthorized_employee(self, client, employee_auth_headers, another_employee_user):
        """Test that employees cannot update other employees' data"""
        update_data = {
            "email": "hacked@test.com",
            "full_name": "Hacked Name"
        }
        
        response = client.patch(
            f'/users/{another_employee_user.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=employee_auth_headers
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'admin' in data['error'].lower() or 'own' in data['error'].lower()

    # PATCH /users/<id> - success (employee updates own data)
    def test_update_user_employee_self(self, client, employee_auth_headers, employee_user):
        """Test that employees can update their own data"""
        update_data = {
            "full_name": "Updated Self Name"
        }
        
        response = client.patch(
            f'/users/{employee_user.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=employee_auth_headers
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['full_name'] == "Updated Self Name"

    # PATCH /users/<id> - fail (validation error - invalid email)
    def test_update_user_invalid_email(self, client, admin_auth_headers, employee_user):
        """Test updating user with invalid email format"""
        update_data = {
            "email": "not-an-email"
        }
        
        response = client.patch(
            f'/users/{employee_user.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # PATCH /users/<id> - fail (password too short)
    def test_update_user_password_too_short(self, client, admin_auth_headers, employee_user):
        """Test updating user with password shorter than minimum length"""
        update_data = {
            "password": "12345"
        }
        
        response = client.patch(
            f'/users/{employee_user.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # PATCH /users/<id> - fail (duplicate email)
    def test_update_user_duplicate_email(self, client, admin_auth_headers, employee_user, another_employee_user):
        """Test updating user with an email that already exists"""
        update_data = {
            "email": another_employee_user.email
        }
        
        response = client.patch(
            f'/users/{employee_user.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'email' in data['error'].lower() or 'use' in data['error'].lower()

    # PATCH /users/<id> - fail (non-existent user)
    def test_update_user_not_found(self, client, admin_auth_headers):
        """Test updating a non-existent user"""
        update_data = {
            "full_name": "Ghost User"
        }
        
        response = client.patch(
            '/users/99999',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # GET /users - success with pagination
    def test_get_users_with_pagination(self, client, admin_auth_headers, employee_user, admin_user):
        """Test getting users with pagination parameters"""
        response = client.get('/users?page=1&per_page=10', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert len(data['data']) <= 10

    # GET /users - success with different page sizes
    def test_get_users_custom_page_size(self, client, admin_auth_headers, employee_user, admin_user):
        """Test getting users with custom page size"""
        response = client.get('/users?page=1&per_page=1', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert len(data['data']) <= 1

    # GET /users - success with role filter
    def test_get_users_filter_by_role(self, client, admin_auth_headers, employee_user, employee_role):
        """Test filtering users by role"""
        response = client.get('/users?role=Employee', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        # All returned users should have employee role_id
        for user in data['data']:
            assert user['role_id'] == employee_role.id

    # GET /users - success with admin role filter
    def test_get_users_filter_by_admin_role(self, client, admin_auth_headers, admin_user, admin_role):
        """Test filtering users by admin role"""
        response = client.get('/users?role=Admin', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        # All returned users should have admin role_id
        for user in data['data']:
            assert user['role_id'] == admin_role.id

    # GET /users - success with non-existent role filter
    def test_get_users_filter_by_nonexistent_role(self, client, admin_auth_headers):
        """Test filtering users by a role that doesn't exist"""
        response = client.get('/users?role=NonExistentRole', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert len(data['data']) == 0

    # GET /users - fail (employee access)
    def test_get_users_forbidden_employee(self, client, employee_auth_headers):
        """Test that employees cannot list all users"""
        response = client.get('/users', headers=employee_auth_headers)
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'admin' in data['error'].lower()

    # GET /users - edge case (page 0)
    def test_get_users_page_zero(self, client, admin_auth_headers):
        """Test pagination with page 0 (should use page 1 or handle gracefully)"""
        response = client.get('/users?page=0&per_page=10', headers=admin_auth_headers)
        
        # Should either return 200 with data or handle gracefully
        assert response.status_code in [200, 400]
        data = json.loads(response.data)
        assert 'success' in data

    # GET /users - edge case (negative page)
    def test_get_users_negative_page(self, client, admin_auth_headers):
        """Test pagination with negative page number"""
        response = client.get('/users?page=-1&per_page=10', headers=admin_auth_headers)
        
        # Should handle gracefully
        assert response.status_code in [200, 400]
        data = json.loads(response.data)
        assert 'success' in data

    # GET /users - edge case (very large page number)
    def test_get_users_large_page_number(self, client, admin_auth_headers):
        """Test pagination with very large page number"""
        response = client.get('/users?page=10000&per_page=10', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert len(data['data']) == 0  # No users on page 10000

    # GET /users - edge case (invalid page parameter)
    def test_get_users_invalid_page_parameter(self, client, admin_auth_headers):
        """Test pagination with invalid page parameter"""
        response = client.get('/users?page=abc&per_page=10', headers=admin_auth_headers)
        
        # Flask's request.args.get with type=int should use default (1)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # GET /users - edge case (invalid per_page parameter)
    def test_get_users_invalid_per_page_parameter(self, client, admin_auth_headers):
        """Test pagination with invalid per_page parameter"""
        response = client.get('/users?page=1&per_page=xyz', headers=admin_auth_headers)
        
        # Flask's request.args.get with type=int should use default (20)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # GET /users - edge case (zero per_page)
    def test_get_users_zero_per_page(self, client, admin_auth_headers):
        """Test pagination with per_page=0"""
        response = client.get('/users?page=1&per_page=0', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)

    # GET /users - edge case (very large per_page)
    def test_get_users_large_per_page(self, client, admin_auth_headers):
        """Test pagination with very large per_page value"""
        response = client.get('/users?page=1&per_page=1000', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)

    # POST /users - fail (missing required fields)
    def test_create_user_missing_email(self, client, admin_auth_headers):
        """Test creating user without email"""
        user_data = {
            "password": "password123",
            "full_name": "No Email User"
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

    # POST /users - fail (missing password)
    def test_create_user_missing_password(self, client, admin_auth_headers):
        """Test creating user without password"""
        user_data = {
            "email": "nopass@test.com",
            "full_name": "No Password User"
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

    # POST /users - fail (invalid email format)
    def test_create_user_invalid_email_format(self, client, admin_auth_headers):
        """Test creating user with invalid email format"""
        user_data = {
            "email": "not-valid-email",
            "password": "password123",
            "full_name": "Invalid Email User"
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

    # POST /users - fail (password too short)
    def test_create_user_password_too_short(self, client, admin_auth_headers):
        """Test creating user with password shorter than minimum length"""
        user_data = {
            "email": "shortpass@test.com",
            "password": "12345",
            "full_name": "Short Password User"
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

    # POST /users - fail (empty JSON body)
    def test_create_user_empty_body(self, client, admin_auth_headers):
        """Test creating user with empty JSON body"""
        response = client.post(
            '/users',
            data=json.dumps({}),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['success'] is False

    # POST /users - fail (no JSON body)
    def test_create_user_no_json(self, client, admin_auth_headers):
        """Test creating user without JSON content"""
        response = client.post(
            '/users',
            headers=admin_auth_headers
        )
        
        assert response.status_code in [400, 500]
        data = json.loads(response.data)
        assert data['success'] is False

    # POST /users - fail (employee cannot create users)
    def test_create_user_forbidden_employee(self, client, employee_auth_headers):
        """Test that employees cannot create users"""
        user_data = {
            "email": "newuser@test.com",
            "password": "password123",
            "full_name": "New User"
        }
        
        response = client.post(
            '/users',
            data=json.dumps(user_data),
            content_type='application/json',
            headers=employee_auth_headers
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False
        assert 'admin' in data['error'].lower()

    # POST /users - success (without full_name)
    def test_create_user_without_full_name(self, client, admin_auth_headers, employee_role):
        """Test creating user without optional full_name"""
        user_data = {
            "email": "noname@test.com",
            "password": "password123"
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
        assert data['data']['email'] == "noname@test.com"
        assert data['data']['full_name'] is None

    # GET /users/<id> - fail (employee accessing another employee)
    def test_get_user_by_id_forbidden_employee(self, client, employee_auth_headers, another_employee_user):
        """Test that employees cannot access other employees' data"""
        response = client.get(f'/users/{another_employee_user.id}', headers=employee_auth_headers)
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['success'] is False

    # GET /users/<id> - success (employee accessing own data)
    def test_get_user_by_id_employee_self(self, client, employee_auth_headers, employee_user):
        """Test that employees can access their own data"""
        response = client.get(f'/users/{employee_user.id}', headers=employee_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['data']['id'] == employee_user.id
        assert data['data']['email'] == employee_user.email

    # GET /users/<id> - fail (invalid user ID format)
    def test_get_user_by_id_invalid_format(self, client, admin_auth_headers):
        """Test getting user with invalid ID format"""
        response = client.get('/users/abc', headers=admin_auth_headers)
        
        assert response.status_code == 404

    # GET /users/<id> - success (verify response structure)
    def test_get_user_by_id_response_structure(self, client, admin_auth_headers, employee_user):
        """Test that user response has correct structure"""
        response = client.get(f'/users/{employee_user.id}', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert 'id' in data['data']
        assert 'email' in data['data']
        assert 'full_name' in data['data']
        assert 'role_id' in data['data']
        assert 'created_at' in data['data']
        assert 'updated_at' in data['data']
        assert 'password' not in data['data']  # Password should not be exposed

    # GET /users - success (verify response structure)
    def test_get_users_response_structure(self, client, admin_auth_headers, employee_user, admin_user):
        """Test that users list response has correct structure"""
        response = client.get('/users', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'data' in data
        assert isinstance(data['data'], list)
        assert 'error' in data
        assert data['error'] is None
        
        # Check each user object structure
        for user in data['data']:
            assert 'id' in user
            assert 'email' in user
            assert 'role_id' in user
            assert 'password' not in user  # Password should not be exposed

    # PATCH /users/<id> - success (update password)
    def test_update_user_password(self, client, admin_auth_headers, employee_user):
        """Test updating user password"""
        update_data = {
            "password": "newpassword123"
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
        # Password should not be in response
        assert 'password' not in data['data']

    # PATCH /users/<id> - success (update only email)
    def test_update_user_email_only(self, client, admin_auth_headers, employee_user):
        """Test updating only user email"""
        update_data = {
            "email": "newemail@test.com"
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
        assert data['data']['email'] == "newemail@test.com"

    # PATCH /users/<id> - success (update only full_name)
    def test_update_user_full_name_only(self, client, admin_auth_headers, employee_user):
        """Test updating only user full name"""
        original_email = employee_user.email
        update_data = {
            "full_name": "New Full Name"
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
        assert data['data']['full_name'] == "New Full Name"
        assert data['data']['email'] == original_email  # Email should not change

    # PATCH /users/<id> - fail (empty update)
    def test_update_user_empty_update(self, client, admin_auth_headers, employee_user):
        """Test updating user with empty data"""
        update_data = {}
        
        response = client.patch(
            f'/users/{employee_user.id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers=admin_auth_headers
        )
        
        # Should still return success as no validation errors
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True

    # POST /users - success (special characters in name)
    def test_create_user_special_characters_name(self, client, admin_auth_headers, employee_role):
        """Test creating user with special characters in name"""
        user_data = {
            "email": "special@test.com",
            "password": "password123",
            "full_name": "Test User-O'Brien (Jr.)"
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
        assert data['data']['full_name'] == "Test User-O'Brien (Jr.)"

    # POST /users - success (email with subdomain)
    def test_create_user_email_with_subdomain(self, client, admin_auth_headers, employee_role):
        """Test creating user with subdomain in email"""
        user_data = {
            "email": "user@subdomain.example.com",
            "password": "password123",
            "full_name": "Subdomain User"
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
        assert data['data']['email'] == "user@subdomain.example.com"

    # POST /users - success (verify default role assignment)
    def test_create_user_default_role(self, client, admin_auth_headers, employee_role):
        """Test that new users are assigned employee role by default"""
        user_data = {
            "email": "defaultrole@test.com",
            "password": "password123",
            "full_name": "Default Role User"
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
        assert data['data']['role_id'] == employee_role.id

    # GET /users - success (multiple users with pagination page 2)
    def test_get_users_second_page(self, client, admin_auth_headers, employee_user, admin_user, another_employee_user):
        """Test getting second page of users"""
        response = client.get('/users?page=2&per_page=1', headers=admin_auth_headers)
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)