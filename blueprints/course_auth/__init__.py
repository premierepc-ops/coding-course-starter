import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from course_config import LEARNERS

course_auth_bp = Blueprint("course_auth", __name__, template_folder="templates")

login_manager = LoginManager()


class CourseUser(UserMixin):
    def __init__(self, user_id, slug, name, is_admin=False):
        self.id = user_id
        self.slug = slug
        self.username = slug
        self.name = name
        self.is_admin = is_admin
        self.email = None


def _learner_by_slug(slug):
    for learner in LEARNERS:
        if learner["slug"] == slug:
            return learner
    return None


def _expected_learner_pin(learner):
    """PIN from Railway/local env, or optional per-learner pin in course_config (local dev)."""
    env_pin = os.environ.get("LEARNER_PIN", "").strip()
    if env_pin:
        return env_pin
    return str(learner.get("pin", "")).strip()


def _pin_required():
    """Production deploys must set LEARNER_PIN so sign-in is not honor-system."""
    if os.environ.get("LEARNER_PIN", "").strip():
        return True
    if os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get("RAILWAY_PROJECT_ID"):
        return True
    return False


def user_from_learner(learner, is_admin=False):
    user_id = LEARNERS.index(learner) + 1
    return CourseUser(user_id, learner["slug"], learner["name"], is_admin)


def init_auth(app):
    login_manager.init_app(app)
    login_manager.login_view = "course_auth.login"
    login_manager.login_message = "Sign in to continue."


@login_manager.user_loader
def load_user(user_id):
    try:
        uid = int(user_id)
    except (TypeError, ValueError):
        return None
    if uid == 0:
        return CourseUser(0, "instructor", "Instructor", is_admin=True)
    if 1 <= uid <= len(LEARNERS):
        return user_from_learner(LEARNERS[uid - 1])
    return None


@course_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("quiz.admin_view"))
        return redirect(url_for("home"))

    if request.method == "POST":
        if request.form.get("instructor") == "1":
            password = request.form.get("password", "")
            expected = os.environ.get("INSTRUCTOR_PASSWORD", "")
            if expected and password == expected:
                login_user(CourseUser(0, "instructor", "Instructor", is_admin=True))
                return redirect(url_for("quiz.admin_view"))
            flash("Wrong instructor password.")
            return redirect(url_for("course_auth.login", instructor=1))

        if not LEARNERS:
            flash("No learners registered yet. Add yourself to course_config.py in your fork.")
            return redirect(url_for("course_auth.login"))

        slug = request.form.get("slug", "").strip()
        pin = request.form.get("pin", "").strip()
        learner = _learner_by_slug(slug)
        if not learner:
            flash("Pick your name from the list.")
            return redirect(url_for("course_auth.login"))

        expected_pin = _expected_learner_pin(learner)
        if _pin_required():
            if not expected_pin:
                flash("Student sign-in is not configured yet. Ask your instructor to set LEARNER_PIN on Railway.")
                return redirect(url_for("course_auth.login"))
            if pin != expected_pin:
                flash("Wrong PIN. Ask your instructor if you forgot it.")
                return redirect(url_for("course_auth.login"))
        elif expected_pin and pin != expected_pin:
            flash("Wrong PIN.")
            return redirect(url_for("course_auth.login"))

        login_user(user_from_learner(learner))
        return redirect(url_for("home"))

    show_instructor = request.args.get("instructor") == "1"
    pin_required = _pin_required()
    return render_template(
        "course_auth/login.html",
        learners=LEARNERS,
        show_instructor=show_instructor,
        pin_required=pin_required,
    )


@course_auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
