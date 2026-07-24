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
        "Her repo stays on her GitHub. You are a collaborator on Railway. "
        "She never signs up for Railway — she pastes one secret in GitHub only."
    ),
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
                "The live site still builds the **template** repo for now — that is OK for Phase 0.",
            ],
            "link": {"label": "Read the glossary", "href": "/tools"},
        },
        {
            "num": 1,
            "title": "Create your GitHub repo",
            "summary": "Your repo on your GitHub account — not the shared template.",
            "student": [
                f"Open {TEMPLATE_REPO}",
                "Click green **Use this template** → **Create a new repository**.",
                "Owner: **your** GitHub account (not premierepc-ops).",
                "Name: e.g. `jaqira-coding-course` (lowercase, hyphens OK).",
                "Visibility: **Private** (required).",
                "Click **Create repository**.",
                f"Settings → Collaborators → invite **`{INSTRUCTOR_GITHUB}`**.",
                "Copy HTTPS URL (Code → HTTPS) and send it to your instructor.",
            ],
            "instructor": [
                "Accept the collaborator invite (GitHub notifications bell).",
                "Continue with Step 1b — you wire deploy; she does not touch Railway.",
            ],
            "link": {"label": "Open the template on GitHub", "href": TEMPLATE_REPO},
        },
        {
            "num": "1b",
            "title": "Wire her repo to your Railway project",
            "summary": "Instructor sets up deploy — student pastes one GitHub secret (no Railway account).",
            "student": [
                "Repo → **Settings → Secrets and variables → Actions** → **New repository secret**.",
                "Name: `RAILWAY_TOKEN` — value: paste the token your instructor sends you.",
                "No railway.com login. GitHub only.",
            ],
            "instructor": [
                "Railway → project **jaqira-course** → **Settings → Tokens** → create a **production** project token.",
                "Push `.github/workflows/railway-deploy.yml` to her repo (already in the template if you pull latest).",
                "Send her the token — she adds it as GitHub secret `RAILWAY_TOKEN` (Step 1b student lines above).",
                "Optional: **web** service → **Settings → Source → Disconnect** so the template repo stops auto-deploying.",
                "Trigger a test: push an empty commit to her `main` or use **Actions → Deploy to Railway → Run workflow**.",
                f"Confirm {LIVE_SITE_URL}/healthz returns ok.",
                "Keep existing Variables and the /data volume.",
            ],
        },
        {
            "num": 2,
            "title": "Install Cursor, Python 3, and Git",
            "summary": "On the student's laptop only.",
            "student": [
                "Install Cursor from https://cursor.com",
                "Install Python 3 from https://python.org/downloads/ (Windows: check **Add Python to PATH**).",
                "Install Git from https://git-scm.com/downloads if Cursor did not include it.",
                "In Cursor terminal run: `python --version` and `git --version` — both must print a version.",
            ],
            "instructor": [
                "Watch installs; troubleshoot Windows PATH if `python` is not found.",
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
            ],
            "instructor": [
                "Review and **merge** the PR to `main` (only works if Step 1b Source is their repo).",
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
        "label": "Instructor: connect Railway Source",
        "manual": True,
        "instructor_only": True,
    },
    {
        "id": "tools",
        "step_num": 2,
        "label": "Install Cursor, Python 3, and Git",
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
