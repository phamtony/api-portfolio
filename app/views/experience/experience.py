from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from extensions import db
from models import Experience
from forms import ExperienceForm


experience_page = Blueprint("experience_page", __name__)


@experience_page.route("/experience", methods=["GET", "POST"])
@login_required
def add_experience():
    experience_query = Experience.query.filter_by(general_id=current_user.id)
    form = ExperienceForm()
    if request.method == "POST" and form.validate_on_submit():
        exp_query_count = 1
        if experience_query:
            exp_query_count = experience_query.count() + 1
        new_experience = Experience(
            name=form.name.data,
            position=form.position.data,
            time=form.time.data,
            link=form.link.data,
            description=form.description.data,
            general=current_user,
            order_exp=exp_query_count,
        )
        db.session.add(new_experience)
        db.session.commit()
        return redirect(url_for("main_page.home")+"#Experience")

    return render_template("form_page.html", form=form, title="Experience")


@experience_page.route("/edit-experience/<int:id>", methods=["GET", "POST"])
@login_required
def edit_experience(id):
    experience = Experience.query.get(id)
    edit_experience = ExperienceForm(
        name=experience.name,
        position=experience.position,
        time=experience.time,
        link=experience.link,
        description=experience.description,
    )
    if edit_experience.validate_on_submit():
        experience.name = edit_experience.name.data
        experience.position = edit_experience.position.data
        experience.time = edit_experience.time.data
        experience.link = edit_experience.link.data
        experience.description = edit_experience.description.data
        db.session.commit()
        return redirect(url_for("main_page.home")+"#Experience")

    return render_template("form_page.html", form=edit_experience, title="Experience")


@experience_page.route("/edit-experience-order")
@login_required
def edit_experience_order():
    experience_query_order_by = Experience.query.filter_by(general_id=current_user.id).order_by("order_exp")
    order_list = request.args.getlist("order", type=int)

    range_count = 0
    range_sequence = 1

    for exp in experience_query_order_by:
        exp.order_exp = order_list[range_count]
        range_count = range_count + 1

    for exp in experience_query_order_by:
        exp.order_exp = range_sequence
        range_sequence = range_sequence + 1

    db.session.commit()
    return redirect(url_for("main_page.home") + "#Experience")


@experience_page.route("/delete-experience/<int:id>")
@login_required
def delete_experience(id):
    experience_info = Experience.query.get(id)
    db.session.delete(experience_info)
    experience_query_order_by = Experience.query.filter_by(general_id=current_user.id).order_by("order_exp")
    range_count = 1
    for exp in experience_query_order_by:
        exp.order_exp = range_count
        range_count = range_count + 1

    db.session.commit()
    return redirect(url_for("main_page.home")+"#Experience")
