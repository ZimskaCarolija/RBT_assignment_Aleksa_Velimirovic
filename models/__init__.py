from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .role import Role
from .vacation_entitlement import VacationEntitlement
from .vacation_record import VacationRecord
