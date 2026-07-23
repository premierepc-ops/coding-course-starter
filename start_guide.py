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
                f"Open the template: {TEMPLATE_REPO}",
                'Click "Use this template" (green button, top right) — that creates your own repo from the starter.',
                'If you see "Fork" instead, that works too — same idea: your own copy on your GitHub account.',
                'Click "Create a new repository".',
                "Name it something like jaqira-coding-course (all lowercase, use hyphens).",
                "Prefer Private if you don't want your name or progress files visible on GitHub. Public works too.",
                "Click Create repository. That new repo is yours — the rest of the course happens there.",
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
                "Before sign-in works, your instructor registers you — either in course_config.py in your fork "
                "or via Railway Variables (LEARNER_SLUG, LEARNER_NAME) on the live site.",
                "Ask your instructor for your sign-in PIN (they set it — you don't pick it yourself).",
                "Click Sign in in the top menu of this site.",
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
                "Right-click lessons → New Folder → name it your first name in lowercase (e.g. jaqira).",
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
                "After the PR merges, visit About Me in the menu above — your changes should be live.",
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
        "id": "fork",
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
