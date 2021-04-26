from flask import render_template, jsonify, redirect, url_for, flash, request

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user

from __init__ import create_app
from extensions import db, login_manager
from model import General, About, Experience, Education, Skills, Project
from form import GeneralForm, AboutForm, ExperienceForm, EducationForm, SkillsForm, ProjectForm, RegisterForm, LoginForm, AccountForm

app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return General.query.get(int(user_id))


@app.route("/")
@login_required
def home():
    general = General.query.get(current_user.id)
    about = About.query.filter_by(general_id=current_user.id).first()
    experiences = Experience.query.filter_by(general_id=current_user.id)
    education = Education.query.filter_by(general_id=current_user.id)
    skills = Skills.query.filter_by(general_id=current_user.id).first()
    projects = Project.query.filter_by(general_id=current_user.id)
    return render_template("index.html", general_info=general, about_info=about, experiences=experiences, education_list=education, skills=skills, projects=projects)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        user = General.query.filter_by(email=email).first()
        if user:
            flash("This user already exist. Log in instead!")
            return redirect(url_for("login"))

        hash_pw = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)

        new_user = General(
            name=form.name.data,
            password=hash_pw,
            email=form.email.data,
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for("home"))

    return render_template("login_register.html", title="Register", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = General.query.filter_by(email=email).first()

        if not user:
            flash("Email does not exist. Please try again or register.")
            return redirect(url_for("login"))

        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Password incorrect, please try again.")
            return redirect(url_for("login"))

    return render_template("login_register.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/general", methods=["GET", "POST"])
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="General", ckEditor=True)


@app.route("/edit-general", methods=["GET", "POST"])
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
        return redirect(url_for("home"))
    return render_template("form_template.html", form=edit_general, title="General", ckEditor=True)


@app.route("/about", methods=["GET", "POST"])
@login_required
def about():
    form = AboutForm()
    if request.method == "POST" and form.validate_on_submit():
        file = request.files['image']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        else:
            file.filename = None
        new_about = About(
            intro=form.intro.data,
            image=file.filename,
            section_one=form.section_one.data,
            skills_work=form.skills_work.data,
            section_two=form.section_two.data,
            skills_goto=form.skills_goto.data,
            general=current_user,
        )
        db.session.add(new_about)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="About")


@app.route("/edit-about", methods=["GET", "POST"])
@login_required
def edit_about():
    about_info = About.query.filter_by(general_id=current_user.id).first()
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


@app.route("/delete-about")
@login_required
def delete_about():
    about_info = About.query.filter_by(general_id=current_user.id).first()
    db.session.delete(about_info)
    db.session.commit()
    return redirect((url_for("home")))


@app.route("/experience", methods=["GET", "POST"])
@login_required
def add_experience():
    #Refactor later with authentication and login
    form = ExperienceForm()
    if request.method == "POST" and form.validate_on_submit():
        new_experience = Experience(
            name=form.name.data,
            position=form.position.data,
            time=form.time.data,
            link=form.link.data,
            description=form.description.data,
            general=current_user,
        )
        db.session.add(new_experience)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="Experience", ckEditor=True)


@app.route('/edit-experience/<int:id>', methods=["GET", "POST"])
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=edit_experience, title="Experience", ckEditor=True)


@app.route('/delete-experience/<int:id>')
@login_required
def delete_experience(id):
    experience_info = Experience.query.get(id)
    db.session.delete(experience_info)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/education", methods=["GET", "POST"])
@login_required
def add_education():
    # Refactor later with authentication and login
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="Education")


@app.route('/edit-education/<int:id>', methods=["GET", "POST"])
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=edit_education, title="Education")


@app.route('/delete-education/<int:id>', methods=["GET", "POST"])
@login_required
def delete_education(id):
    education_info = Education.query.get(id)
    db.session.delete(education_info)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/skills", methods=["GET", "POST"])
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="Skills")


@app.route("/edit-skills", methods=["GET", "POST"])
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
        return redirect(url_for("home"))

    return render_template("form_template.html", form=edit_skills, title="Skills")


@app.route("/delete-skills")
@login_required
def delete_skills():
    skills_info = Skills.query.filter_by(general_id=current_user.id).first()
    db.session.delete(skills_info)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/project", methods=["GET", "POST"])
@login_required
def add_project():
    form = ProjectForm()
    if request.method == "POST" and form.validate_on_submit():
        file = request.files['screenshot']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        else:
            file.filename = None
        new_project = Project(
            name=form.name.data,
            link=form.link.data,
            github_link=form.github_link.data,
            screenshot=file.filename,
            description=form.description.data,
            tech_list=form.tech_list.data,
            general=current_user,
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("form_template.html", form=form, title="Project")


@app.route("/edit-project/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):
    project_info = Project.query.get(id)
    image = project_info.screenshot
    edit_project = ProjectForm(
        name=project_info.name,
        link=project_info.link,
        github_link=project_info.github_link,
        screenshot=None,
        description=project_info.description,
        tech_list=project_info.tech_list,
    )
    if edit_project.validate_on_submit():
        file = request.files['screenshot']
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            project_info.screenshot = file.filename
        project_info.name = edit_project.name.data
        project_info.link = edit_project.link.data
        project_info.github_link = edit_project.github_link.data
        project_info.description = edit_project.description.data
        project_info.tech_list = edit_project.tech_list.data
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("form_template.html", form=edit_project, title="Project", image=image)


@app.route("/delete-project/<int:id>")
@login_required
def delete_project(id):
    project_info = Project.query.get(id)
    db.session.delete(project_info)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/my-account", methods=["GET", "POST"])
@login_required
def my_account():
    user_info = General.query.get(current_user.id)
    form = AccountForm(
        name=user_info.name,
        email=user_info.email,
        password=None,
        api_key=user_info.api_key,
    )
    if form.validate_on_submit():
        message = ""
        if form.password.data:
            hash_pw = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)
            user_info.password = hash_pw
            message += "Password change has been saved."
        user_info.name = form.name.data
        user_info.email = form.email.data
        user_info.api_key = form.api_key.data
        message += " All changes saved."
        flash(message)
        db.session.commit()
        return redirect(url_for("my_account"))
    return render_template("account.html", form=form)


@app.route('/json')
def json_reveal():
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
