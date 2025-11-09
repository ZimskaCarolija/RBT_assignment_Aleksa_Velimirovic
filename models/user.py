from . import db
from .timestamp_mixin import TimestampMixin
import bcrypt

class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    role_id = db.Column(db.SmallInteger, db.ForeignKey("roles.id"), nullable=False)

    role = db.relationship("Role", back_populates="users")
    vacation_entitlements = db.relationship("VacationEntitlement", back_populates="user")
    vacation_records = db.relationship("VacationRecord", back_populates="user")
