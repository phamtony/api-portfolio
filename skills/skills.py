from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from extensions import db
from models import Skills
from forms import SkillsForm


skills_page = Blueprint("skills_page", __name__)


@skills_page.route("/skills", methods=["GET", "POST"])
@login_required
def skills():
    form = SkillsForm()
    if request.method == "POST" and form.validate_on_submit():
        new_skills = Skills(
            language=form.language.data,
            framework_library=form.framework_library.data,
            database=form.database.data,
            misc=form.misc.data,
            general=current_user,
        )
        db.session.add(new_skills)
        db.session.commit()
        return redirect(url_for("main_page.home"))

    return render_template("form_template.html", form=form, title="Skills")


@skills_page.route("/edit-skills", methods=["GET", "POST"])
@login_required
def edit_skills():
    skills_info = Skills.query.filter_by(general_id=current_user.id).first()
    edit_skills = SkillsForm(
        language=skills_info.language,
        framework_library=skills_info.framework_library,
        database=skills_info.database,
        misc=skills_info.misc,
    )

    if edit_skills.validate_on_submit():
        skills_info.language = edit_skills.language.data
        skills_info.framework_library = edit_skills.framework_library.data
        skills_info.database = edit_skills.database.data
        skills_info.misc = edit_skills.misc.data
        db.session.commit()
        return redirect(url_for("main_page.home"))

    return render_template("form_template.html", form=edit_skills, title="Skills")


@skills_page.route("/delete-skills")
@login_required
def delete_skills():
    skills_info = Skills.query.filter_by(general_id=current_user.id).first()
    db.session.delete(skills_info)
    db.session.commit()
    return redirect(url_for("main_page.home"))
