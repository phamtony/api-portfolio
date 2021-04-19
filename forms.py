from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField
import email_validator

class GeneralForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    occupation = StringField("Occupation")
    email = StringField("Email", validators=[Email()])
    github = StringField("Github")
    linkedin = StringField("Linkedin")
    submit = SubmitField("Submit")


class AboutForm(FlaskForm):
    intro = CKEditorField("Intro")
    image = FileField()
    section_one = CKEditorField("Section One")
    skills_work = StringField("List skills, use ',' to separate.")
    section_two = CKEditorField("Section Two")
    skills_goto = StringField("List skills, use ',' to separate.")
    submit = SubmitField("Submit")
