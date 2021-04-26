from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
bootstrap = Bootstrap()

login_manager.login_view = "login"
login_manager.login_message = "You need to log in to view the page. If you're not registered, please register first."
