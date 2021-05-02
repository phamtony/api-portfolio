from flask import Blueprint, request, redirect, url_for, render_template, current_app
from flask_login import login_required, current_user
import os

from extensions import db
from models import About
from forms import AboutForm


about_page = Blueprint("about_page", __name__)


@about_page.route("/about", methods=["GET", "POST"])
@login_required
def about():
    form = AboutForm()
    if request.method == "POST" and form.validate_on_submit():
        file = request.files['image']
        if file:
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
        else:
            file.filename = None
        new_about = About(
            intro=form.intro.data,
            image=file.filename,
            general=current_user,
        )
        db.session.add(new_about)
        db.session.commit()
        return redirect(url_for("main_page.home")+"#About")

    return render_template("form_page.html", form=form, title="About", ckEditor=True)


@about_page.route("/edit-about", methods=["GET", "POST"])
@login_required
def edit_about():
    about_info = About.query.filter_by(general_id=current_user.id).first()
    image = about_info.image
    edit_about = AboutForm(
        intro=about_info.intro,
        image=None,
    )
    if edit_about.validate_on_submit():
        file = request.files['image']
        if file:
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
            about_info.image = file.filename
        about_info.intro = edit_about.intro.data
        db.session.commit()
        return redirect(url_for("main_page.home")+"#About")
    return render_template("form_page.html", form=edit_about, image=image, title="About", ckEditor=True)


@about_page.route("/delete-about")
@login_required
def delete_about():
    about_info = About.query.filter_by(general_id=current_user.id).first()
    db.session.delete(about_info)
    db.session.commit()
    return redirect(url_for("main_page.home")+"#About")
