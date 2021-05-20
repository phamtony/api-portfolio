from flask import Blueprint, request, redirect, url_for, render_template, current_app, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid

from extensions import db, s3_session
from portfolio_func import allowed_image, image_ext
from models import About
from forms import AboutForm


about_page = Blueprint("about_page", __name__)


@about_page.route("/about", methods=["GET", "POST"])
@login_required
def about():
    form = AboutForm()
    if request.method == "POST" and form.validate_on_submit():
        s3_client = s3_session.resource("s3")
        file = request.files["image"]

        if file:

            if file.filename == "":
                flash("Image must have file name.")
                return redirect(request.url)

            if not allowed_image(file.filename, current_app):
                flash("That image extension is not allowed.")
                return redirect(request.url)

            filename = secure_filename(str(uuid.uuid4())) + f".{image_ext(file.filename)}"
            s3_client.Bucket(current_app.config["S3_BUCKET"]).put_object(Key=filename, Body=file, ACL="public-read")

        else:
            filename = None

        new_about = About(
            intro=form.intro.data,
            image=filename,
            general=current_user,
        )

        db.session.add(new_about)
        db.session.commit()
        return redirect(url_for("main_page.home")+"#About")

    return render_template("form_page.html", form=form, title="About")


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
        s3_client = s3_session.resource("s3")
        file = request.files["image"]

        if file:

            if file.filename == "":
                flash("Image must have file name.")
                return redirect(request.url)

            if not allowed_image(file.filename, current_app):
                flash("That image extension is not allowed.")
                return redirect(request.url)

            try:
                s3_client.Object(current_app.config["S3_BUCKET"], image).delete()
            except:
                pass

            filename = secure_filename(str(uuid.uuid4())) + f".{image_ext(file.filename)}"
            s3_client.Bucket(current_app.config["S3_BUCKET"]).put_object(Key=filename, Body=file, ACL="public-read")
            about_info.image = filename

        about_info.intro = edit_about.intro.data
        db.session.commit()
        return redirect(url_for("main_page.home")+"#About")
    return render_template("form_page.html", form=edit_about, image=image, title="About")


@about_page.route("/delete-about")
@login_required
def delete_about():
    s3_client = s3_session.resource("s3")
    about_info = About.query.filter_by(general_id=current_user.id).first()
    image = about_info.image

    try:
        s3_client.Object(current_app.config["S3_BUCKET"], image).delete()
    except:
        pass

    db.session.delete(about_info)
    db.session.commit()
    return redirect(url_for("main_page.home")+"#About")
