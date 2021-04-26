from flask import Flask

from api.api import json_return

def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.DevelopmentConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    app.register_blueprint(json_return)

    from extensions import db, login_manager, ckeditor, bootstrap

    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        db.create_all()

    return app
