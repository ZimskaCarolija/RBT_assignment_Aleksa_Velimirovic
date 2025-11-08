from . import db
from .timestamp_mixin import TimestampMixin

class VacationEntitlement(TimestampMixin, db.Model):
    __tablename__ = "vacation_entitlements"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    year = db.Column(db.SmallInteger, nullable=False)
    total_days = db.Column(db.SmallInteger, nullable=True)

    user = db.relationship("User", back_populates="vacation_entitlements")

    __table_args__ = (
        db.UniqueConstraint("user_id", "year", name="uq_user_year"),
    )
