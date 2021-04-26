from flask import Flask
import os

def create_app():
    app = Flask(__name__)

    UPLOAD_FOLDER = './static/images/'
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from extensions import db, login_manager, ckeditor, bootstrap
    
    db.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        db.create_all()

    return app
