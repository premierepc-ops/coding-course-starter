import os

from dotenv import load_dotenv
from flask import Flask, abort, flash, redirect, render_template, request, url_for
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


def _use_secure_cookies() -> bool:
    """Secure cookies on Railway/HTTPS; allow HTTP localhost unless forced."""
    if os.environ.get("FORCE_INSECURE_COOKIES") == "1":
        return False
    if os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("RAILWAY_PROJECT_ID"):
        return True
    return os.environ.get("SESSION_COOKIE_SECURE", "").lower() in ("1", "true", "yes")


app.config["SESSION_COOKIE_SECURE"] = _use_secure_cookies()
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

from blueprints.course_auth import course_auth_bp, init_auth
from blueprints.aboutme import aboutme_bp
from blueprints.guestbook import guestbook_bp
from blueprints.quiz import quiz_bp
from course_dashboard import build_dashboard, build_nav, current_phase_for_user
from session_guides import SESSION_GUIDES, session_unlocked, session_url, sessions_for_nav
from start_guide import START_GUIDE
from tool_icons import TOOL_ICONS
from tools_guide import TOOLS_GUIDE
from course_config import LEARNERS

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


@app.route("/start")
def start_here():
    return _render_session(1)


@app.route("/session/<int:session_num>")
def session_guide(session_num):
    if session_num not in SESSION_GUIDES:
        abort(404)
    if session_num == 1:
        return redirect(url_for("start_here"))
    return _render_session(session_num)


def _render_session(session_num: int):
    is_instructor = bool(
        current_user
        and getattr(current_user, "is_authenticated", False)
        and getattr(current_user, "is_admin", False)
    )
    signed_in = bool(
        current_user
        and getattr(current_user, "is_authenticated", False)
        and not is_instructor
    )
    unlocked = 0
    if signed_in:
        unlocked = current_phase_for_user(current_user)
    elif is_instructor:
        unlocked = 6

    if not session_unlocked(session_num, unlocked, is_instructor, signed_in or session_num == 1):
        flash(f"Session {session_num} unlocks when you reach Phase {session_num} on Course Home.")
        return redirect(url_for("home"))

    all_sessions = sessions_for_nav(unlocked, is_instructor, signed_in or session_num == 1)
    next_session = next((s for s in all_sessions if s["num"] == session_num + 1), None)
    guide = SESSION_GUIDES[session_num]
    return render_template(
        "session.html",
        guide=guide,
        learners=LEARNERS if session_num == 1 else None,
        all_sessions=all_sessions,
        next_session=next_session,
    )


@app.route("/tools")
def tools_glossary():
    return render_template("tools.html", guide=TOOLS_GUIDE, icons=TOOL_ICONS)


@app.context_processor
def inject_nav():
    unlocked = 0
    if current_user and getattr(current_user, "is_authenticated", False):
        if getattr(current_user, "is_admin", False):
            unlocked = 6
        else:
            unlocked = current_phase_for_user(current_user)
    return {
        "nav": build_nav(current_user),
        "nav_active": request.endpoint,
        "unlocked_phase": unlocked,
    }


@app.template_global()
def display_of(username):
    from blueprints.quiz import get_learner

    learner = get_learner(username)
    return learner["name"] if learner else username


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    app.run(debug=debug)
