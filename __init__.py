from flask import Flask

from api.api import json_return
from index.index import main_page
from register_login.register_login import register_login_page
from account.account import account_page
from general.general import general_page
from about.about import about_page
from experience.experience import experience_page
from education.education import education_page
from skills.skills import skills_page
from project.project import project_page

from models import General


def create_app():
    app = Flask(__name__)

    if app.config["ENV"] == "development":
        app.config.from_object("config.DevelopmentConfig")
    else:
        app.config.from_object("config.ProductionConfig")

    app.register_blueprint(json_return)
    app.register_blueprint(main_page)
    app.register_blueprint(account_page)
    app.register_blueprint(register_login_page)
    app.register_blueprint(general_page)
    app.register_blueprint(about_page)
    app.register_blueprint(experience_page)
    app.register_blueprint(education_page)
    app.register_blueprint(skills_page)
    app.register_blueprint(project_page)

    from extensions import db, login_manager, ckeditor

    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return General.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
