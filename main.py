from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
import os

from forms import GeneralForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/general", methods=["GET", "POST"])
def generalForm():
    form = GeneralForm()
    return render_template("general.html", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
