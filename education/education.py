from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from extensions import db
from models import Education
from forms import EducationForm


education_page = Blueprint("education_page", __name__)


@education_page.route("/education", methods=["GET", "POST"])
@login_required
def add_education():
    form = EducationForm()
    if request.method == "POST" and form.validate_on_submit():
        new_education = Education(
            school=form.school.data,
            time=form.time.data,
            degree=form.degree.data,
            general=current_user,
        )
        db.session.add(new_education)
        db.session.commit()
        return redirect(url_for("main_page.home")+"#Education")

    return render_template("form_page.html", form=form, title="Education")


@education_page.route('/edit-education/<int:id>', methods=["GET", "POST"])
@login_required
def edit_education(id):
    education = Education.query.get(id)
    edit_education = EducationForm(
        school=education.school,
        time=education.time,
        degree=education.degree,
    )
    if edit_education.validate_on_submit():
        education.school = edit_education.school.data
        education.time = edit_education.time.data
        education.degree = edit_education.degree.data
        db.session.commit()
        return redirect(url_for("main_page.home")+"#Education")

    return render_template("form_page.html", form=edit_education, title="Education")


@education_page.route('/delete-education/<int:id>', methods=["GET", "POST"])
@login_required
def delete_education(id):
    education_info = Education.query.get(id)
    db.session.delete(education_info)
    db.session.commit()
    return redirect(url_for("main_page.home")+"#Education")
