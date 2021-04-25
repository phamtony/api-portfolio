from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
bootstrap = Bootstrap()
