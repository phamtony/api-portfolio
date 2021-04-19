from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField
import email_validator

class GeneralForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    occupation = StringField("Occupation", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    github = StringField("Github")
    linkedin = StringField("Linkedin")
    submit = SubmitField("Submit")
