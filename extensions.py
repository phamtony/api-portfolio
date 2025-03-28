from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import boto3
import boto3.session
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
s3_session = boto3.session.Session()
cors = CORS()

login_manager.login_view = "register_login_page.login"
login_manager.login_message = "You need to log in to view the page. If you're not registered, please register first. <br><br> If you're here to just browse around and see how this works, please use these credentials: <br><br> Email: guest@guest.com <br> Password: guest"
