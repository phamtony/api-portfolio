from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config.from_object("config.DevelopmentConfig")

    from extensions import db, login_manager, ckeditor, bootstrap

    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        db.create_all()

    return app
