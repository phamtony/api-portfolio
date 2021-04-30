from flask import Blueprint, request, redirect, url_for, render_template, current_app
from flask_login import login_required, current_user
import os

from extensions import db
from models import Project
from forms import ProjectForm


project_page = Blueprint("project_page", __name__)


@project_page.route("/project", methods=["GET", "POST"])
@login_required
def add_project():
    form = ProjectForm()
    if request.method == "POST" and form.validate_on_submit():
        file = request.files['screenshot']
        if file:
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
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
        return redirect(url_for("main_page.home")+"#Project")

    return render_template("form_page.html", form=form, title="Project")


@project_page.route("/edit-project/<int:id>", methods=["GET", "POST"])
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
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
            project_info.screenshot = file.filename
        project_info.name = edit_project.name.data
        project_info.link = edit_project.link.data
        project_info.github_link = edit_project.github_link.data
        project_info.description = edit_project.description.data
        project_info.tech_list = edit_project.tech_list.data
        db.session.commit()
        return redirect(url_for("main_page.home")+"#Project")

    return render_template("form_page.html", form=edit_project, title="Project", image=image)


@project_page.route("/delete-project/<int:id>")
@login_required
def delete_project(id):
    project_info = Project.query.get(id)
    db.session.delete(project_info)
    db.session.commit()
    return redirect(url_for("main_page.home")+"#Project")