from flask import Blueprint, render_template

main = Blueprint('main',__name__)

@main.route("/")
def home():
    return render_template("maintemplate/home.html", title = "home")

@main.route("/about")
def about():
    return render_template("maintemplate/about.html", title = "about")
