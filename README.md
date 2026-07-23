# Coding Course Starter

Fork this repo to your GitHub account, clone your fork, and open it in **Cursor**. This is your personal app for the coding course — you deploy it to Railway; quizzes live on the family site.

## Quick start

1. **Fork** this repo on GitHub (use the Fork button).
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/coding-course-starter.git
   cd coding-course-starter
   ```
3. **Install Python 3** and **Cursor** (see `ONBOARDING.md`).
4. **Set up environment:**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env — set SECRET_KEY to a long random string
   ```
5. **Run locally:**
   ```bash
   python app.py
   ```
   Visit http://localhost:5000

6. **Create your learner folder:**
   ```bash
   cp -r .learners/_TEMPLATE .learners/your-slug
   ```
   Fill in `.learners/your-slug/LEARNER.md`.

7. **Deploy to Railway** — Dad sets up the project and connects your fork. Push to `main` and watch it deploy.

## Course docs

| File | Purpose |
|------|---------|
| `TRAINING_PROGRAM.md` | Agent handoff — how the course runs |
| `ONBOARDING.md` | Setup checklist for new learners |
| `.learners/<slug>/` | Your profile, progress, recon, capstone |

## Quiz

Take phase quizzes and the final exam at **https://family.rydzfski.com/quiz** (Google SSO — enroll by email before your first quiz).

## Git rules

- `lessons/<slug>/` practice files → push to `main` directly
- App code changes → feature branch → PR → instructor reviews and merges

## Stack

Python 3 · Flask · Jinja2 · SQLite (via `site_paths.py`) · Gunicorn · Railway
