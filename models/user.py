from . import db
from .timestamp_mixin import TimestampMixin
from werkzeug.security import check_password_hash, generate_password_hash

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

    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, value):
        self.password = value

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
