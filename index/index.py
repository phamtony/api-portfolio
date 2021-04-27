from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import General, About, Experience, Education, Skills, Project


main_page = Blueprint("main_page", __name__, template_folder="templates")


@main_page.route("/")
@login_required
def home():
    general = General.query.get(current_user.id)
    about = About.query.filter_by(general_id=current_user.id).first()
    experiences = Experience.query.filter_by(general_id=current_user.id)
    education = Education.query.filter_by(general_id=current_user.id)
    skills = Skills.query.filter_by(general_id=current_user.id).first()
    projects = Project.query.filter_by(general_id=current_user.id)
    return render_template("index.html", general_info=general, about_info=about, experiences=experiences, education_list=education, skills=skills, projects=projects)