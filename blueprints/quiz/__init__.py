import sqlite3
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from site_paths import db_path
from .questions import QUESTIONS, QUESTIONS_VERSION

from course_config import LEARNERS, LEARNER_TOKEN

quiz_bp = Blueprint("quiz", __name__, template_folder="templates")

DB_PATH = db_path("quiz.db")

PHASE_NAMES = {
    1: "Tools, Terminal & First Code",
    2: "Python & Git Fluency",
    3: "Extending the Real App",
    4: "Railway & Deployment",
    5: "Security",
    6: "Capstone",
}

# Learner registry lives in course_config.py (see ONBOARDING.md).


def get_learner(slug):
    """Find a learner by slug (stored as username on quiz attempts)."""
    if not slug:
        return None
    for learner in LEARNERS:
        if learner.get("slug") == slug:
            return learner
    return None


def learner_for_user(user):
    """Find the enrolled learner for a logged-in course user."""
    if not user or not getattr(user, "is_authenticated", False):
        return None
    if getattr(user, "is_admin", False):
        return None
    return get_learner(getattr(user, "slug", None) or getattr(user, "username", None))


def personalize(text, learner):
    """Substitute the learner's name into question text.

    Uses a literal token replace (never str.format), so the many Jinja/dict
    code samples containing `{{ }}`, `{% %}` or `{...}` pass through untouched.
    Numbers (ages, list values) are load-bearing scenario data and are NOT
    personalized. Falls back to a neutral word if the learner is unknown.
    """
    if not text:
        return text
    name = learner["name"] if learner else "the learner"
    return text.replace(LEARNER_TOKEN, name)


def personalize_row(row, learner):
    """Return a dict copy of a question/answer row with name-personalized text fields."""
    d = dict(row)
    for field in ("text", "option_a", "option_b", "option_c", "option_d", "explanation"):
        if d.get(field):
            d[field] = personalize(d[field], learner)
    return d


