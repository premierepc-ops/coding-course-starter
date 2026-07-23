# Onboarding a New Learner

Everything for the course lives in **this fork** — app, quiz, HTMX examples, and learner progress files. No family site login required.

Work top to bottom. Steps marked **[Instructor]** need the person running the course (you).

---

## 0. Prerequisites

- Student has a **GitHub account**, **Cursor** (free Hobby), **Python 3**, and **Git**
- **[Instructor]** Railway project connected to the student's fork (see step 5)
- Read **`ARCHITECTURE.md`** if anything about forks, login, or privacy is unclear

## 1. Fork and clone

1. Fork this template on GitHub
2. Clone the fork locally and open in Cursor

## 2. Create the learner folder

```bash
cp -r .learners/_TEMPLATE .learners/<slug>
```

Fill `.learners/<slug>/LEARNER.md`.

## 3. Register the learner for quiz

Edit **`course_config.py`** — add an entry to `LEARNERS`:

```python
LEARNERS = [
    {"slug": "jaqira", "name": "Jaqira", "age": 19},
]
```

The student signs in at `/login` by picking their name. No Google SSO.

## 4. Set instructor password

In `.env` (local) and Railway Variables (production):

```
INSTRUCTOR_PASSWORD=your-private-password
LEARNER_PIN=student-sign-in-pin
```

Share `LEARNER_PIN` with the student only (text, in person — not in git). Without it, no one can sign in as the student on Railway.

Instructor opens `/login?instructor=1` → `/quiz/admin` for GPA, wrong answers, and session notes.

## 5. **[Instructor]** Railway project

One project per student under your workspace:

1. Create project, connect **their fork**, deploy on push to `main`
2. Volume at `/data`, set `SECRET_KEY`, `DATA_DIR=/data`, `PORT=8080`, `INSTRUCTOR_PASSWORD`, `LEARNER_PIN`
3. Invite student as **Editor** (Project Settings → Members)

## 6. Phase 0 recon → run the course

Agent writes `.learners/<slug>/recon.md`, then follow `TRAINING_PROGRAM.md`.

---

## Graduation

All four (see `TRAINING_PROGRAM.md`): final quiz pass, capstone deployed, doing-based checks, explain every line on demo night.

## Adding another student later

New fork → new `LEARNERS` entry in `course_config.py` → new Railway project. Each student is isolated.
