# RBT Assignment - Aleksa Velimirovic

Flask application for managing employee vacations.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/ZimskaCarolija/RBT_assignment_Aleksa_Velimirovic.git
cd RBT_assignment_Aleksa_Velimirovic
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment configuration

Create a `.env` file in the root directory with the following variables:

FLASK_APP=app.py
FLASK_ENV=development
DEV_DATABASE_URL=
PRO_DATABASE_URL=
SECRET_KEY=supersecretkey
UPLOAD_FOLDER = uploads

### 4. Run database migrations

```bash
python -m flask db upgrade
```

### 5. Seed database with initial data

```bash
python -m flask --app app.py create
```

This command will add initial data:
- **Roles**: Admin, Employee
- **Users**: velimirovicaleksa001@gmail.com (password: `aleksa`)

**Note:** Passwords are hashed using `werkzeug.security.generate_password_hash` with salt, so each hash is unique.

### 6. Run the application

```bash
python app.py
```

Or using Flask CLI:

```bash
python -m flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
RBT_assignment_Aleksa_Velimirovic/
├── app.py                          # Main application entry point
├── container.py                    # Dependency injection container
├── requirements.txt                # Python dependencies
├── pytest.ini                     # Pytest configuration
├── README.md                       # This file
│
├── commands/                       # Flask CLI commands
│   ├── __init__.py
│   └── seed.py                    # Database seeding command
│
├── config/                         # Application configuration
│   ├── base.py                    # Base configuration
│   ├── development.py             # Development environment config
│   ├── production.py              # Production environment config
│   └── test.py                    # Test environment config
│
├── dto/                            # Data Transfer Objects (Pydantic models)
│   ├── __init__.py
│   ├── check_overlap_dto.py
│   ├── create_entitlement_request.py
│   ├── create_user_request.py
│   ├── entitlement_dto.py
│   ├── Import_result.py
│   ├── update_user_request.py
│   ├── user_response.py
│   ├── vacation_create.py
│   ├── vacation_list_dto.py
│   ├── vacation_record_dto.py
│   ├── vacation_record.py
│   └── vacation_summary_dto.py
│
├── docs/                           # Documentation
│   ├── db_diagram.png             # Database schema diagram
│   ├── openapi.yaml               # OpenAPI specification
│   ├── pgsql-export.sql           # Database export with seed data
│   └── README.md                  # Documentation README
│
├── middleware/                     # Custom middleware
│   └── auth.py                    # Authentication and authorization decorators
│
├── migrations/                     # Database migrations (Alembic)
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/                  # Migration versions
│
├── models/                         # SQLAlchemy database models
│   ├── __init__.py
│   ├── role.py                    # Role model
│   ├── timestamp_mixin.py         # Timestamp mixin (created_at, updated_at)
│   ├── user.py                    # User model
│   ├── vacation_entitlement.py    # Vacation entitlement model
│   └── vacation_record.py         # Vacation record model
│
├── repositories/                   # Data access layer
│   ├── __init__.py
│   ├── base_repository.py         # Base repository with common operations
│   ├── role_repository.py         # Role repository
│   ├── user_repository.py         # User repository
│   ├── vacation_entitlement_repository.py
│   └── vacation_record_repository.py
│
├── routes/                         # API route handlers
│   ├── imports.py                 # CSV import routes
│   ├── users.py                   # User management routes
│   └── vacation.py                # Vacation management routes
│
├── seeders/                        # Database seeders
│   ├── __init__.py
│   ├── role_seeder.py             # Role seeder
│   └── user_seeder.py             # User seeder
│
├── services/                       # Business logic layer
│   ├── __init__.py
│   ├── import_service.py          # CSV import service
│   ├── user_service.py            # User management service
│   └── vacation_service.py        # Vacation management service
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and configuration
│   ├── README.md                  # Test documentation
│   ├── test_import_routes.py      # Import routes tests
│   ├── test_users_routes.py       # User routes tests
│   └── test_vacation_routes.py    # Vacation routes tests
│
└── utils/                          # Utility functions
    ├── file_helper.py             # File handling utilities
    ├── import_helper.py           # CSV import utilities
    ├── password.py                # Password hashing utilities
    └── response.py                # API response utilities
```

