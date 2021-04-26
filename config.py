import os


class Config(object):
    DEBUG = False
    TESTING = False

    UPLOAD_FOLDER = './static/images/'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False
