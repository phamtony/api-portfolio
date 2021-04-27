from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from extensions import db
from models import General
from forms import AccountForm


account_page = Blueprint("account", __name__, template_folder="templates")


@account_page.route("/my-account", methods=["GET", "POST"])
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
        return redirect(url_for("account.my_account"))
    return render_template("account.html", form=form)
