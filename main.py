from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
import os

from model import db, General
from forms import GeneralForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///portfolio.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    general = General.query.all()
    print(general)
    return render_template("index.html", general_info=general)


@app.route("/general", methods=["GET", "POST"])
def generalForm():
    form = GeneralForm()
    if request.method == "POST" and form.validate_on_submit():
        new_portfolio = General(
            name=form.name.data,
            occupation=form.occupation.data,
            email=form.email.data,
            github=form.github.data,
            linkedin=form.linkedin.data,
        )
        db.session.add(new_portfolio)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("general.html", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
