from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from extensions import db
from models import General
from forms import GeneralForm


general_page = Blueprint("general_page", __name__)


@general_page.route("/general", methods=["GET", "POST"])
@login_required
def general():
    form = GeneralForm()
    if request.method == "POST" and form.validate_on_submit():
        new_general = General(
            name=form.name.data,
            occupation=form.occupation.data,
            email=form.email.data,
            github=form.github.data,
            linkedin=form.linkedin.data,
            front_text=form.front_text.data,
        )
        db.session.add(new_general)
        db.session.commit()
        return redirect(url_for("main_page.home"))

    return render_template("form_page.html", form=form, title="General", ckEditor=True)


@general_page.route("/edit-general", methods=["GET", "POST"])
@login_required
def edit_general():
    general_info = General.query.get(current_user.id)
    edit_general = GeneralForm(
        name=general_info.name,
        occupation=general_info.occupation,
        email=general_info.email,
        github=general_info.github,
        linkedin=general_info.linkedin,
        front_text=general_info.front_text,
    )
    if edit_general.validate_on_submit():
        general_info.name = edit_general.name.data
        general_info.occupation = edit_general.occupation.data
        general_info.email = edit_general.email.data
        general_info.github = edit_general.github.data
        general_info.linkedin = edit_general.linkedin.data
        general_info.front_text = edit_general.front_text.data
        db.session.commit()
        return redirect(url_for("main_page.home"))
    return render_template("form_page.html", form=edit_general, title="General", ckEditor=True)