from flask import Blueprint, jsonify, request

from models import General, About, Experience, Education, Skills, Project


json_return = Blueprint("json_return", __name__)


@json_return.route("/json")
def api():
    api = request.args.get("api")
    id = General.query.filter_by(api_key=api).first().id

    skill_query = Skills.query.filter_by(general_id=id).first()
    about_query = About.query.filter_by(general_id=id).first()
    experience_query = Experience.query.filter_by(general_id=id).order_by("order_exp")
    education_query = Education.query.filter_by(general_id=id)
    project_query = Project.query.filter_by(general_id=id)

    try:
        general = General.query.get(id).serialized
    except AttributeError:
        general = {}

    try:
        skills = skill_query.serialized
    except AttributeError:
        skills = {}

    try:
        about = about_query.serialized
    except AttributeError:
        about = {}

    try:
        experience = [experience.serialized for experience in experience_query]
    except AttributeError:
        experience = {}

    try:
        education = [ed.serialized for ed in education_query]
    except AttributeError:
        education = {}

    try:
        projects = [project.serialized for project in project_query]
    except AttributeError:
        projects = []

    return jsonify(skills=skills, general=general, about=about, experience=experience, education=education, projects=projects)
