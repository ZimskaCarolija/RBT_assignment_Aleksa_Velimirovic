from .development import DevelopmentConfig

class TestConfig(DevelopmentConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False

