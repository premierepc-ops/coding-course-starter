"""Plain-English Phase 1 directions shown at /start and on the course home checklist."""

from course_config import TEMPLATE_REPO

INSTRUCTOR_GITHUB = "premierepc-ops"
LIVE_SITE_URL = "https://web-production-41df3f.up.railway.app"

START_GUIDE = {
    "title": "Phase 1 — Start here",
    "time_estimate": "About 60–90 minutes with your instructor",
    "intro": (
        "Each step lists **Student** and **Instructor** actions separately. "
        "Your instructor hosts the live site — you work in GitHub and Cursor."
    ),
    "roles_note": (
        "Student repo on their GitHub. Your Railway project. They code in Cursor — you merge PRs to `main` — "
        "GitHub Actions deploys to your live URL. Railway Source stays empty; that is normal."
    ),
    "deploy_pitfalls": [
        "Working setup: GitHub Actions + secret RAILWAY_TOKEN + empty Railway Source (see DEPLOY.md).",
        "Do not use Railway Source → Connect Repo for student-owned repos — it failed; use Actions instead.",
        "Do not use github.com/apps/railway (404). Student does not install any Railway GitHub App.",
        "Secret name must be exactly RAILWAY_TOKEN. Value is your Railway project token — not a Railway login.",
        "Do not click **Fork** on GitHub — that is a different button. Use **Use this template** only.",
    ],
    "steps": [
        {
            "num": 0,
            "title": "Phase 0 — read Meet your tools",
            "summary": "Vocabulary before installs.",
            "student": [
                "Open /tools and read the glossary once with your instructor.",
                "Take the Phase 0 quiz if you are signed in (optional but recommended).",
            ],
            "instructor": [
                "Confirm the student can sign in at /login (LEARNER_PIN set on your Railway project).",
                "If Step 1b deploy is wired, the live site runs the student's repo via GitHub Actions — not the template.",
            ],
            "link": {"label": "Read the glossary", "href": "/tools"},
        },
        {
            "num": 1,
            "title": "Create your GitHub repo",
            "summary": "Your repo on your GitHub account — not the shared template.",
            "student": [
                f"Open {TEMPLATE_REPO}",
                "Click green **Use this template** → **Create a new repository** — **not Fork** (Fork is wrong for this course).",
                "Owner: **your** GitHub account (not premierepc-ops).",
                "Name: e.g. `yourname-coding-course` (lowercase, hyphens OK).",
                "Visibility: **Private** (required).",
                "Click **Create repository**.",
                f"Settings → Collaborators → invite **`{INSTRUCTOR_GITHUB}`**.",
                "Copy HTTPS URL (Code → HTTPS) and send it to your instructor.",
            ],
            "instructor": [
                "Accept the collaborator invite (GitHub notifications bell).",
                "Continue with Step 1b — you wire deploy; the student does not touch Railway.",
            ],
            "link": {"label": "Open the template on GitHub", "href": TEMPLATE_REPO},
        },
        {
            "num": "1b",
            "title": "Wire deploy: student GitHub → your Railway",
            "summary": "You create a token. Student saves it as GitHub secret RAILWAY_TOKEN. Actions deploys on every merge to main.",
            "student": [
                "**Wait** until your instructor sends you a long token string (looks like `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`).",
                "Open your repo on GitHub → top tab **Settings** (the repo's settings — not your profile picture menu).",
                "Left sidebar → **Secrets and variables** → **Actions**.",
                "Click **New repository secret**.",
                "**Name** field — type exactly: `RAILWAY_TOKEN` (all caps, underscore, no spaces).",
                "**Secret** field — paste the entire token string from your instructor (one line, ~36 characters).",
                "Click **Add secret**.",
                "Confirm: the Actions secrets page now shows a row named **RAILWAY_TOKEN** (GitHub hides the value — that is normal).",
                "You never visit railway.com and you never install any Railway app.",
            ],
            "instructor": [
                "**First — create the token (you only):** open https://railway.com → your student Railway project → **Settings** (project gear, not the web service) → **Tokens** → **Create Token** → environment **production** → copy the token immediately (shown once).",
                "Send that token to the student by text or screen share — never commit it to git.",
                "**Second — confirm workflow file:** the student's repo `main` branch must contain `.github/workflows/railway-deploy.yml`.",
                "**Third — student adds secret:** they follow the Student steps above. Verify on screen share: repo **Settings → Secrets and variables → Actions** must show **RAILWAY_TOKEN** in the list.",
                "**Fourth — disconnect old source:** **web** service → **Settings** → **Source** → **Disconnect** if it still shows `premierepc-ops/coding-course-starter`.",
                "**Fifth — test deploy:** student repo → **Actions** tab → **Deploy to Railway** → **Run workflow** → wait for green checkmark (~2 min).",
                f"**Sixth — verify live site:** open {LIVE_SITE_URL}/healthz — page must show `ok`.",
                "**Railway web → Settings → Source will show empty** — correct. Deploys come from the student's repo Actions tab, not Source.",
                "Keep Railway Variables (`LEARNER_PIN`, etc.) and the `/data` volume — do not wipe the project.",
            ],
        },
        {
            "num": 2,
            "title": "Install Cursor and Python",
            "summary": "Cursor is the editor. Python runs your code — Cursor does not include Python.",
            "student": [
                "Install **Cursor** from https://cursor.com",
                "Install **Python 3** from https://python.org/downloads/ — required to run code in the terminal (Windows: check **Add Python to PATH**).",
                "Cursor **Extensions → Python** (Microsoft) is optional — it helps edit `.py` files but does **not** replace installing Python from python.org.",
                "**Git:** Cursor has Git built in (Source Control sidebar, **Git: Clone** in Step 3). In terminal run `git --version` — if you see a version, skip Git install. If not, install from https://git-scm.com/downloads once.",
                "Verify in Cursor terminal: `python --version` must print a version. `git --version` must work before Step 3.",
            ],
            "instructor": [
                "Python missing or not on PATH is the usual Windows blocker — fix that before Step 5.",
                "Use Cursor's Git UI for commit/push later; no need to teach git CLI commands in Phase 1.",
            ],
            "link": {"label": "Download Cursor", "href": "https://cursor.com"},
        },
        {
            "num": 3,
            "title": "Clone your repo in Cursor",
            "summary": "Get the code on your computer.",
            "student": [
                "Cursor → Ctrl+Shift+P (Cmd on Mac) → **Git: Clone**.",
                "Paste **your** repo HTTPS URL → pick a folder → open.",
                "Sidebar should show `app.py`, `blueprints/`, `templates/`.",
            ],
            "instructor": [
                "Confirm they cloned **their** repo, not the template URL.",
            ],
        },
        {
            "num": 4,
            "title": "Sign in on the live site",
            "summary": "URL and PIN from your instructor.",
            "student": [
                f"Open {LIVE_SITE_URL} (or the URL your instructor gives you).",
                "Click **Sign in** → choose your name → enter your PIN → **Continue**.",
                "Course Home should show your name at the top.",
            ],
            "instructor": [
                "Give the live URL and LEARNER_PIN in person — not in git.",
                "Registration is via Railway Variables or course_config.py — the student never edits this.",
            ],
            "link": {"label": "Go to Sign in", "href": "/login"},
        },
        {
            "num": 5,
            "title": "Type and run hello.py",
            "summary": "No AI — the student types every character.",
            "student": [
                "Create `lessons/yourname/hello.py` in the repo.",
                'Type yourself: `print("Hello, world!")` and `print("I typed this myself.")`',
                "Save → Terminal → `python lessons/yourname/hello.py` — both lines must print.",
            ],
            "instructor": [
                "Enforce predict-then-run. No AI for this step.",
            ],
        },
        {
            "num": 6,
            "title": "About Me → pull request → live",
            "summary": "First change that ships to the live URL.",
            "student": [
                "Edit `blueprints/aboutme/templates/aboutme/index.html` with something about you.",
                "With your instructor: commit, push a branch, open a pull request on GitHub.",
                "After they merge to `main`, wait ~2 min — your repo **Actions** tab runs **Deploy to Railway** automatically.",
                "Then visit the live About Me page (link below) to see your change.",
            ],
            "instructor": [
                "Review and **merge** the PR to `main`.",
                "GitHub Actions **Deploy to Railway** runs automatically (~2 min). Check green on the student's repo **Actions** tab.",
                f"Student visits {LIVE_SITE_URL}/aboutme/ to verify.",
                "Update `.learners/<slug>/progress.md` in their repo when Phase 1 is complete.",
            ],
            "link": {"label": "Preview About Me", "href": "/aboutme/"},
        },
    ],
}

