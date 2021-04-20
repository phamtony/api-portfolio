from flask import Flask, render_template, jsonify, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
import os

from model import db, General, About, Experience, Education, Skills, Project
from forms import GeneralForm, AboutForm, ExperienceForm, EducationForm, SkillsForm, ProjectForm

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
# Be sure to show education and experience related to current ID.
user_id = 1


@app.route("/")
def home():
    general = General.query.get(user_id)
    about = About.query.get(user_id)
    experiences = Experience.query.all()
    education = Education.query.all()
    skills = Skills.query.get(user_id)
    return render_template("index.html", general_info=general, about_info=about, experiences=experiences, education_list=education, skills=skills)


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

    return render_template("form_template.html", form=form, title="General")


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
    return render_template("form_template.html", form=edit_general, title="General")


@app.route("/about", methods=["GET", "POST"])
def about():
    form = AboutForm()
    if request.method == "POST" and form.validate_on_submit():
        file = request.files['image']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        new_about = About(
            intro=form.intro.data,
            image=file.filename,
            section_one=form.section_one.data,
            skills_work=form.skills_work.data,
            section_two=form.section_two.data,
            skills_goto=form.skills_goto.data,
        )
        db.session.add(new_about)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="About")


@app.route("/edit-about", methods=["GET", "POST"])
def edit_about():
    about_info = About.query.get(user_id)
    image = about_info.image
    edit_about = AboutForm(
        intro=about_info.intro,
        image=None,
        section_one=about_info.section_one,
        skills_work=about_info.skills_work,
        section_two=about_info.section_two,
        skills_goto=about_info.skills_goto,
    )
    if edit_about.validate_on_submit():
        file = request.files['image']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            about_info.image = file.filename
        about_info.intro = edit_about.intro.data
        about_info.section_one = edit_about.section_one.data
        about_info.skills_work = edit_about.skills_work.data
        about_info.section_two = edit_about.section_two.data
        about_info.skills_goto = edit_about.skills_goto.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("form_template.html", form=edit_about, image=image, title="About")


@app.route("/experience", methods=["GET", "POST"])
def add_experience():
    #Refactor later with authentication and login
    general = General.query.get(user_id)
    form = ExperienceForm()
    if request.method == "POST" and form.validate_on_submit():
        new_experience = Experience(
            name=form.name.data,
            position=form.position.data,
            time=form.time.data,
            link=form.link.data,
            description=form.description.data,
            general=general,
        )
        db.session.add(new_experience)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="Experience")


@app.route("/education", methods=["GET", "POST"])
def add_education():
    # Refactor later with authentication and login
    general = General.query.get(user_id)
    form = EducationForm()
    if request.method == "POST" and form.validate_on_submit():
        new_education = Education(
            school=form.school.data,
            time=form.time.data,
            degree=form.degree.data,
            general=general,
        )
        db.session.add(new_education)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="Education")


@app.route('/experience/<int:id>', methods=["GET", "POST"])
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=edit_experience, title="Experience")


@app.route('/education/<int:id>', methods=["GET", "POST"])
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=edit_education, title="Education")


@app.route("/skills", methods=["GET", "POST"])
def skills():
    form = SkillsForm()
    if request.method == "POST" and form.validate_on_submit():
        new_skills = Skills(
            language=form.language.data,
            framework_library=form.framework_library.data,
            database=form.database.data,
            misc=form.misc.data,
        )
        db.session.add(new_skills)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="Skills")


@app.route("/edit-skills", methods=["GET", "POST"])
def edit_skills():
    skills_info = Skills.query.get(user_id)
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=edit_skills, title="Skills")


@app.route('/json-test')
def json_test():
    skills = Skills.query.get(user_id)
    return jsonify(skills=skills.to_dict())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