def get_db():
    db = sqlite3.connect(DB_PATH, check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phase INTEGER NOT NULL,
            text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct TEXT NOT NULL,
            explanation TEXT NOT NULL,
            topic TEXT NOT NULL,
            difficulty INTEGER NOT NULL DEFAULT 1
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            phase INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            gpa REAL NOT NULL,
            letter_grade TEXT NOT NULL,
            auto_feedback TEXT NOT NULL,
            session_feedback TEXT DEFAULT NULL,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS quiz_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attempt_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer_given TEXT NOT NULL,
            correct INTEGER NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS student_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            note TEXT NOT NULL DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS meta (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    db.commit()

    # Seed / re-seed questions. questions.py is the single source of truth: whenever
    # QUESTIONS_VERSION changes (or the table is empty), wipe and re-seed. Ids are the
    # 1-based list position, assigned explicitly so re-seeding preserves the ids that
    # quiz_answers rows reference — historical attempts keep rendering the right questions.
    stored = db.execute("SELECT value FROM meta WHERE key='questions_version'").fetchone()
    stored_version = int(stored["value"]) if stored else 0
    count = db.execute("SELECT COUNT(*) FROM questions").fetchone()[0]

    if count == 0 or stored_version != QUESTIONS_VERSION:
        db.execute("DELETE FROM questions")
        for i, q in enumerate(QUESTIONS, start=1):
            db.execute(
                "INSERT INTO questions (id, phase, text, option_a, option_b, option_c, option_d, correct, explanation, topic, difficulty) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (i, q["phase"], q["text"], q["a"], q["b"], q["c"], q["d"], q["correct"], q["explanation"], q["topic"], q["difficulty"])
            )
        db.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('questions_version', ?)",
            (str(QUESTIONS_VERSION),)
        )
        db.commit()
    db.close()


init_db()


def percentage_to_gpa(pct):
    if pct >= 97: return 4.0
    if pct >= 93: return 4.0
    if pct >= 90: return 3.7
    if pct >= 87: return 3.3
    if pct >= 83: return 3.0
    if pct >= 80: return 2.7
    if pct >= 77: return 2.3
    if pct >= 73: return 2.0
    if pct >= 70: return 1.7
    if pct >= 67: return 1.3
    if pct >= 63: return 1.0
    if pct >= 60: return 0.7
    return 0.0


def percentage_to_letter(pct):
    if pct >= 97: return "A+"
    if pct >= 93: return "A"
    if pct >= 90: return "A-"
    if pct >= 87: return "B+"
    if pct >= 83: return "B"
    if pct >= 80: return "B-"
    if pct >= 77: return "C+"
    if pct >= 73: return "C"
    if pct >= 70: return "C-"
    if pct >= 67: return "D+"
    if pct >= 63: return "D"
    if pct >= 60: return "D-"
    return "F"


def generate_auto_feedback(phase, score, total, wrong_topics):
    pct = (score / total) * 100
    letter = percentage_to_letter(pct)

    if pct >= 90:
        summary = "Excellent. Demonstrated strong command of the material."
    elif pct >= 80:
        summary = "Solid performance. Most concepts are understood; a few gaps remain."
    elif pct >= 70:
        summary = "Passing, but several areas need reinforcement before moving on."
    elif pct >= 60:
        summary = "Below expectations. Review Phase {} material before proceeding.".format(phase)
    else:
        summary = "Significant gaps present. Phase {} material should be revisited in full.".format(phase)

    phase_name = PHASE_NAMES.get(phase, "Final Test") if phase > 0 else "Final Test"

    if wrong_topics:
        topic_counts = {}
        for t in wrong_topics:
            topic_counts[t] = topic_counts.get(t, 0) + 1
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        weak_str = ", ".join(t for t, _ in sorted_topics[:3])
        weak_section = " Weakest areas: {}.".format(weak_str)
    else:
        weak_section = " No significant weak areas identified."

    return "Phase {phase} ({name}) — {score}/{total} ({pct:.0f}%, {letter}). {summary}{weak}".format(
        phase=phase if phase > 0 else "Final",
        name=phase_name,
        score=score,
        total=total,
        pct=pct,
        letter=letter,
        summary=summary,
        weak=weak_section
    )


def get_best_attempt(user_id, phase):
    db = get_db()
    row = db.execute(
        "SELECT * FROM quiz_attempts WHERE user_id=? AND phase=? ORDER BY percentage DESC LIMIT 1",
        (user_id, phase)
    ).fetchone()
    db.close()
    return row


def get_cumulative_gpa(user_id):
    db = get_db()
    rows = db.execute(
        "SELECT phase, MAX(percentage) as best_pct FROM quiz_attempts WHERE user_id=? AND phase BETWEEN 1 AND 6 GROUP BY phase",
        (user_id,)
    ).fetchall()
    db.close()
    if not rows:
        return None, []
    gpas = [percentage_to_gpa(r["best_pct"]) for r in rows]
    cumulative = round(sum(gpas) / len(gpas), 2)
    return cumulative, rows


# ───────────────────────── Routes ─────────────────────────

@quiz_bp.route("/")
@login_required
def dashboard():
    # Student always gets the student view, even if they're also admin.
    # Non-student admins get redirected to the review dashboard.
    if not learner_for_user(current_user):
        if current_user.is_admin:
            return redirect(url_for("quiz.admin_view"))
        abort(403)
    db = get_db()
    phase_data = []
    for phase in range(1, 7):
        best = db.execute(
            "SELECT * FROM quiz_attempts WHERE user_id=? AND phase=? ORDER BY percentage DESC LIMIT 1",
            (current_user.id, phase)
        ).fetchone()
        attempt_count = db.execute(
            "SELECT COUNT(*) FROM quiz_attempts WHERE user_id=? AND phase=?",
            (current_user.id, phase)
        ).fetchone()[0]
        phase_data.append({
            "phase": phase,
            "name": PHASE_NAMES[phase],
            "best": best,
            "attempts": attempt_count,
        })

    final_best = db.execute(
        "SELECT * FROM quiz_attempts WHERE user_id=? AND phase=0 ORDER BY percentage DESC LIMIT 1",
        (current_user.id,)
    ).fetchone()

    cumulative_gpa, _ = get_cumulative_gpa(current_user.id)

    note_row = db.execute(
        "SELECT note FROM student_notes WHERE user_id=?", (current_user.id,)
    ).fetchone()
    student_note = note_row["note"] if note_row else ""

    db.close()

    submitted = request.args.get("submitted")

    return render_template(
        "quiz/dashboard.html",
        phase_data=phase_data,
        final_best=final_best,
        cumulative_gpa=cumulative_gpa,
        phase_names=PHASE_NAMES,
        student_note=student_note,
        submitted=submitted,
    )


@quiz_bp.route("/phase/<int:phase>", methods=["GET", "POST"])
@login_required
def take_quiz(phase):
    if not learner_for_user(current_user):
        abort(403)
    if phase not in range(1, 7):
        abort(404)

    db = get_db()
    questions = db.execute(
        "SELECT * FROM questions WHERE phase=? ORDER BY id",
        (phase,)
    ).fetchall()

    if request.method == "POST":
        score = 0
        wrong_topics = []
        answers_to_save = []

        for q in questions:
            given = request.form.get("q_{}".format(q["id"]), "")
            is_correct = 1 if given.lower() == q["correct"].lower() else 0
            if is_correct:
                score += 1
            else:
                wrong_topics.append(q["topic"])
            answers_to_save.append((q["id"], given, is_correct))

        total = len(questions)
        pct = (score / total * 100) if total > 0 else 0
        gpa = percentage_to_gpa(pct)
        letter = percentage_to_letter(pct)
        feedback = generate_auto_feedback(phase, score, total, wrong_topics)

        cursor = db.execute(
            "INSERT INTO quiz_attempts (user_id, username, phase, score, total, percentage, gpa, letter_grade, auto_feedback) VALUES (?,?,?,?,?,?,?,?,?)",
            (current_user.id, current_user.username, phase, score, total, pct, gpa, letter, feedback)
        )
        attempt_id = cursor.lastrowid

        for q_id, given, correct in answers_to_save:
            db.execute(
                "INSERT INTO quiz_answers (attempt_id, question_id, answer_given, correct) VALUES (?,?,?,?)",
                (attempt_id, q_id, given, correct)
            )

        db.commit()
        db.close()
        return redirect(url_for("quiz.dashboard", submitted="1"))

    learner = learner_for_user(current_user)
    personalized = [personalize_row(q, learner) for q in questions]
    db.close()
    return render_template(
        "quiz/quiz.html",
        questions=personalized,
        phase=phase,
        phase_name=PHASE_NAMES[phase],
    )


@quiz_bp.route("/results/<int:attempt_id>")
@login_required
def results(attempt_id):
    if not current_user.is_admin:
        abort(403)
    db = get_db()
    attempt = db.execute("SELECT * FROM quiz_attempts WHERE id=?", (attempt_id,)).fetchone()
    if not attempt:
        abort(404)

    answers = db.execute(
        """SELECT qa.answer_given, qa.correct, q.text, q.option_a, q.option_b, q.option_c, q.option_d, q.correct as right_answer, q.explanation, q.topic
           FROM quiz_answers qa JOIN questions q ON qa.question_id = q.id
           WHERE qa.attempt_id=?""",
        (attempt_id,)
    ).fetchall()
    db.close()

    learner = get_learner(attempt["username"])
    answers = [personalize_row(a, learner) for a in answers]
    return render_template("quiz/results.html", attempt=attempt, answers=answers, phase_names=PHASE_NAMES)


@quiz_bp.route("/final", methods=["GET", "POST"])
@login_required
def final_test():
    if not learner_for_user(current_user):
        abort(403)
    db = get_db()

    # Require all 6 phase quizzes to be completed first
    completed_phases = db.execute(
        "SELECT DISTINCT phase FROM quiz_attempts WHERE user_id=? AND phase BETWEEN 1 AND 6",
        (current_user.id,)
    ).fetchall()
    completed_set = {r["phase"] for r in completed_phases}
    if not all(p in completed_set for p in range(1, 7)):
        db.close()
        missing = [p for p in range(1, 7) if p not in completed_set]
        return render_template("quiz/final_locked.html", missing=missing, phase_names=PHASE_NAMES)

    questions = db.execute("SELECT * FROM questions ORDER BY phase, id").fetchall()

    if request.method == "POST":
        score = 0
        wrong_topics = []
        answers_to_save = []

        for q in questions:
            given = request.form.get("q_{}".format(q["id"]), "")
            is_correct = 1 if given.lower() == q["correct"].lower() else 0
            if is_correct:
                score += 1
            else:
                wrong_topics.append(q["topic"])
            answers_to_save.append((q["id"], given, is_correct))

        total = len(questions)
        pct = (score / total * 100) if total > 0 else 0
        gpa = percentage_to_gpa(pct)
        letter = percentage_to_letter(pct)
        feedback = generate_auto_feedback(0, score, total, wrong_topics)

        cursor = db.execute(
            "INSERT INTO quiz_attempts (user_id, username, phase, score, total, percentage, gpa, letter_grade, auto_feedback) VALUES (?,?,?,?,?,?,?,?,?)",
            (current_user.id, current_user.username, 0, score, total, pct, gpa, letter, feedback)
        )
        attempt_id = cursor.lastrowid

        for q_id, given, correct in answers_to_save:
            db.execute(
                "INSERT INTO quiz_answers (attempt_id, question_id, answer_given, correct) VALUES (?,?,?,?)",
                (attempt_id, q_id, given, correct)
            )

        db.commit()
        db.close()
        return redirect(url_for("quiz.dashboard", submitted="1"))

    learner = learner_for_user(current_user)
    personalized = [personalize_row(q, learner) for q in questions]
    db.close()
    return render_template("quiz/final.html", questions=personalized)


@quiz_bp.route("/admin")
@login_required
def admin_view():
    if not current_user.is_admin:
        abort(403)
    db = get_db()

    raw_attempts = db.execute(
        "SELECT * FROM quiz_attempts ORDER BY completed_at DESC"
    ).fetchall()

    option_map = {"a": "option_a", "b": "option_b", "c": "option_c", "d": "option_d"}

    attempts = []
    for i, att in enumerate(raw_attempts):
        wrong_raw = db.execute(
            """SELECT qa.answer_given, qa.correct, q.text, q.option_a, q.option_b,
                      q.option_c, q.option_d, q.correct as right_answer, q.explanation, q.topic
               FROM quiz_answers qa JOIN questions q ON qa.question_id = q.id
               WHERE qa.attempt_id=? AND qa.correct=0""",
            (att["id"],)
        ).fetchall()

        learner = get_learner(att["username"])
        wrong_answers = []
        for w in wrong_raw:
            given_col = option_map.get(w["answer_given"].lower(), "option_a")
            right_col = option_map.get(w["right_answer"].lower(), "option_a")
            wrong_answers.append({
                "text": personalize(w["text"], learner),
                "answer_given": w["answer_given"],
                "given_text": personalize(w[given_col], learner),
                "right_answer": w["right_answer"],
                "correct_text": personalize(w[right_col], learner),
                "explanation": personalize(w["explanation"], learner),
                "topic": w["topic"],
            })

        # Count attempt number for this user+phase
        attempt_number = db.execute(
            "SELECT COUNT(*) FROM quiz_attempts WHERE user_id=? AND phase=? AND completed_at <= ?",
            (att["user_id"], att["phase"], att["completed_at"])
        ).fetchone()[0]

        attempts.append({
            "attempt": att,
            "wrong_answers": wrong_answers,
            "attempt_number": attempt_number,
        })

    # Build a GPA + notes summary for every learner who has attempts.
    students = db.execute(
        "SELECT DISTINCT user_id, username FROM quiz_attempts ORDER BY username"
    ).fetchall()

    learner_summaries = []
    for s in students:
        uid = s["user_id"]
        phase_rows = db.execute(
            """SELECT phase, MAX(percentage) as best_pct
               FROM quiz_attempts WHERE user_id=? AND phase BETWEEN 1 AND 6
               GROUP BY phase ORDER BY phase""",
            (uid,)
        ).fetchall()
        gpa_summary = None
        if phase_rows:
            phase_gpas = []
            phases_detail = []
            for r in phase_rows:
                g = percentage_to_gpa(r["best_pct"])
                phase_gpas.append(g)
                phases_detail.append({
                    "phase": r["phase"],
                    "letter": percentage_to_letter(r["best_pct"]),
                    "pct": r["best_pct"],
                    "gpa": g,
                })
            gpa_summary = {
                "cumulative": round(sum(phase_gpas) / len(phase_gpas), 2),
                "phases_done": len(phase_rows),
                "phases": phases_detail,
            }

        sn = db.execute(
            "SELECT note, updated_at FROM student_notes WHERE user_id=?", (uid,)
        ).fetchone()
        self_note = {"note": sn["note"], "updated_at": sn["updated_at"]} if sn and sn["note"] else None

        learner_summaries.append({
            "username": s["username"],
            "gpa_summary": gpa_summary,
            "self_note": self_note,
        })

    db.close()
    return render_template(
        "quiz/admin.html",
        attempts=attempts,
        phase_names=PHASE_NAMES,
        learner_summaries=learner_summaries,
    )


@quiz_bp.route("/admin/feedback/<int:attempt_id>", methods=["POST"])
@login_required
def add_feedback(attempt_id):
    if not current_user.is_admin:
        abort(403)
    feedback = request.form.get("feedback", "").strip()
    if feedback:
        db = get_db()
        db.execute("UPDATE quiz_attempts SET session_feedback=? WHERE id=?", (feedback, attempt_id))
        db.commit()
        db.close()
    return redirect(url_for("quiz.admin_view"))


@quiz_bp.route("/notes", methods=["POST"])
@login_required
def save_student_notes():
    if not learner_for_user(current_user):
        abort(403)
    note = request.form.get("note", "").strip()
    db = get_db()
    existing = db.execute(
        "SELECT id FROM student_notes WHERE user_id=?", (current_user.id,)
    ).fetchone()
    if existing:
        db.execute(
            "UPDATE student_notes SET note=?, updated_at=CURRENT_TIMESTAMP WHERE user_id=?",
            (note, current_user.id)
        )
    else:
        db.execute(
            "INSERT INTO student_notes (user_id, note) VALUES (?,?)",
            (current_user.id, note)
        )
    db.commit()
    db.close()
    return redirect(url_for("quiz.dashboard"))
