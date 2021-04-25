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
    front_text = CKEditorField("Hero Text")
    submit = SubmitField("Submit")


class AboutForm(FlaskForm):
    intro = CKEditorField("Intro")
    image = FileField()
    section_one = CKEditorField("Section One")
    skills_work = StringField("List skills, use ',' to separate.")
    section_two = CKEditorField("Section Two")
    skills_goto = StringField("List skills, use ',' to separate.")
    submit = SubmitField("Submit")


class ExperienceForm(FlaskForm):
    name = StringField("Company Name")
    position = StringField("Position")
    time = StringField("How long were you here for? eg. Apr. 2015 - Present")
    link = StringField("Company Link")
    description = CKEditorField("Job Description")
    submit = SubmitField("Submit")


class EducationForm(FlaskForm):
    school = StringField("School Name")
    time = StringField("Duration")
    degree = StringField("Degree")
    submit = SubmitField("Submit")


class SkillsForm(FlaskForm):
    language = StringField("Language")
    framework_library = StringField("Framework/Library")
    database = StringField("Database")
    misc = StringField("Misc")
    submit = SubmitField("Submit")


class ProjectForm(FlaskForm):
    name = StringField("Project Name")
    link = StringField("Project Link")
    github_link = StringField("Github Link")
    screenshot = FileField()
    description = StringField("Project Description")
    tech_list = StringField("List Of Tech")
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class AccountForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    password = PasswordField("Change Password")
    api_key = StringField("API Key")
    submit = SubmitField("Save")
