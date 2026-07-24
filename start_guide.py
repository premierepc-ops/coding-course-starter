"""Plain-English Phase 1 directions shown at /start and on the course home checklist."""

from course_config import TEMPLATE_REPO

START_GUIDE = {
    "title": "Phase 1 — Start here",
    "time_estimate": "About 60–90 minutes with your instructor",
    "intro": (
        "Brand new to coding? Start with Phase 0 — read Meet your tools so the words make sense. "
        "Then follow these steps in order with your instructor. "
        "When a step is done, come back to Course Home and sign in."
    ),
    "steps": [
        {
            "num": 0,
            "title": "Phase 0 — read Meet your tools",
            "summary": "Learn what GitHub, Python, Cursor, Railway, and the rest actually mean.",
            "directions": [
                "Open Meet your tools in the menu (or go to /tools).",
                "Read each definition once — you are not being quizzed on vocabulary.",
                "Ask your instructor anything that still sounds like gibberish.",
                "When the map makes sense, continue to Step 1 below.",
            ],
            "link": {"label": "Read the glossary", "href": "/tools"},
        },
        {
            "num": 1,
            "title": "Make your own copy of this project on GitHub",
            "summary": "You need your own repo — not the shared template.",
            "directions": [
                f"Open: {TEMPLATE_REPO}",
                "Top right, click the green **Use this template** button, then **Create a new repository**.",
                "Owner: your GitHub account (not premierepc-ops).",
                "Repository name: something like `yourname-coding-course` (lowercase, hyphens OK).",
                "Visibility: **Private** — required. Your name and progress files must not be public on GitHub.",
                "Leave everything else default. Click **Create repository**.",
                "Copy the repo HTTPS URL (green Code button) — send it to your instructor. They need it for Railway.",
                "Settings → Collaborators → invite your instructor's GitHub username so they can review PRs and connect deploy.",
                "Your repo lives on **your** GitHub — it does not appear in premierepc-ops until you invite them.",
            ],
            "link": {"label": "Open the template on GitHub", "href": TEMPLATE_REPO},
        },
        {
            "num": 2,
            "title": "Install the tools",
            "summary": "Three free apps — install once, use all course.",
            "directions": [
                "Cursor — the code editor where you type and run programs (Phase 0 explains what this is).",
                "Python 3 — the language you'll write. Download at https://python.org/downloads/ "
                "(on Windows, check Add Python to PATH during install).",
                "Git — saves versions of your code so you never lose work. Usually comes with Cursor; if not: https://git-scm.com/downloads",
                "After installing, open Cursor's terminal and run: python --version and git --version — both should print a version number.",
            ],
            "link": {"label": "Download Cursor", "href": "https://cursor.com"},
        },
        {
            "num": 3,
            "title": "Clone your repo and open it in Cursor",
            "summary": "Get the code on your computer.",
            "directions": [
                "Open Cursor.",
                "Press Ctrl+Shift+P (Windows) or Cmd+Shift+P (Mac), type Git: Clone, press Enter.",
                "Paste the URL of your repo (from GitHub — green Code button → HTTPS).",
                "Pick a folder (e.g. Documents/code) and open the cloned project.",
                "You should see folders like blueprints, templates, and app.py in the sidebar.",
            ],
        },
        {
            "num": 4,
            "title": "Sign in on this website",
            "summary": "So quizzes and your dashboard know it's you.",
            "directions": [
                "Before sign-in works, your instructor registers you — either in course_config.py in your repo "
                "or via Railway Variables (LEARNER_SLUG, LEARNER_NAME) on the live site.",
                "Ask your instructor for your sign-in PIN and the live site URL (usually ends in .up.railway.app).",
                "Open that URL in your browser — not localhost unless you're running the app yourself.",
                "Click Sign in in the top menu.",
                "Choose your name from the list, type your PIN, click Continue.",
                "You'll land on Course Home with your name at the top.",
            ],
            "link": {"label": "Go to Sign in", "href": "/login"},
        },
        {
            "num": 5,
            "title": "Type and run your first Python file",
            "summary": "No AI for this one — your fingers on the keyboard.",
            "directions": [
                "In Cursor's file explorer (left sidebar), right-click the project root → New Folder → name it lessons.",
                "Right-click lessons → New Folder → name it your first name in lowercase (e.g. alex).",
                "Right-click that folder → New File → name it hello.py.",
                "Click hello.py to open it. Type these two lines yourself (don't copy from AI):",
                '  print("Hello, world!")',
                '  print("I typed this myself.")',
                "Save the file (Ctrl+S / Cmd+S).",
                "Open the terminal: menu Terminal → New Terminal. Run:",
                "  python lessons/yourname/hello.py",
                "(Replace yourname with your folder name.) You should see both lines printed. If you get an error, read it out loud — that's debugging.",
            ],
        },
        {
            "num": 6,
            "title": "Customize your About Me page",
            "summary": "Your first change to the live app.",
            "directions": [
                "In your repo, open blueprints/aboutme/templates/aboutme/index.html.",
                "Change the placeholder text to something about you (hobbies, fun fact, photo link).",
                "Save the file. Your instructor will help you commit, push, and open a pull request.",
                "After the PR merges, open /aboutme/ on the live site (your Railway URL).",
                "About Me also appears in the top menu once your instructor marks Phase 1 in your progress.",
            ],
            "link": {"label": "Preview About Me page", "href": "/aboutme/"},
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
        "label": "Make your own copy on GitHub",
        "manual": True,
        "link": START_GUIDE["steps"][1]["link"],
    },
    {
        "id": "tools",
        "step_num": 2,
        "label": "Install Cursor, Python 3, and Git",
        "manual": True,
        "link": START_GUIDE["steps"][2]["link"],
    },
    {
        "id": "clone",
        "step_num": 3,
        "label": "Clone your repo and open it in Cursor",
        "manual": True,
    },
    {
        "id": "signin",
        "step_num": 4,
        "label": "Sign in on this site (name + PIN)",
        "manual": False,
        "link": START_GUIDE["steps"][4]["link"],
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
        "link": START_GUIDE["steps"][6]["link"],
    },
]
