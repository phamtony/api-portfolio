from flask import Blueprint, flash, redirect, url_for, render_template, request
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db
from forms import RegisterForm, LoginForm
from models import General


register_login_page = Blueprint("register_login_page", __name__, template_folder="templates")


@register_login_page.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        user = General.query.filter_by(email=email).first()
        if user:
            flash("This user already exist. Log in instead!")
            return redirect(url_for("register_login_page.login"))

        hash_pw = generate_password_hash(form.password.data, method="pbkdf2:sha256", salt_length=8)

        new_user = General(
            name=form.name.data,
            password=hash_pw,
            email=form.email.data,
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for("main_page.home"))

    return render_template("login_register.html", title="Register", form=form)


@register_login_page.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_page.home"))
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = General.query.filter_by(email=email).first()

        if not user:
            flash("Email does not exist. Please try again or register.")
            return redirect(url_for("register_login_page.login"))

        if check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main_page.home"))
        else:
            flash("Password incorrect, please try again.")
            return redirect(url_for("register_login_page.login"))

    return render_template("login_register.html", title="Login", form=form)


@register_login_page.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("register_login_page.login"))
