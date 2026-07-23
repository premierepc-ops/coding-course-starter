"""Build context for the Course Home dashboard at `/`."""

import os
import re
from dataclasses import dataclass
from typing import Optional

from course_config import LEARNERS
from start_guide import SETUP_STEPS, START_GUIDE

ROOT = os.path.dirname(os.path.abspath(__file__))
LEARNERS_DIR = os.path.join(ROOT, ".learners")

PHASE_CATALOG = [
    {
        "num": 0,
        "title": "Recon",
        "tagline": "Map the codebase before you touch anything.",
        "links": [{"label": "Read recon.md", "href": None, "note": "In .learners/<slug>/recon.md"}],
    },
    {
        "num": 1,
        "title": "Tools & first code",
        "tagline": "Cursor, Python, git, and your first live page.",
        "links": [
            {"label": "About Me page", "href": "/aboutme/"},
            {"label": "Phase 1 quiz", "href": "/quiz/phase/1"},
        ],
    },
    {
        "num": 2,
        "title": "Python & git fluency",
        "tagline": "Scripts, loops, functions — and git as muscle memory.",
        "links": [
            {"label": "lessons/ folder", "href": None, "note": "Practice scripts in your fork"},
            {"label": "Phase 2 quiz", "href": "/quiz/phase/2"},
        ],
    },
    {
        "num": 3,
        "title": "Extend the app",
        "tagline": "Routes, SQLite, and HTMX — copy the guestbook pattern.",
        "links": [
            {"label": "Guestbook lab", "href": "/guestbook/"},
            {"label": "Phase 3 quiz", "href": "/quiz/phase/3"},
        ],
    },
    {
        "num": 4,
        "title": "Railway & deploy",
        "tagline": "Git push → live site. Read logs when something breaks.",
        "links": [{"label": "Health check", "href": "/healthz"}],
    },
    {
        "num": 5,
        "title": "Security",
        "tagline": "Secrets, XSS, HTTPS, and a threat model you can defend.",
        "links": [{"label": "Phase 5 quiz", "href": "/quiz/phase/5"}],
    },
    {
        "num": 6,
        "title": "Capstone",
        "tagline": "Plan it, build it, deploy it, explain every line.",
        "links": [{"label": "Phase 6 quiz", "href": "/quiz/phase/6"}, {"label": "Final exam", "href": "/quiz/final"}],
    },
]

# Setup checklist — imported from start_guide.py (plain-English directions per step)


@dataclass
class PhaseState:
    num: int
    title: str
    tagline: str
    links: list
    status: str = "not_started"
    whats_next: str = ""
    milestones_done: int = 0
    milestones_total: int = 0
    quiz_best_pct: Optional[float] = None
    quiz_passed: bool = False


def _read_progress_file(slug: str) -> str:
    path = os.path.join(LEARNERS_DIR, slug, "progress.md")
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def _parse_phases_from_markdown(text: str) -> dict[int, dict]:
    """Extract per-phase status, whats_next, and milestone counts from progress.md."""
    result: dict[int, dict] = {}
    if not text:
        return result

    chunks = re.split(r"\n## Phase (\d+)", text)
    # chunks[0] is preamble; then pairs of (num, body)
    i = 1
    while i + 1 < len(chunks):
        num = int(chunks[i])
        body = chunks[i + 1]
        status_match = re.search(r"\*\*Status:\*\*\s*(.+?)(?:\.\s|$)", body, re.M)
        status_raw = status_match.group(1).strip() if status_match else "Not started"
        if status_raw.lower().startswith("complete"):
            status = "complete"
        elif "in progress" in status_raw.lower():
            status = "in_progress"
        else:
            status = "not_started"

        next_match = re.search(r"\*\*What's next:\*\*\s*(.+)", body)
        whats_next = next_match.group(1).strip() if next_match else ""

        milestones = re.findall(r"- \[([ xX])\]", body)
        done = sum(1 for m in milestones if m.lower() == "x")
        total = len(milestones)

        result[num] = {
            "status": status,
            "whats_next": whats_next,
            "milestones_done": done,
            "milestones_total": total,
        }
        i += 2
    return result


def _quiz_summary(user_id: int) -> dict[int, dict]:
    from blueprints.quiz import get_db, percentage_to_letter

    db = get_db()
    rows = db.execute(
        """SELECT phase, MAX(percentage) as best_pct
           FROM quiz_attempts WHERE user_id=? AND phase BETWEEN 0 AND 6
           GROUP BY phase""",
        (user_id,),
    ).fetchall()
    db.close()
    out = {}
    for row in rows:
        pct = row["best_pct"]
        out[row["phase"]] = {
            "best_pct": pct,
            "passed": pct >= 70,
            "letter": percentage_to_letter(pct),
        }
    return out


