# Onboarding a New Learner

Everything for the course lives in **the student's repo** — app, quiz, HTMX examples, and learner progress files. No family site login required.

Work top to bottom. Steps marked **[Instructor]** need the person running the course (you).

---

## 0. Prerequisites

- Student has a **GitHub account**, **Cursor** (free Hobby), **Python 3**, and **Git**
- **[Instructor]** Railway project connected to the student's repo (see step 5)
- Read **`ARCHITECTURE.md`** if anything about repos, login, or privacy is unclear

### Privacy: private repo required

The template repo on GitHub is public — that's the shared starter only. When a student uses **Use this template**, their new repo must be **Private**:

- **Private** — only people they invite can see the repo. **This is required** — `.learners/<slug>/` holds their name and progress.
- Do **not** create a public copy. Quiz scores and course notes do not belong on public GitHub.

On Railway, you can register the learner with **env vars only** (`LEARNER_SLUG`, `LEARNER_NAME`, `LEARNER_AGE`, `LEARNER_PIN`) before the student adds anything to git. Their GitHub repo must still be **Private** once they clone and work locally.

Never commit `LEARNER_PIN` or `INSTRUCTOR_PASSWORD` to git.

## 1. Use this template and clone

1. Student uses **Use this template** → create repo. Set visibility to **Private** (required).
2. Clone their repo locally and open in Cursor

## 2. Create the learner folder

```bash
cp -r .learners/_TEMPLATE .learners/<slug>
```

Fill `.learners/<slug>/LEARNER.md`.

## 3. Register the learner for quiz

Edit **`course_config.py`** — add an entry to `LEARNERS`:

```python
LEARNERS = [
    {"slug": "student", "name": "Student", "age": 19},
]
```

**Or** on Railway before their repo exists, set Variables: `LEARNER_SLUG`, `LEARNER_NAME`, optional `LEARNER_AGE`. The live site can show the student's name in the sign-in list without this file change.

The student signs in at `/login` by picking their name. No Google SSO. Sign-in does **not** work until step 3 (or Railway env vars) is done.

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

1. Create project, connect **their repo**, deploy on push to `main`
2. Volume at `/data`, set `SECRET_KEY`, `DATA_DIR=/data`, `PORT=8080`, `INSTRUCTOR_PASSWORD`, `LEARNER_PIN`
3. Invite student as **Editor** (Project Settings → Members)

While waiting for the student's repo, you can deploy the template repo with env vars for a preview URL — then repoint Railway to their repo before Phase 1 sign-in.

## 6. Phase 0 recon → run the course

Agent writes `.learners/<slug>/recon.md`, then follow `TRAINING_PROGRAM.md`.

---

## Graduation

All four (see `TRAINING_PROGRAM.md`): final quiz pass, capstone deployed, doing-based checks, explain every line on demo night.

## Adding another student later

New repo → new `LEARNERS` entry in `course_config.py` → new Railway project. Each student is isolated.
