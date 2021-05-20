import os


class Config(object):
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALLOWED_IMAGE_EXTENSIONS = ["PNG", "JPG", "JPEG", "GIF", "SVG"]

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024

    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_REGION = os.environ.get("S3_REGION")
    S3_IMAGE_PATH = os.environ.get("S3_IMAGE_PATH")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("://", "ql://", 1)
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
