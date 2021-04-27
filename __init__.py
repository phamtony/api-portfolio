from flask import Flask

from api.api import json_return
from index.index import main_page
from register_login.register_login import register_login_page
from account.account import account_page

from models import General


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "production":
        app.config.from_object("config.DevelopmentConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.DevelopmentConfig")

    app.register_blueprint(json_return)
    app.register_blueprint(main_page)
    app.register_blueprint(account_page)
    app.register_blueprint(register_login_page)

    from extensions import db, login_manager, ckeditor, bootstrap

    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return General.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