## Project Overview

### Description

This is a Flask-based REST API application for managing employee vacation requests and entitlements. The application provides functionality for:

- **User Management**: Create, read, update users with role-based access control
- **Vacation Management**: Create vacation records, check overlaps, manage entitlements
- **Bulk Import**: Import users, vacation records, and entitlements from CSV files
- **Role-Based Access Control**: Admin and Employee roles with different permissions

### Key Features

- **RESTful API**: Clean REST API design with proper HTTP status codes
- **Authentication**: Basic Authentication with password hashing using Werkzeug
- **Authorization**: Role-based access control (Admin/Employee)
- **Database Migrations**: Alembic for database schema versioning
- **Dependency Injection**: Flask-Injector for clean dependency management
- **Data Validation**: Pydantic models for request/response validation
- **CSV Import**: Bulk import functionality for users, vacations, and entitlements
- **Comprehensive Testing**: Full test suite with pytest

### Technology Stack

- **Framework**: Flask 2.x
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Flask-Migrate (Alembic)
- **Validation**: Pydantic
- **Dependency Injection**: Flask-Injector
- **Testing**: pytest, pytest-flask, pytest-cov
- **Password Hashing**: Werkzeug Security
- **Environment Management**: python-dotenv

### API Endpoints

#### Users
- `POST /users` - Create new user (Admin only)
- `GET /users` - List users with pagination (Admin only)
- `GET /users/{id}` - Get user by ID (Admin or owner)
- `PATCH /users/{id}` - Update user (Admin or owner)

#### Vacations
- `GET /vacation/users/{id}/summary` - Get vacation summary
- `POST /vacation/users/{id}/check` - Check date overlap
- `POST /vacation/users/{id}/create` - Create vacation record
- `POST /vacation/users/{id}/entitlements` - Create vacation entitlement
- `GET /vacation/users/{id}/records` - List vacation records

#### Imports
- `POST /import/users` - Import users from CSV (Admin only)
- `POST /import/vacations` - Import vacation records from CSV (Admin only)
- `POST /import/entitlements` - Import entitlements from CSV (Admin only)

### Testing

Run the test suite:

```bash
pytest
```

For detailed test documentation, see [tests/README.md](tests/README.md)

### Documentation

- **API Documentation**: See `docs/openapi.yaml` for OpenAPI specification
- **Database Schema**: See `docs/pgsql-export.sql` for database structure
- **Test Documentation**: See `tests/README.md` for test suite details

## Git Workflow

This project follows a three-branch Git workflow to ensure code quality and proper testing before deployment:

### Branch Structure

- **`main`**: Production-ready code that has passed all tests and quality checks
  - Contains stable, tested features
  - Protected branch - only merges from `qa` branch
  - All code in `main` has passed comprehensive testing

- **`qa`**: Quality assurance branch containing features ready for testing
  - Contains complete features that are ready for QA testing
  - Merges from `dev` branch after feature completion
  - All features in `qa` should be fully implemented and documented

- **`dev`**: Development branch where active development happens
  - Developers create feature branches from `dev`
  - Feature branches are merged back into `dev` after code review
  - `dev` branch is merged into `qa` when features are complete
  - `qa` branch is merged into `main` after successful testing

### Workflow Process

1. **Feature Development**:
   ```bash
   git checkout dev
   git pull origin dev
   git checkout -b feature/your-feature-name
   # ... make changes ...
   git commit -m "Add feature: description"
   git push origin feature/your-feature-name
   # Create pull request to merge into dev
   ```

2. **Merge to QA**:
   ```bash
   git checkout qa
   git pull origin qa
   git merge dev
   git push origin qa
   # Run tests and QA checks
   ```

3. **Merge to Main**:
   ```bash
   git checkout main
   git pull origin main
   git merge qa
   git push origin main
   # Deploy to production
   ```

### Branch Protection Rules

- `main` branch requires:
  - All tests must pass
  - Code review approval
  - No direct commits (only merges from `qa`)

- `qa` branch requires:
  - All tests must pass
  - Code review approval
  - No direct commits (only merges from `dev`)

## Future Improvements and Roadmap

The following improvements are planned for future development:

### 1. Code Refactoring