def build_dashboard(current_user=None, host: str = "") -> dict:
    learner = None
    slug = None
    if current_user and getattr(current_user, "is_authenticated", False):
        if getattr(current_user, "is_admin", False):
            learner = None
        else:
            slug = getattr(current_user, "slug", None)
            for entry in LEARNERS:
                if entry["slug"] == slug:
                    learner = entry
                    break

    progress_text = _read_progress_file(slug) if slug else ""
    parsed = _parse_phases_from_markdown(progress_text)
    quiz_by_phase = _quiz_summary(current_user.id) if learner and current_user else {}

    phases: list[PhaseState] = []
    for spec in PHASE_CATALOG:
        num = spec["num"]
        info = parsed.get(num, {})
        quiz = quiz_by_phase.get(num, {}) if num >= 1 else {}
        status = info.get("status", "not_started")
        if num >= 1 and quiz.get("passed") and status != "complete":
            status = "in_progress" if status == "not_started" else status

        phases.append(
            PhaseState(
                num=num,
                title=spec["title"],
                tagline=spec["tagline"],
                links=spec["links"],
                status=status,
                whats_next=info.get("whats_next", ""),
                milestones_done=info.get("milestones_done", 0),
                milestones_total=info.get("milestones_total", 0),
                quiz_best_pct=quiz.get("best_pct"),
                quiz_passed=quiz.get("passed", False),
            )
        )

    # Setup checklist — only auto-check what we can verify reliably
    setup_done = set()
    if current_user and getattr(current_user, "is_authenticated", False) and not getattr(
        current_user, "is_admin", False
    ):
        setup_done.add("signin")
    if slug and os.path.isfile(os.path.join(LEARNERS_DIR, slug, "LEARNER.md")):
        setup_done.add("learner")

    setup = []
    for step in SETUP_STEPS:
        setup.append({**step, "done": step["id"] in setup_done})

    # Next action
    next_action = _pick_next_action(phases, learner, current_user, setup)

    current_phase = _current_phase_num(phases)

    return {
        "learner": learner,
        "learner_name": learner["name"] if learner else None,
        "is_instructor": bool(
            current_user
            and getattr(current_user, "is_authenticated", False)
            and getattr(current_user, "is_admin", False)
        ),
        "signed_in": bool(
            current_user
            and getattr(current_user, "is_authenticated", False)
            and not getattr(current_user, "is_admin", False)
        ),
        "phases": phases,
        "setup_steps": setup,
        "next_action": next_action,
        "current_phase": current_phase,
        "learners_registered": LEARNERS,
        "is_live": bool(host and "railway.app" in host),
        "start_guide_url": "/start",
    }


def _current_phase_num(phases: list[PhaseState]) -> int:
    for phase in phases:
        if phase.status != "complete":
            return phase.num
    return 6


def _pick_next_action(phases, learner, current_user, setup) -> dict:
    if not learner:
        return {
            "title": "Start Session 1 — read the step-by-step guide",
            "detail": "Never coded before? The Start Here page walks you through fork, install, sign-in, and your first file — in plain English.",
            "href": "/start",
            "label": "Open Start Here",
        }

    incomplete_setup = [s for s in setup if not s["done"]]
    if incomplete_setup:
        step = incomplete_setup[0]
        return {
            "title": step["label"],
            "detail": (step.get("directions") or ["See Start Here for full directions."])[0],
            "href": step.get("link", {}).get("href") or "/start",
            "label": step.get("link", {}).get("label") or "See how to do this",
        }

    for phase in phases:
        if phase.status == "complete":
            continue
        if phase.num == 0:
            return {
                "title": "Finish Phase 0 recon",
                "detail": phase.whats_next or "Read the repo and fill in .learners/<slug>/recon.md with your agent.",
                "href": None,
                "label": None,
            }
        if phase.num == 1:
            return {
                "title": "Start Phase 1 — type hello.py by hand",
                "detail": phase.whats_next or "Install tools, run a script you typed yourself, then customize /aboutme/.",
                "href": "/aboutme/",
                "label": "Open About Me",
            }
        if phase.num == 3:
            return {
                "title": "Phase 3 — study the guestbook",
                "detail": "Trace how hx-post swaps in new HTML, then build your own feature.",
                "href": "/guestbook/",
                "label": "Open guestbook lab",
            }
        quiz_href = f"/quiz/phase/{phase.num}" if 1 <= phase.num <= 6 else "/quiz/"
        return {
            "title": f"Phase {phase.num}: {phase.title}",
            "detail": phase.whats_next or phase.tagline,
            "href": quiz_href if phase.num >= 1 else None,
            "label": f"Phase {phase.num} quiz" if phase.num >= 1 else None,
        }

    return {
        "title": "Course complete — demo night",
        "detail": "Walk through your capstone line by line. You shipped it.",
        "href": "/quiz/",
        "label": "View quiz dashboard",
    }
