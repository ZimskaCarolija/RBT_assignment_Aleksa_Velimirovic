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

```env
DEV_DATABASE_URL=postgresql://username:password@localhost:5432/database_name
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
UPLOAD_FOLDER=uploads
```

**Example `.env` file:**
```env
DEV_DATABASE_URL=postgresql://postgres:password@localhost:5432/rbt_db
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
UPLOAD_FOLDER=uploads
```

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
flask run
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