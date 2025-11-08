from app import db
from models.user import User
from models.role import Role
from werkzeug.security import generate_password_hash

def seed_users():
    users = [
        {"email": "velimirovicaleksa001@gmail.com", "password": "aleksa", "full_name": "Aleksa Velimirovic", "role_id": 1},     
    ]

    for u in users:
        existing_user = User.query.filter_by(email=u["email"]).first()
        if not existing_user:
            user = User(
                email=u["email"],
                password=generate_password_hash(u["password"]),
                full_name=u["full_name"],
                role_id=u["role_id"]
            )
            db.session.add(user)

    db.session.commit()
    print("Users seeded successfully!")
