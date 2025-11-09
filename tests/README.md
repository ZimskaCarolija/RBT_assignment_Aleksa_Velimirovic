# Test Suite Documentation

## Overview

This folder contains a complete test suite for all API routes in the application. Tests cover:

- **Users Routes** (`test_users_routes.py`) - Tests for all user management endpoints
- **Vacation Routes** (`test_vacation_routes.py`) - Tests for vacation management endpoints
- **Import Routes** (`test_import_routes.py`) - Tests for bulk import endpoints

## Installation

First install required packages:

```bash
pip install -r requirements.txt
```

## Running Tests

### Run all tests

```bash
pytest
```

### Run specific test files

```bash
# Tests for users routes
pytest tests/test_users_routes.py

# Tests for vacation routes
pytest tests/test_vacation_routes.py

# Tests for import routes
pytest tests/test_import_routes.py
```

### Run specific test classes

```bash
# Tests for users routes
pytest tests/test_users_routes.py::TestUsersRoutes

# Tests for vacation routes
pytest tests/test_vacation_routes.py::TestVacationRoutes

# Tests for import routes
pytest tests/test_import_routes.py::TestImportRoutes
```

### Run specific test methods

```bash
# Example: test for creating user
pytest tests/test_users_routes.py::TestUsersRoutes::test_create_user_success
```

### Run with verbose output

```bash
pytest -v
```

### Run with detailed output

```bash
pytest -vv
```

### Run with coverage report

```bash
pytest --cov=. --cov-report=html
```

## Test Structure

### Test Configuration

- **`config/test.py`** - Test configuration using development database
- **`tests/conftest.py`** - Pytest fixtures for test setup

### Test Files

#### `test_users_routes.py`

Tests for users endpoints:
- `GET /users` - List users (with pagination and filtering)
- `POST /users` - Create new user
- `GET /users/{id}` - Get user by ID
- `PATCH /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user (soft delete)

**Covered scenarios:**
- Success cases
- Failure cases
- Authentication and authorization
- Data validation
- Error handling

#### `test_vacation_routes.py`

Tests for vacation endpoints:
- `GET /vacation/users/{id}/summary` - Vacation summary
- `POST /vacation/users/{id}/check` - Check overlap
- `POST /vacation/users/{id}/create` - Create vacation record
- `POST /vacation/users/{id}/entitlements` - Create entitlement
- `GET /vacation/users/{id}/records` - List vacation records

**Covered scenarios:**
- Success cases
- Failure cases
- Authentication and authorization
- Date validation
- Overlap checks
- Insufficient days checks

#### `test_import_routes.py`

Tests for import endpoints:
- `POST /import/users` - Import users from CSV
- `POST /import/vacations` - Import vacation records from CSV
- `POST /import/entitlements` - Import entitlements from CSV

**Covered scenarios:**
- Success imports
- Failure imports
- Admin-only access
- CSV file validation
- Error handling for invalid data

## Fixtures

### Basic Fixtures

- **`app`** - Flask application for testing
- **`client`** - Test client for HTTP requests
- **`db_session`** - Database session

### User Fixtures

- **`admin_role`** - Admin role
- **`employee_role`** - Employee role
- **`admin_user`** - Admin user
- **`employee_user`** - Employee user
- **`another_employee_user`** - Another employee user

### Auth Fixtures

- **`admin_auth_headers`** - Basic Auth headers for admin user
- **`employee_auth_headers`** - Basic Auth headers for employee user
- **`another_employee_auth_headers`** - Basic Auth headers for another employee user

### Vacation Fixtures

- **`vacation_entitlement`** - Vacation entitlement for testing
- **`vacation_record`** - Vacation record for testing

## Test Scenarios

### Success Scenarios

All tests cover successful scenarios:
- Valid data
- Correct authentication
- Correct authorization
- Valid request/response formats

### Failure Scenarios

All tests cover failure scenarios:
- **401 Unauthorized** - Missing authentication
- **403 Forbidden** - Missing permissions
- **400 Bad Request** - Invalid data
- **404 Not Found** - Resource does not exist
- **500 Internal Server Error** - Server errors

### Validation Scenarios

Tests cover validation:
- Email format
- Password length
- Date format
- Required fields
- Data types
- Business rules (overlap, insufficient days, etc.)

## Examples

### Example 1: Test for creating user

```python
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
```

### Example 2: Test for unauthorized access

```python
def test_create_user_unauthorized(self, client):
    user_data = {
        "email": "unauth@test.com",
        "password": "password123"
    }
    
    response = client.post(
        '/users',
        data=json.dumps(user_data),
        content_type='application/json'
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert data['success'] is False
```

## Troubleshooting

### Problem: Tests fail due to database

**Solution:** Check that `TestConfig` is properly configured to use development database.

### Problem: Tests fail due to authentication

**Solution:** Check that you are using correct auth headers from fixtures.

### Problem: Tests fail due to dependency injection

**Solution:** Check that `FlaskInjector` is properly configured in `create_app` function.

## Coverage

To generate coverage report:

```bash
pytest --cov=. --cov-report=html
```

This will create an HTML report in the `htmlcov/` folder.

## Best Practices

1. **Isolation** - Each test is isolated and does not depend on other tests
2. **Fixtures** - Use fixtures for setup and cleanup
3. **Assertions** - Use clear assertions with messages
4. **Naming** - Name tests clearly and descriptively
5. **Coverage** - Try to cover all scenarios (success and failure)

## Additional Notes

- Tests use development database
- Each test has a clean database state
- Upload folder is automatically cleaned after tests
- Tests use Basic Authentication with base64 encoding