- **DTO Class Naming**: Refactor DTO class names for better consistency and clarity
  - Standardize naming conventions (e.g., `CreateUserRequest` → `UserCreateRequest`)
  - Ensure all DTOs follow the same naming pattern
  - Improve DTO organization and structure

### 2. Security Enhancements

- **Rate Limiting**: Implement rate limiting per IP address to prevent abuse
  - Add rate limiting middleware using Flask-Limiter
  - Configure limits for different endpoints (e.g., login attempts, API calls)
  - Implement IP-based throttling to prevent brute force attacks
  - Add configuration for different rate limits per user role

- **Additional Security Measures**:
  - Implement JWT tokens for stateless authentication
  - Add CORS configuration for production
  - Implement request validation and sanitization
  - Add security headers (HSTS, CSP, etc.)

### 3. ETL Improvements

- **Enhanced CSV Processing**:
  - Support more diverse CSV file formats (different delimiters, encodings, etc.)
  - Improve data validation and error handling
  - Add support for Excel files (.xlsx, .xls)
  - Implement data transformation pipelines

- **Distributed Processing**:
  - Integrate Apache Spark for large-scale data processing
  - Implement cluster-based processing for bulk imports
  - Add support for parallel processing of large CSV files
  - Optimize memory usage for large file imports

- **ETL Pipeline Enhancements**:
  - Add data quality checks and validation
  - Implement data transformation rules
  - Add support for incremental imports
  - Create ETL monitoring and logging

### 4. Database Performance Optimization

- **Index Creation**:
  - Add indexes on frequently queried columns:
    - `year` column in `vacation_records` table
    - `user_id` in `vacation_records` and `vacation_entitlements`
    - `email` in `users` table (already unique, but ensure index exists)
    - `deleted_at` for soft delete queries
    - Composite indexes for common query patterns

- **Query Optimization**:
  - Optimize queries with soft delete filters (`deleted_at IS NULL`)
  - Add partial indexes for active records
  - Implement query result caching where appropriate
  - Add database query monitoring and profiling

- **Database Consistency**:
  - Implement database-level constraints for data integrity
  - Add foreign key constraints with proper cascade rules
  - Implement database triggers for audit logging
  - Add database-level validation rules

### 5. Database-Level Improvements

- **Soft Delete Consistency**:
  - Standardize soft delete implementation across all tables
  - Ensure all queries properly filter deleted records
  - Add database-level constraints to prevent inconsistencies
  - Implement cascade soft delete for related records

- **Update Consistency**:
  - Ensure `updated_at` is automatically updated on all tables
  - Add database triggers for automatic timestamp updates
  - Implement optimistic locking for concurrent updates
  - Add version tracking for audit purposes

### 6. Additional Routes and Features

- **New API Endpoints**:
  - `GET /users/{id}/vacations` - Get all vacations for a user
  - `GET /vacation/statistics` - Get vacation statistics (admin only)
  - `POST /vacation/users/{id}/cancel` - Cancel a vacation record
  - `PATCH /vacation/users/{id}/records/{record_id}` - Update vacation record
  - `GET /import/history` - Get import history (admin only)
  - `GET /health/detailed` - Detailed health check with database status

- **Reporting Features**:
  - Vacation usage reports
  - User activity reports
  - Import history and statistics
  - Export functionality for reports

### 7. Testing Improvements

- **Test Coverage**:
  - Increase test coverage to 90%+
  - Add integration tests
  - Add performance tests
  - Add security tests

- **Test Infrastructure**:
  - Set up CI/CD pipeline
  - Add automated test running on pull requests
  - Implement test coverage reporting
  - Add load testing

### 8. Documentation

- **API Documentation**:
  - Complete OpenAPI specification
  - Add more examples and use cases
  - Create API client libraries

- **Developer Documentation**:
  - Architecture documentation
  - Database schema documentation
  - Deployment guides
  - Contributing guidelines

### Implementation Priority

1. **High Priority**:
   - Database indexes for performance
   - Rate limiting for security
   - DTO naming refactoring

2. **Medium Priority**:
   - Enhanced CSV processing
   - Additional API routes
   - Database consistency improvements

3. **Low Priority**:
   - Spark integration
   - Advanced reporting features
   - Performance optimizations
