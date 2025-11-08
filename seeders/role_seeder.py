from flask_seeder import Seeder
from models.role import Role
from models import db

class seed_roles():
    def run(self):
        roles = ["Admin", "Employee"]
        for role_name in roles:
            if not Role.query.filter_by(name=role_name).first():
                role = Role(name=role_name)
                db.session.add(role)
        db.session.commit()
