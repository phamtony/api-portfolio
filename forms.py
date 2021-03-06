from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo
import email_validator


class GeneralForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    occupation = StringField("Occupation")
    email = StringField("Email", validators=[Email()])
    github = StringField("Github")
    linkedin = StringField("Linkedin")
    user_intro = TextAreaField("Intro", render_kw={"placeholder": "HTML markup or plain text"})


class AboutForm(FlaskForm):
    image = FileField("")
    intro = TextAreaField("About You", render_kw={"placeholder": "HTML markup or plain text"})


class ExperienceForm(FlaskForm):
    name = StringField("Company Name")
    position = StringField("Position")
    time = StringField("How long were you here for? eg. Apr. 2015 - Present")
    link = StringField("Company Link")
    description = TextAreaField("Experience Description")
    order_exp = HiddenField("")


class EducationForm(FlaskForm):
    school = StringField("School Name")
    time = StringField("Duration")
    degree = StringField("Degree")
    order_ed = HiddenField("")


class SkillsForm(FlaskForm):
    language = StringField("Language")
    framework_library = StringField("Framework/Library")
    database = StringField("Database")
    misc = StringField("Misc")


class ProjectForm(FlaskForm):
    screenshot = FileField()
    name = StringField("Project Name")
    link = StringField("Project Link")
    github_link = StringField("Github Link")
    description = TextAreaField("Project Description")
    tech_list = StringField("List Of Tech")
    order_project = HiddenField("")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Set Password", validators=[DataRequired(), EqualTo("confirm", message="Passwords must match.")])
    confirm = PasswordField("Confirm Password")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])


class AccountForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    password = PasswordField("Change Password", validators=[EqualTo("confirm", message="Passwords must match.")])
    confirm = PasswordField("Confirm Password")
    api_key = StringField("API Key")
