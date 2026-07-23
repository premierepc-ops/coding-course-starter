from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from course_config import LEARNERS
from session_feedback_store import list_feedback, save_feedback, summary_by_session
from session_guides import SESSION_GUIDES

session_feedback_bp = Blueprint("session_feedback", __name__, template_folder="templates")


def _step_label(session_num: int, step_num: int) -> str:
    if step_num == 0:
        return "Whole session / section"
    guide = SESSION_GUIDES.get(session_num)
    if not guide:
        return f"Step {step_num}"
    for step in guide.get("steps", []):
        if step.get("num") == step_num:
            return step["title"]
    return f"Step {step_num}"


def _session_label(session_num: int) -> str:
    if session_num == 0:
        return "Phase 0 — Meet your tools"
    guide = SESSION_GUIDES.get(session_num)
    return guide["title"] if guide else f"Session {session_num}"


@session_feedback_bp.route("/feedback", methods=["POST"])
@login_required
def submit_feedback():
    try:
        session_num = int(request.form.get("session_num", ""))
        step_num = int(request.form.get("step_num", ""))
    except ValueError:
        abort(400)

    worked = (request.form.get("worked") or "").strip()[:2000]
    didnt_work = (request.form.get("didnt_work") or "").strip()[:2000]
    if not worked and not didnt_work:
        flash("Add at least one note — what worked or what didn't.")
        return redirect(request.form.get("return_to") or url_for("home"))

    if getattr(current_user, "is_admin", False):
        author_role = "instructor"
        author_name = "Instructor"
        learner_slug = (request.form.get("learner_slug") or "").strip()
    else:
        author_role = "student"
        author_name = getattr(current_user, "name", "") or getattr(current_user, "slug", "")
        learner_slug = getattr(current_user, "slug", "") or ""

    save_feedback(
        session_num=session_num,
        step_num=step_num,
        learner_slug=learner_slug,
        author_role=author_role,
        author_name=author_name,
        worked=worked,
        didnt_work=didnt_work,
    )
    flash("Session notes saved — thank you. This helps us improve the course.")
    return redirect(request.form.get("return_to") or url_for("home"))


@session_feedback_bp.route("/instructor/session-feedback")
@login_required
def instructor_review():
    if not getattr(current_user, "is_admin", False):
        abort(403)

    session_filter = request.args.get("session")
    step_filter = request.args.get("step")
    session_num = int(session_filter) if session_filter and session_filter.isdigit() else None
    step_num = int(step_filter) if step_filter and step_filter.isdigit() else None

    entries = list_feedback(session_num=session_num, step_num=step_num)
    summary = summary_by_session()
    grouped: dict[int, list] = {}
    for row in summary:
        grouped.setdefault(row["session_num"], []).append(row)

    return render_template(
        "session_feedback/review.html",
        entries=entries,
        summary=grouped,
        session_num=session_num,
        step_num=step_num,
        session_label=_session_label,
        step_label=_step_label,
        learners=LEARNERS,
    )
