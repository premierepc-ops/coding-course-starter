# Coding Course Starter

A **self-contained** learn-to-code platform: Flask app + quizzes + HTMX examples + Cursor-native curriculum. One private repo per student via **Use this template**, deploy to Railway. No tie-in to any other site.

**Template:** https://github.com/premierepc-ops/coding-course-starter

## Quick start

```bash
git clone https://github.com/YOUR_USERNAME/coding-course-starter.git
cd coding-course-starter
pip install -r requirements.txt
cp .env.example .env
# Edit .env — SECRET_KEY and INSTRUCTOR_PASSWORD
python app.py
```

Visit http://localhost:5000

| URL | Purpose |
|-----|---------|
| `/` | Home |
| `/aboutme/` | Phase 1 personal page |
| `/guestbook/` | Phase 3 HTMX reference (in-repo) |
| `/quiz/` | Phase quizzes + final (sign in at `/login`) |
| `/quiz/admin` | Instructor dashboard (instructor login) |

## Onboarding a student

See `ONBOARDING.md` and **`DEPLOY.md`**. Summary: **Use this template** → collaborator invite → `RAILWAY_TOKEN` secret → GitHub Actions deploys to your Railway project.

## Course docs

- `TRAINING_PROGRAM.md` — agent handoff / curriculum
- `DEPLOY.md` — student repo → GitHub Actions → Railway (read this first for deploy)
- `ONBOARDING.md` — setup checklist
- `.learners/<slug>/` — profile, progress, recon, capstone

## Stack

Python 3 · Flask · Jinja2 · HTMX · SQLite · Gunicorn · Railway · Cursor
