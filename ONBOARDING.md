# Onboarding a New Learner

Everything for the course lives in **the student's repo** — app, quiz, HTMX examples, and learner progress files. No family site login required.

Work top to bottom. Steps marked **[Instructor]** need the person running the course (you).

**Deploy model:** student repo → GitHub Actions → your Railway project. See **`DEPLOY.md`** for the full picture (Railway Source stays empty — that is intentional).

---

## 0. Prerequisites

- Student has a **GitHub account** and **Cursor** (free Hobby)
- Student installs **Python 3** from python.org (Cursor does not include it — see Phase 1 Step 2)
- Git: usually already available via Cursor; install git-scm.com only if `git --version` fails
- **[Instructor]** Railway project ready (see step 5) and deploy wired (step 5b)
- Read **`ARCHITECTURE.md`** and **`DEPLOY.md`** if anything about repos, login, or deploy is unclear

### Privacy: private repo required

The template repo on GitHub is public — that's the shared starter only. When a student uses **Use this template**, their new repo must be **Private**:

- **Private** — only people they invite can see the repo. **This is required** — `.learners/<slug>/` holds their name and progress.
- Do **not** create a public copy. Quiz scores and course notes do not belong on public GitHub.

On Railway, you can register the learner with **env vars only** (`LEARNER_SLUG`, `LEARNER_NAME`, `LEARNER_AGE`, `LEARNER_PIN`) before the student adds anything to git. Their GitHub repo must still be **Private** once they clone and work locally.

Never commit `LEARNER_PIN`, `INSTRUCTOR_PASSWORD`, or `RAILWAY_TOKEN` to git.

## 1. Use this template and clone

1. Student uses **Use this template** → create repo under **their** GitHub account. Set visibility to **Private** (required).
2. Student **invites the instructor as a collaborator** on that repo and sends the HTTPS URL.
3. Student clones their repo locally and opens in Cursor (Phase 1 Step 3).

The repo stays on the student's GitHub. It does **not** need to appear in Railway Source.

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

1. Create project (e.g. `jaqira-course`) or use existing.
2. Service `web`, volume at `/data`, Variables: `SECRET_KEY`, `DATA_DIR=/data`, `PORT=8080`, `INSTRUCTOR_PASSWORD`, `LEARNER_PIN` (and optional `LEARNER_*`).
3. **web** → **Settings → Source → Disconnect** if connected to the template repo — deploy will come from GitHub Actions instead.

For Phase 0 before the student repo exists, you can deploy the template once with `railway up` and env vars. After step 5b, all deploys come from **their** repo.

## 5b. **[Instructor + student]** Wire GitHub Actions deploy

Follow **`start_guide.py` Step 1b** (shown at `/start`) or **`DEPLOY.md`**.

Summary:

1. **[You]** Railway project **Settings → Tokens** → create **production** token → send to student.
2. **[Student]** Repo **Settings → Secrets and variables → Actions** → secret name **`RAILWAY_TOKEN`** → paste token.
3. **[You]** Confirm `.github/workflows/railway-deploy.yml` on their `main`.
4. **[Either]** Actions → **Deploy to Railway → Run workflow** → green; `/healthz` → `ok`.

Student never creates a Railway account. Railway **Source** stays empty — normal.

## 6. Phase 0 recon → run the course

Agent writes `.learners/<slug>/recon.md`, then follow `TRAINING_PROGRAM.md`. Student works in Cursor; merges to `main` deploy via Actions.

---

## Graduation

All four (see `TRAINING_PROGRAM.md`): final quiz pass, capstone deployed, doing-based checks, explain every line on demo night.

## Adding another student later

New private repo → new `LEARNERS` entry → **new Railway project** → new project token → new `RAILWAY_TOKEN` secret in that repo. Each student is isolated.
