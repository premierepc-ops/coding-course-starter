from flask import Blueprint, render_template

aboutme_bp = Blueprint("aboutme", __name__, template_folder="templates")


@aboutme_bp.route("/")
def index():
    return render_template("aboutme/index.html", name="Your Name Here")
