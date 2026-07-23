import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_login import current_user
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)

if not os.environ.get("SECRET_KEY"):
    raise RuntimeError(
        "Missing SECRET_KEY. Set it in Railway Variables or a local .env file "
        "(copy from .env.example)."
    )

app.secret_key = os.environ["SECRET_KEY"]
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

from blueprints.course_auth import course_auth_bp, init_auth
from blueprints.aboutme import aboutme_bp
from blueprints.guestbook import guestbook_bp
from blueprints.quiz import quiz_bp
from course_dashboard import build_dashboard

init_auth(app)

app.register_blueprint(course_auth_bp, url_prefix="/")
app.register_blueprint(aboutme_bp, url_prefix="/aboutme")
app.register_blueprint(guestbook_bp, url_prefix="/guestbook")
app.register_blueprint(quiz_bp, url_prefix="/quiz")


@app.route("/healthz")
def healthz():
    return "ok", 200


@app.route("/")
def home():
    ctx = build_dashboard(current_user, request.host)
    return render_template("index.html", **ctx)


@app.template_global()
def display_of(username):
    from blueprints.quiz import get_learner

    learner = get_learner(username)
    return learner["name"] if learner else username


if __name__ == "__main__":
    app.run(debug=True)
