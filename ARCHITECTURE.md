# How this course app is supposed to work

Read this if something feels "off" about who can see what, or why the app knows a student name.

## Three separate things (do not mix them up)

| Piece | What it is | Who owns it |
|-------|------------|-------------|
| **Template repo** | `premierepc-ops/coding-course-starter` on GitHub | Instructor — generic, no student data |
| **Student repo** | Student clicks **Use this template** → their own private GitHub repo | Student — their code, their `.learners/<slug>/`, their `course_config.py` |
| **Railway project** | One deploy per student (e.g. `student-course`) | Instructor workspace — connected to **the student's repo**, not the template |

**The live URL always serves whatever repo Railway is connected to.** If Railway points at the template, you are previewing the generic starter — not the student's real course instance.

## Intended Phase 1 flow

1. Student uses **Use this template** on GitHub → creates their **private** repo.
2. Student clones **their repo**, adds themselves to `course_config.py`, creates `.learners/<slug>/`.
3. Instructor **repoints Railway** Source to the student's repo (Settings → Source).
4. Instructor sets Railway Variables: `SECRET_KEY`, `INSTRUCTOR_PASSWORD`, **`LEARNER_PIN`** (student sign-in PIN — not in git).
5. Push to `main` → Railway redeploys **their** app at the same URL.

Until step 3, the deployed site is a generic demo. It should **not** show a student's name or progress from the template repo.

## What is public vs protected

| URL | Signed out | Student signed in | Instructor |
|-----|------------|-------------------|------------|
| `/` Course Home | Generic landing + course map | Personal dashboard (from `.learners/<slug>/progress.md`) | Instructor summary |
| `/aboutme/` | Public placeholder page | Same (student customizes in their repo) | Same |
| `/guestbook/` | Public read/write lab | Same | Same |
| `/quiz/*` | Redirect to login | Quiz attempts tied to their session | — |
| `/quiz/admin` | Redirect to login | 403 Forbidden | GPA, wrong answers, notes |

**Important:** This is a **teaching app**, not a bank. Student sign-in is **name + PIN** (`LEARNER_PIN` on Railway), not Google SSO. The About Me and guestbook pages stay public by design (Phase 1 and Phase 3 work). Quiz scores and instructor notes require sign-in.

Anyone with the URL can visit the site. Without the student PIN they cannot take quizzes as that student or see the personalized dashboard. Without `INSTRUCTOR_PASSWORD` they cannot open `/quiz/admin`.

## Where a student name on sign-in comes from

Only when **all** of these are true:

1. Railway deploys **their repo** (not the bare template).
2. Their repo's `course_config.py` (or Railway `LEARNER_*` env vars) lists their slug and name.
3. They signed in at `/login` with their name **and** the correct `LEARNER_PIN`.
4. `.learners/<slug>/progress.md` exists in their repo (instructor/agent updates each phase).

If you saw a specific student name on the template deploy, that was demo data or Railway env vars on the wrong repo — remove env vars and redeploy the generic template.

**Also check Railway:** if a student project still deploys the **template** repo, delete `LEARNER_SLUG`, `LEARNER_NAME`, and `LEARNER_AGE` from Railway Variables. Those env vars register a student on the live site without anything in git — fine on a student repo deploy, wrong on the generic template preview.

## One student per repo

Each student repo has one entry in `LEARNERS` and one Railway project. Adding another student later = new repo + new Railway project (see `ONBOARDING.md`).

## Updating content as you go (Phase 1, then Phase 2, …)

You do **not** need one giant update. Ship in slices:

| What you're changing | Where it lives | Who gets it |
|----------------------|----------------|-------------|
| Platform fixes (auth, nav, styling) | Template repo → merge into student repo | Everyone on next pull |
| Phase 1 steps | `start_guide.py` | Student repo (or template, then sync) |
| Phase 2+ steps | `session_guides.py`, linked from Course Home | Same |
| Student progress | `.learners/<slug>/progress.md` in **their repo only** | Never in template |

**Workflow after Phase 1:**

1. Edit in template (`premierepc-ops/coding-course-starter`) or directly in the student's repo.
2. Push to `main` on whichever repo **Railway is connected to** — that redeploys the live URL in ~1 min.
3. If you fixed the template and they already have a repo: pull template updates into their repo, then push.

**Rule of thumb:** Railway deploys **one GitHub repo**. Unpushed local edits and unpulled template updates are **not** on the live site until they're on that repo's `main`.

## Phase unlocks (progress.md, not quiz pass)

Nav links and phase guides follow **`.learners/<slug>/progress.md`**, not quiz scores alone. Passing a quiz is recorded but does not automatically open the next phase — the instructor marks phases complete in `progress.md`.

## Session feedback (curriculum improvement)

Each step on `/tools`, `/start`, and `/session/2`…`/session/6` has **What worked / What didn't** forms. Entries append to `session_feedback.db` (same `DATA_DIR` volume as quiz data). Instructors review aggregated notes at **`/instructor/session-feedback`** (linked from `/quiz/admin`). Use this to revise `session_guides.py` between learners — nothing is auto-edited; you read the log and update the guides.
