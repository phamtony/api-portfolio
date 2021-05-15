from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
import boto3
import boto3.session
from flask_cors import CORS

db = SQLAlchemy()
login_manager = LoginManager()
ckeditor = CKEditor()
s3_session = boto3.session.Session()
cors = CORS()

login_manager.login_view = "register_login_page.login"
login_manager.login_message = "You need to log in to view the page. If you're not registered, please register first."
