"""Build context for the Course Home dashboard at `/`."""

import os
import re
from dataclasses import dataclass
from typing import Optional

from course_config import LEARNERS
from session_guides import session_url, sessions_for_nav
from start_guide import SETUP_STEPS, START_GUIDE
from welcome_content import WELCOME

ROOT = os.path.dirname(os.path.abspath(__file__))
LEARNERS_DIR = os.path.join(ROOT, ".learners")

PHASE_CATALOG = [
    {
        "num": 0,
        "title": "Meet your tools",
        "tagline": "Learn what GitHub, Python, Cursor, and the rest mean — before you install anything.",
        "links": [
            {"label": "Phase 0 — tool glossary", "href": "/tools", "min_phase": 0},
            {"label": "Phase 0 quiz", "href": "/quiz/phase/0", "min_phase": 0},
        ],
    },
    {
        "num": 1,
        "title": "Tools & first code",
        "tagline": "Cursor, Python, git, and your first live page.",
        "links": [
            {"label": "Phase 1 guide", "href": "/start", "min_phase": 0},
            {"label": "About Me page", "href": "/aboutme/", "min_phase": 1},
            {"label": "Phase 1 quiz", "href": "/quiz/phase/1", "min_phase": 1},
        ],
    },
    {
        "num": 2,
        "title": "Python & git fluency",
        "tagline": "Scripts, loops, functions — and git as muscle memory.",
        "links": [
            {"label": "Phase 2 guide", "href": "/session/2", "min_phase": 2},
            {"label": "lessons/ folder", "href": None, "note": "Practice scripts in your repo"},
            {"label": "Phase 2 quiz", "href": "/quiz/phase/2", "min_phase": 2},
        ],
    },
    {
        "num": 3,
        "title": "Extend the app",
        "tagline": "Routes, SQLite, and HTMX — copy the guestbook pattern.",
        "links": [
            {"label": "Phase 3 guide", "href": "/session/3", "min_phase": 3},
            {"label": "Read recon.md", "href": None, "note": "In .learners/<slug>/ — your instructor shares this here"},
            {"label": "Guestbook lab", "href": "/guestbook/", "min_phase": 3},
            {"label": "Phase 3 quiz", "href": "/quiz/phase/3", "min_phase": 3},
        ],
    },
    {
        "num": 4,
        "title": "Railway & deploy",
        "tagline": "Git push → live site. Read logs when something breaks.",
        "links": [
            {"label": "Phase 4 guide", "href": "/session/4", "min_phase": 4},
            {"label": "Health check", "href": "/healthz", "min_phase": 0},
        ],
    },
    {
        "num": 5,
        "title": "Security",
        "tagline": "Secrets, XSS, HTTPS, and a threat model you can defend.",
        "links": [
            {"label": "Phase 5 guide", "href": "/session/5", "min_phase": 5},
            {"label": "Phase 5 quiz", "href": "/quiz/phase/5", "min_phase": 5},
        ],
    },
    {
        "num": 6,
        "title": "Capstone",
        "tagline": "Plan it, build it, deploy it, explain every line.",
        "links": [
            {"label": "Phase 6 guide", "href": "/session/6", "min_phase": 6},
            {"label": "Phase 6 quiz", "href": "/quiz/phase/6", "min_phase": 6},
            {"label": "Final exam", "href": "/quiz/final", "min_phase": 6},
        ],
    },
]


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


def _unlocked_phase(current_user) -> int:
    if not current_user or not getattr(current_user, "is_authenticated", False):
        return 0
    if getattr(current_user, "is_admin", False):
        return 6
    return current_phase_for_user(current_user)


def _link_locked(link: dict, unlocked_phase: int, is_instructor: bool) -> bool:
    if is_instructor or not link.get("href"):
        return False
    min_phase = link.get("min_phase", 0)
    return unlocked_phase < min_phase


def _enrich_phase_links(links: list, unlocked_phase: int, is_instructor: bool) -> list:
    enriched = []
    for link in links:
        item = dict(link)
        if link.get("href"):
            item["locked"] = _link_locked(link, unlocked_phase, is_instructor)
        enriched.append(item)
    return enriched


