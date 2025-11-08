from . import db

class VacationRecord(db.Model):
    __tablename__ = "vacation_records"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days_count = db.Column(db.SmallInteger, nullable=False)
    year = db.Column(db.SmallInteger, nullable=False)
    note = db.Column(db.Text, nullable=True)

    user = db.relationship("User", back_populates="vacation_records")
