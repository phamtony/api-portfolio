import os


class Config(object):
    DEBUG = False
    TESTING = False

    UPLOAD_FOLDER = './static/images/'
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALLOWED_IMAGE_EXTENSIONS = ["PNG", "JPG", "JPEG", "GIF", "SVG"]

    SQLALCHEMY_DATABASE_URI = "sqlite:///portfolio.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # UPLOAD_FOLDER = ''


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///portfolio.db"