def build_dashboard(current_user=None, host: str = "") -> dict:
    learner = None
    slug = None
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

    if signed_in:
        slug = getattr(current_user, "slug", None)
        for entry in LEARNERS:
            if entry["slug"] == slug:
                learner = entry
                break

    unlocked_phase = _unlocked_phase(current_user)
    progress_text = _read_progress_file(slug) if slug else ""
    parsed = _parse_phases_from_markdown(progress_text)
    quiz_by_phase = _quiz_summary(current_user.id) if learner and current_user else {}

    phases: list[PhaseState] = []
    for spec in PHASE_CATALOG:
        num = spec["num"]
        info = parsed.get(num, {})
        quiz = quiz_by_phase.get(num, {}) if num >= 0 else {}
        status = info.get("status", "not_started")
        if num >= 0 and quiz.get("passed") and status != "complete":
            status = "in_progress" if status == "not_started" else status

        phases.append(
            PhaseState(
                num=num,
                title=spec["title"],
                tagline=spec["tagline"],
                links=_enrich_phase_links(spec["links"], unlocked_phase, is_instructor),
                status=status,
                whats_next=info.get("whats_next", ""),
                milestones_done=info.get("milestones_done", 0),
                milestones_total=info.get("milestones_total", 0),
                quiz_best_pct=quiz.get("best_pct"),
                quiz_passed=quiz.get("passed", False),
            )
        )

    setup_done = set()
    if signed_in:
        setup_done.add("signin")
    if slug and os.path.isfile(os.path.join(LEARNERS_DIR, slug, "LEARNER.md")):
        setup_done.add("learner")

    setup = []
    current_step_marked = False
    for step in SETUP_STEPS:
        done = step["id"] in setup_done
        is_current = not done and not current_step_marked
        if is_current:
            current_step_marked = True
        setup.append({**step, "done": done, "is_current": is_current})

    next_action = _pick_next_action(phases, learner, current_user, setup, unlocked_phase, is_instructor)

    current_phase = _current_phase_num(phases)
    all_sessions = sessions_for_nav(unlocked_phase, is_instructor, signed_in)

    return {
        "learner": learner,
        "learner_name": learner["name"] if learner else None,
        "is_instructor": is_instructor,
        "signed_in": signed_in,
        "phases": phases,
        "setup_steps": setup,
        "next_action": next_action,
        "current_phase": current_phase,
        "unlocked_phase": unlocked_phase,
        "all_sessions": all_sessions,
        "learners_registered": LEARNERS,
        "is_live": bool(host and "railway.app" in host),
        "start_guide_url": "/start",
        "show_welcome": not is_instructor,
        "welcome": WELCOME,
    }


def _current_phase_num(phases: list[PhaseState]) -> int:
    for phase in phases:
        if phase.status != "complete":
            return phase.num
    return 6


def _phase_spec(num: int) -> dict:
    for spec in PHASE_CATALOG:
        if spec["num"] == num:
            return spec
    return {"num": num, "title": f"Phase {num}", "tagline": ""}


def _setup_step_title(label: str) -> str:
    if " — " in label:
        return label.split(" — ", 1)[1]
    return label


def _pick_next_action(phases, learner, current_user, setup, unlocked_phase, is_instructor) -> dict:
    phase0 = _phase_spec(0)

    if not learner:
        return {
            "eyebrow": "Start here",
            "title": phase0["title"],
            "detail": phase0["tagline"],
            "href": "/tools",
            "label": "Read the glossary",
        }

    incomplete_setup = [s for s in setup if not s["done"]]
    if incomplete_setup:
        step = incomplete_setup[0]
        return {
            "eyebrow": "Phase 1 setup",
            "title": _setup_step_title(step["label"]),
            "detail": "Work through Start Here one step at a time.",
            "href": f"/start#step-{step['step_num']}",
            "label": "Show directions",
        }

    for phase in phases:
        if phase.status == "complete":
            continue
        spec = _phase_spec(phase.num)
        if phase.num == 0:
            return {
                "eyebrow": "Phase 0",
                "title": spec["title"],
                "detail": "Skim the glossary, then take the short vocab quiz.",
                "href": "/tools",
                "label": "Continue",
            }
        if phase.num == 1:
            return {
                "eyebrow": "Phase 1",
                "title": spec["title"],
                "detail": phase.whats_next or spec["tagline"],
                "href": "/start",
                "label": "Open guide",
            }
        if phase.num >= 2 and unlocked_phase >= phase.num:
            return {
                "eyebrow": f"Phase {phase.num}",
                "title": spec["title"],
                "detail": phase.whats_next or spec["tagline"],
                "href": session_url(phase.num),
                "label": "Open guide",
            }
        if phase.num >= 1 and unlocked_phase >= phase.num:
            return {
                "eyebrow": f"Phase {phase.num}",
                "title": "Pass the quiz",
                "detail": phase.whats_next or spec["tagline"],
                "href": f"/quiz/phase/{phase.num}",
                "label": "Take quiz",
            }
        return {
            "eyebrow": f"Phase {phase.num}",
            "title": spec["title"],
            "detail": phase.whats_next or spec["tagline"],
            "href": session_url(max(1, phase.num)),
            "label": "Open guide",
        }

    return {
        "eyebrow": "Course complete",
        "title": "Demo night",
        "detail": "Walk through your capstone line by line.",
        "href": "/quiz/",
        "label": "Quiz dashboard",
    }


def current_phase_for_user(current_user=None) -> int:
    """Return the learner's current phase number (0–6) for nav gating."""
    if not current_user or not getattr(current_user, "is_authenticated", False):
        return 0
    if getattr(current_user, "is_admin", False):
        return 6

    slug = getattr(current_user, "slug", None)
    if not slug:
        return 0

    parsed = _parse_phases_from_markdown(_read_progress_file(slug))
    for num in range(7):
        info = parsed.get(num, {})
        if info.get("status") != "complete":
            return num
    return 6


def build_nav(current_user=None) -> dict:
    """Which nav links to show — follows progress.md current phase."""
    if current_user and getattr(current_user, "is_authenticated", False):
        if getattr(current_user, "is_admin", False):
            return {
                "start": True,
                "tools": True,
                "home": True,
                "aboutme": True,
                "guestbook": True,
                "quiz": True,
                "admin": True,
            }

        phase = current_phase_for_user(current_user)
        return {
            "start": True,
            "tools": True,
            "home": True,
            "aboutme": phase >= 1,
            "guestbook": phase >= 3,
            "quiz": phase >= 0,
            "admin": False,
        }

    return {
        "start": True,
        "tools": True,
        "home": True,
        "aboutme": False,
        "guestbook": False,
        "quiz": False,
        "admin": False,
    }
