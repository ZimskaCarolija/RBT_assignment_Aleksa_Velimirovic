import pytest
import os
import shutil
from models import db
from app import create_app
from config.test import TestConfig
from models.user import User
from models.role import Role
from models.vacation_entitlement import VacationEntitlement
from models.vacation_record import VacationRecord
from utils.password import hash_password
import base64


@pytest.fixture(scope='function')
def app():
    app = create_app(TestConfig)
    upload_dir = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_dir, exist_ok=True)
    yield app
    if os.path.exists(upload_dir):
        shutil.rmtree(upload_dir, ignore_errors=True)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def admin_role(db_session):
    role = db_session.query(Role).filter_by(name="Admin").first()
    if role:
        return role
    role = Role(name="Admin")
    db_session.add(role)
    db_session.commit()
    return role


@pytest.fixture
def employee_role(db_session):
    role = db_session.query(Role).filter_by(name="Employee").first()
    if role:
        return role
    role = Role(name="Employee")
    db_session.add(role)
    db_session.commit()
    return role


@pytest.fixture
def admin_user(db_session, admin_role):
    user = db_session.query(User).filter_by(email="admin@test.com").first()
    if user:
        return user
    user = User(
        email="admin@test.com",
        password=hash_password("aleksa"),
        full_name="Admin User",
        role_id=admin_role.id
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def employee_user(db_session, employee_role):
    user = db_session.query(User).filter_by(email="employee@test.com").first()
    if user:
        return user
    user = User(
        email="employee@test.com",
        password=hash_password("employee123"),
        full_name="Employee User",
        role_id=employee_role.id
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def another_employee_user(db_session, employee_role):
    user = db_session.query(User).filter_by(email="employee2@test.com").first()
    if user:
        return user
    user = User(
        email="employee2@test.com",
        password=hash_password("employee123"),
        full_name="Employee 2 User",
        role_id=employee_role.id
    )
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def vacation_entitlement(db_session, employee_user):
    entitlement = db_session.query(VacationEntitlement).filter_by(
        user_id=employee_user.id,
        year=2025
    ).first()
    if entitlement:
        return entitlement
    entitlement = VacationEntitlement(
        user_id=employee_user.id,
        year=2025,
        total_days=25
    )
    db_session.add(entitlement)
    db_session.commit()
    return entitlement


@pytest.fixture
def vacation_record(db_session, employee_user):
    from datetime import date
    record = db_session.query(VacationRecord).filter_by(
        user_id=employee_user.id,
        start_date=date(2025, 7, 1),
        end_date=date(2025, 7, 5)
    ).first()
    if record:
        return record
    record = VacationRecord(
        user_id=employee_user.id,
        start_date=date(2025, 7, 1),
        end_date=date(2025, 7, 5),
        days_count=5,
        year=2025,
        note="Summer vacation"
    )
    db_session.add(record)
    db_session.commit()
    return record


def create_auth_header(email, password):
    credentials = f"{email}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded}"}


@pytest.fixture
def admin_auth_headers(admin_user):
    return create_auth_header("admin@test.com", "aleksa")


@pytest.fixture
def employee_auth_headers(employee_user):
    return create_auth_header("employee@test.com", "employee123")


@pytest.fixture
def another_employee_auth_headers(another_employee_user):
    return create_auth_header("employee2@test.com", "employee123")
