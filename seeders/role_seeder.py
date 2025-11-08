from app import db
from models.role import Role

def seed_roles():
    roles = ["Admin", "Employee"]

    for role_name in roles:
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            role = Role(name=role_name)
            db.session.add(role)

    db.session.commit()
    print("Roles seeded successfully!")
