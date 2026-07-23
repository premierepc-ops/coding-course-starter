"""Single source of truth for enrolled learners in this course instance.

Students in their own repo: edit LEARNERS below (see ONBOARDING.md).

Instructor-hosted Railway (before the student creates their repo): set Railway Variables instead —
  LEARNER_SLUG, LEARNER_NAME, and optionally LEARNER_AGE.
"""

import os

TEMPLATE_REPO = "https://github.com/premierepc-ops/coding-course-starter"

# Add entries here in the student's repo after they copy _TEMPLATE.
_LEARNERS_IN_REPO: list[dict] = [
    # {"slug": "student", "name": "Student", "age": 19},
]

LEARNER_TOKEN = "{{LEARNER}}"


def get_learners() -> list[dict]:
    if _LEARNERS_IN_REPO:
        return list(_LEARNERS_IN_REPO)

    slug = os.environ.get("LEARNER_SLUG", "").strip()
    name = os.environ.get("LEARNER_NAME", "").strip()
    if not slug or not name:
        return []

    entry: dict = {"slug": slug, "name": name}
    age = os.environ.get("LEARNER_AGE", "").strip()
    if age.isdigit():
        entry["age"] = int(age)
    return [entry]


# Resolved once at import (Railway env vars are available here).
LEARNERS = get_learners()
