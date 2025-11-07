from . import db

class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    users = db.relationship("User", back_populates="role")
