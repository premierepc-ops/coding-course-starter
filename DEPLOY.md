# Deploy: student GitHub repo → instructor Railway

How the live site actually updates. Read this before telling a student to "connect Railway."

## Architecture (what we use)

```
Student's private GitHub repo (their account)
    │
    │  merge to main
    ▼
GitHub Actions  (.github/workflows/railway-deploy.yml)
    │  uses secret RAILWAY_TOKEN (Railway project token)
    │  runs: railway up --service web
    ▼
Instructor's Railway project (your student project, service web)
    │
    ▼
Live URL  (e.g. web-production-41df3f.up.railway.app)
```

**Railway Source (Connect Repo) stays empty.** That is correct. Do not try to connect the student's repo there unless you switch to a different deploy model entirely.

## Why not Railway Source?

For a repo on the **student's GitHub account** where the instructor is only a **collaborator**:

- Railway Source → Connect Repo often **does not list** the repo.
- `railway service source connect` returned **User does not have access to the repo**.
- Telling the student to install the Railway GitHub App (`github.com/apps/railway` **404s**; correct slug is `railway-app`) still requires GitHub-side setup and **no Railway account for the student** was the goal.

**GitHub Actions + project token** works with the repo on the student's GitHub account and deploys to your Railway project.

## One-time setup (instructor + student)

### Instructor

1. Railway project exists (e.g. your student's project), service `web`, volume at `/data`, Variables set (`SECRET_KEY`, `DATA_DIR=/data`, `LEARNER_PIN`, `INSTRUCTOR_PASSWORD`, optional `LEARNER_*`).
2. **web** service → **Settings → Source → Disconnect** if it pointed at `premierepc-ops/coding-course-starter`.
3. Project **Settings → Tokens** → Create Token → **production** → copy token (shown once).
4. Confirm `.github/workflows/railway-deploy.yml` is on the student's `main` branch.
5. Send the token to the student (text / screen share — never git).

### Student (no Railway account)

1. Repo → **Settings → Secrets and variables → Actions**.
2. **New repository secret**
3. Name: **`RAILWAY_TOKEN`** (exactly)
4. Value: paste the token from instructor
5. **Add secret** — confirm `RAILWAY_TOKEN` appears in the list.

### Verify

1. Student repo → **Actions → Deploy to Railway → Run workflow** → green check (~2 min).
2. `{LIVE_URL}/healthz` → `ok`.

## Day-to-day (student coding)

1. Edit code in Cursor on a branch.
2. Open PR on GitHub (instructor reviews).
3. Instructor **merges to `main`**.
4. GitHub Actions runs automatically → live site updates (~2 min).
5. Student checks **Actions** tab for green, then visits the live URL.

Student never logs into Railway. Empty **Source** on Railway is expected.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Invalid RAILWAY_TOKEN` in Actions | Secret missing, wrong name, or wrong value. Update secret on GitHub. |
| Actions green but old content | Hard refresh; confirm merge hit `main`; check Railway **Deployments** tab. |
| Template overwrote live site | Template had Railway Source connected — disconnect Source; redeploy from student repo. |
| Student asks why Source is empty | Normal — deploy goes through Actions, not Source. |

## Files

| File | Role |
|------|------|
| `.github/workflows/railway-deploy.yml` | Runs `railway up` on push to `main` |
| GitHub secret `RAILWAY_TOKEN` | Railway **project** token (production env) |
| `start_guide.py` Step 1b | Plain-English checklist for `/start` |

## Adding another student

New private repo → new Railway project → new project token → new `RAILWAY_TOKEN` secret in **that** repo → same workflow file from template.
