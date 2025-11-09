from .role_seeder import seed_roles
from .user_seeder import seed_users

def seed_all():
    seed_roles().run()
    seed_users().run()
