from flask_seeder import Seeder
from models.role import Role
from models import db

class seed_roles():
    def run(self):
        roles = [
            {"id": 1, "name": "Admin"},
            {"id": 2, "name": "Employee"}
        ]
        for role_data in roles:
            if not Role.query.filter_by(id=role_data["id"]).first():
                role = Role(id=role_data["id"], name=role_data["name"])
                db.session.add(role)
                print(f"Created role: {role_data['name']} (ID: {role_data['id']})")
        
        db.session.commit()
        print("Roles seeded successfully!")