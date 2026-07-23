# How this course app is supposed to work

Read this if something feels "off" about who can see what, or why the app knows a student name.

## Three separate things (do not mix them up)

| Piece | What it is | Who owns it |
|-------|------------|-------------|
| **Template repo** | `premierepc-ops/coding-course-starter` on GitHub | Instructor — generic, no student data |
| **Student fork** | Student clicks "Use this template" → their own GitHub repo | Student — their code, their `.learners/<slug>/`, their `course_config.py` |
| **Railway project** | One deploy per student (`jaqira-course`, etc.) | Instructor workspace — connected to **the student's fork**, not the template |

**The live URL always serves whatever repo Railway is connected to.** If Railway points at the template, you are previewing the generic starter — not the student's real course instance.

## Intended Session 1 flow

1. Student **forks** the template on GitHub.
2. Student clones **their fork**, adds themselves to `course_config.py`, creates `.learners/<slug>/`.
3. Instructor **repoints Railway** Source to the student's fork (Settings → Source).
4. Instructor sets Railway Variables: `SECRET_KEY`, `INSTRUCTOR_PASSWORD`, **`LEARNER_PIN`** (student sign-in PIN — not in git).
5. Push to `main` → Railway redeploys **their** app at the same URL.

Until step 3, the deployed site is a generic demo. It should **not** show a student's name or progress from the template repo.

## What is public vs protected

| URL | Signed out | Student signed in | Instructor |
|-----|------------|-------------------|------------|
| `/` Course Home | Generic landing + course map | Personal dashboard (from `.learners/<slug>/progress.md`) | Instructor summary |
| `/aboutme/` | Public placeholder page | Same (student customizes in their fork) | Same |
| `/guestbook/` | Public read/write lab | Same | Same |
| `/quiz/*` | Redirect to login | Quiz attempts tied to their session | — |
| `/quiz/admin` | Redirect to login | 403 Forbidden | GPA, wrong answers, notes |

**Important:** This is a **teaching app**, not a bank. Student sign-in is **name + PIN** (`LEARNER_PIN` on Railway), not Google SSO. The About Me and guestbook pages stay public by design (Phase 1 and Phase 3 work). Quiz scores and instructor notes require sign-in.

Anyone with the URL can visit the site. Without the student PIN they cannot take quizzes as that student or see the personalized dashboard. Without `INSTRUCTOR_PASSWORD` they cannot open `/quiz/admin`.

## Where "Welcome, Jaqira" comes from

Only when **all** of these are true:

1. Railway deploys **her fork** (not the bare template).
2. Her fork's `course_config.py` lists `{"slug": "jaqira", ...}`.
3. She signed in at `/login` with her name **and** the correct `LEARNER_PIN`.
4. `.learners/jaqira/progress.md` exists in her fork (agent updates each session).

If you saw her name on the template deploy, that was demo data baked into master for a preview — that was wrong and has been removed from the template.

## One student per fork

Each fork has one entry in `LEARNERS` and one Railway project. Adding another student later = new fork + new Railway project (see `ONBOARDING.md`).
