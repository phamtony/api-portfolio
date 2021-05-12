from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user

from extensions import db
from models import Education
from forms import EducationForm


education_page = Blueprint("education_page", __name__)


@education_page.route("/education", methods=["GET", "POST"])
@login_required
def add_education():
    education_query = Education.query.filter_by(general_id=current_user.id)
    form = EducationForm()
    if request.method == "POST" and form.validate_on_submit():
        ed_query_count = 1
        if education_query:
            ed_query_count = education_query.count() + 1
        new_education = Education(
            school=form.school.data,
            time=form.time.data,
            degree=form.degree.data,
            general=current_user,
            order_ed=ed_query_count,
        )
        db.session.add(new_education)
        db.session.commit()
        return redirect(url_for("main_page.home")+"#Education")

    return render_template("form_page.html", form=form, title="Education")


@education_page.route("/edit-education/<int:id>", methods=["GET", "POST"])
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


@education_page.route("/edit-education-order")
@login_required
def edit_education_order():
    education_query_order_by = Education.query.filter_by(general_id=current_user.id).order_by("order_ed")
    order_list = request.args.getlist("order", type=int)

    range_count = 0
    range_sequence = 1

    for ed in education_query_order_by:
        ed.order_ed = order_list[range_count]
        range_count = range_count + 1

    for ed in education_query_order_by:
        ed.order_ed = range_sequence
        range_sequence = range_sequence + 1

    db.session.commit()
    return redirect(url_for("main_page.home")+"#Education")


@education_page.route("/delete-education/<int:id>", methods=["GET", "POST"])
@login_required
def delete_education(id):
    education_info = Education.query.get(id)
    db.session.delete(education_info)
    education_query_order_by = Education.query.filter_by(general_id=current_user.id).order_by("order_ed")
    range_count = 1
    for ed in education_query_order_by:
        ed.order_ed = range_count
        range_count = range_count + 1

    db.session.commit()
    return redirect(url_for("main_page.home")+"#Education")