SETUP_STEPS = [
    {
        "id": "tools_read",
        "step_num": 0,
        "label": "Phase 0 — read Meet your tools",
        "manual": True,
        "link": START_GUIDE["steps"][0]["link"],
    },
    {
        "id": "own_repo",
        "step_num": 1,
        "label": "Create your GitHub repo",
        "manual": True,
        "link": START_GUIDE["steps"][1]["link"],
    },
    {
        "id": "railway_source",
        "step_num": "1b",
        "label": "Instructor: wire GitHub Actions deploy",
        "manual": True,
        "instructor_only": True,
    },
    {
        "id": "tools",
        "step_num": 2,
        "label": "Install Cursor and Python",
        "manual": True,
        "link": START_GUIDE["steps"][3]["link"],
    },
    {
        "id": "clone",
        "step_num": 3,
        "label": "Clone your repo in Cursor",
        "manual": True,
    },
    {
        "id": "signin",
        "step_num": 4,
        "label": "Sign in on the live site",
        "manual": False,
        "link": START_GUIDE["steps"][5]["link"],
    },
    {
        "id": "hello",
        "step_num": 5,
        "label": "Type and run hello.py yourself",
        "manual": True,
    },
    {
        "id": "aboutme",
        "step_num": 6,
        "label": "Customize About Me and merge a PR",
        "manual": True,
        "link": START_GUIDE["steps"][7]["link"],
    },
]
