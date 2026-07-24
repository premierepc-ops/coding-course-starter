import hashlib
import hmac
import os
import time
from collections import defaultdict

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from course_config import LEARNERS

course_auth_bp = Blueprint("course_auth", __name__, template_folder="templates")

login_manager = LoginManager()

MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 900
_login_attempts: dict[str, list[float]] = defaultdict(list)


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


def _stable_user_id(slug: str) -> int:
    digest = hashlib.sha256(slug.encode()).hexdigest()
    return int(digest[:7], 16) % 999_999 + 1


def user_from_learner(learner, is_admin=False):
    if is_admin:
        return CourseUser(0, "instructor", "Instructor", is_admin=True)
    slug = learner["slug"]
    return CourseUser(_stable_user_id(slug), slug, learner["name"], is_admin=False)


def _login_rate_key(kind: str, slug: str = "") -> str:
    addr = request.remote_addr or "unknown"
    return f"{addr}:{kind}:{slug}"


def _too_many_login_attempts(key: str) -> bool:
    now = time.time()
    recent = [t for t in _login_attempts[key] if now - t < LOGIN_WINDOW_SECONDS]
    _login_attempts[key] = recent
    return len(recent) >= MAX_LOGIN_ATTEMPTS


def _record_login_attempt(key: str) -> None:
    _login_attempts[key].append(time.time())


def _secrets_match(provided: str, expected: str) -> bool:
    if not expected:
        return False
    return hmac.compare_digest(provided.encode(), expected.encode())


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

    for learner in LEARNERS:
        if _stable_user_id(learner["slug"]) == uid:
            return user_from_learner(learner)
    return None


@course_auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("quiz.admin_view"))
        return redirect(url_for("home"))

    if request.method == "POST":
        if request.form.get("instructor") == "1":
            rate_key = _login_rate_key("instructor")
            if _too_many_login_attempts(rate_key):
                flash("Too many attempts. Wait a few minutes and try again.")
                return redirect(url_for("course_auth.login", instructor=1))

            password = request.form.get("password", "")
            expected = os.environ.get("INSTRUCTOR_PASSWORD", "")

            if _secrets_match(password, expected):
                login_user(CourseUser(0, "instructor", "Instructor", is_admin=True))
                _login_attempts.pop(rate_key, None)
                return redirect(url_for("quiz.admin_view"))

            _record_login_attempt(rate_key)
            flash("Wrong instructor password.")
            return redirect(url_for("course_auth.login", instructor=1))

        if not LEARNERS:
            flash(
                "No learners registered yet. Your instructor adds you in course_config.py "
                "or Railway Variables before sign-in works."
            )
            return redirect(url_for("course_auth.login"))

        slug = request.form.get("slug", "").strip()
        pin = request.form.get("pin", "").strip()
        rate_key = _login_rate_key("learner", slug)
        if _too_many_login_attempts(rate_key):
            flash("Too many attempts. Wait a few minutes and try again.")
            return redirect(url_for("course_auth.login"))

        learner = _learner_by_slug(slug)
        if not learner:
            flash("Pick your name from the list.")
            return redirect(url_for("course_auth.login"))

        expected_pin = _expected_learner_pin(learner)
        if _pin_required():
            if not expected_pin:
                flash("Student sign-in is not configured yet. Ask your instructor for help.")
                return redirect(url_for("course_auth.login"))
            if not _secrets_match(pin, expected_pin):
                _record_login_attempt(rate_key)
                flash("Wrong PIN. Ask your instructor if you forgot it.")
                return redirect(url_for("course_auth.login"))
        elif expected_pin and not _secrets_match(pin, expected_pin):
            _record_login_attempt(rate_key)
            flash("Wrong PIN.")
            return redirect(url_for("course_auth.login"))

        login_user(user_from_learner(learner))
        _login_attempts.pop(rate_key, None)
        next_page = request.args.get("next") or request.form.get("next")
        if next_page and next_page.startswith("/"):
            return redirect(next_page)
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
