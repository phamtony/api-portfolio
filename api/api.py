from flask import Blueprint, jsonify, request

from models import General, About, Experience, Education, Skills, Project


json_return = Blueprint("json_return", __name__)


@json_return.route('/json')
def api():
    api = request.args.get("api")
    id = General.query.filter_by(api_key=api).first().id
    skill_query = Skills.query.filter_by(general_id=id).first()
    about_query = About.query.filter_by(general_id=id).first()
    experience_query = Experience.query.filter_by(general_id=id)
    education_query = Education.query.filter_by(general_id=id)
    project_query = Project.query.filter_by(general_id=id)

    general = General.query.get(id).to_dict()
    skills = skill_query.to_dict() if skill_query else {}
    about = about_query.to_dict() if about_query else {}
    experience = [experience.to_dict() for experience in experience_query] if experience_query else {}
    education = [ed.to_dict() for ed in education_query] if education_query else {}
    projects = [project.to_dict() for project in project_query] if project_query else {}

    return jsonify(skills=skills, general=general, about=about, experience=experience, education=education, projects=projects)
