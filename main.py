from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
import os

from model import db, General, About
from forms import GeneralForm, AboutForm

UPLOAD_FOLDER = './static/images/'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

#Refactor later with authentication and login
user_id = 1

@app.route("/")
def home():
    general = General.query.get(user_id)
    about = About.query.get(user_id)
    return render_template("index.html", general_info=general, about_info=about)


@app.route("/general", methods=["GET", "POST"])
def general():
    form = GeneralForm()
    if request.method == "POST" and form.validate_on_submit():
        new_general = General(
            name=form.name.data,
            occupation=form.occupation.data,
            email=form.email.data,
            github=form.github.data,
            linkedin=form.linkedin.data,
        )
        db.session.add(new_general)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("general.html", form=form)


@app.route("/edit-general", methods=["GET", "POST"])
def edit_general():
    general_info = General.query.get(user_id)
    edit_general = GeneralForm(
        name=general_info.name,
        occupation=general_info.occupation,
        email=general_info.email,
        github=general_info.github,
        linkedin=general_info.linkedin,
    )
    if edit_general.validate_on_submit():
        general_info.name = edit_general.name.data
        general_info.occupation = edit_general.occupation.data
        general_info.email = edit_general.email.data
        general_info.github = edit_general.github.data
        general_info.linkedin = edit_general.linkedin.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("general.html", form=edit_general)


@app.route("/about", methods=["GET", "POST"])
def about():
    form = AboutForm()
    if request.method == "POST" and form.validate_on_submit():
        # Fix the form later to upload instead of string path
        # file = request.files['image']
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        new_about = About(
            intro=form.intro.data,
            image=form.image.data,
            section_one=form.section_one.data,
            skills_work=form.skills_work.data,
            section_two=form.section_two.data,
            skills_goto=form.skills_goto.data,
        )
        db.session.add(new_about)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("about.html", form=form)


@app.route("/edit-about", methods=["GET", "POST"])
def edit_about():
    about_info = About.query.get(user_id)
    edit_about = AboutForm(
        intro=about_info.intro,
        image=about_info.image,
        section_one=about_info.section_one,
        skills_work=about_info.skills_work,
        section_two=about_info.section_two,
        skills_goto=about_info.skills_goto,
    )
    if edit_about.validate_on_submit():
        about_info.intro = edit_about.intro.data
        about_info.image = edit_about.image.data
        about_info.section_one = edit_about.section_one.data
        about_info.skills_work = edit_about.skills_work.data
        about_info.section_two = edit_about.section_two.data
        about_info.skills_goto = edit_about.skills_goto.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("about.html", form=edit_about)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
