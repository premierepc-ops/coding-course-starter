"""Plain-English Session 1 directions shown at /start and on the course home checklist."""

from course_config import TEMPLATE_REPO

START_GUIDE = {
    "title": "Session 1 — Start here",
    "intro": (
        "Brand new to coding? Follow these steps in order. "
        "Do them with your instructor the first time — that's normal. "
        "When a step is done, come back to Course Home and sign in."
    ),
    "steps": [
        {
            "num": 1,
            "title": "Make your own copy of this project on GitHub",
            "summary": "You need your own repo — not the shared template.",
            "directions": [
                f"Open the template: {TEMPLATE_REPO}",
                'Click the green "Use this template" button (top right).',
                'Click "Create a new repository".',
                "Name it something like jaqira-coding-course (all lowercase, use hyphens).",
                "Leave it Public or Private — your choice. Click Create repository.",
                "That new repo is yours. The rest of the course happens there.",
            ],
            "link": {"label": "Open the template on GitHub", "href": TEMPLATE_REPO},
        },
        {
            "num": 2,
            "title": "Install the tools",
            "summary": "Three free apps — install once, use all course.",
            "directions": [
                "Cursor — your code editor with AI built in. Download at https://cursor.com (free Hobby plan).",
                "Python 3 — the language you'll write. Download at https://python.org/downloads/ "
                "(check Add Python to PATH on Windows during install).",
                "Git — saves versions of your code. Usually comes with Cursor; if not: https://git-scm.com/downloads",
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
                "Paste the URL of your fork (from GitHub — green Code button → HTTPS).",
                "Pick a folder (e.g. `Documents/code`) and open the cloned project.",
                "You should see folders like `blueprints`, `templates`, and `app.py` in the sidebar.",
            ],
        },
        {
            "num": 4,
            "title": "Sign in on this website",
            "summary": "So quizzes and your dashboard know it's you.",
            "directions": [
                "Ask your instructor for your sign-in PIN (they set it — you don't pick it yourself).",
                "Click Sign in in the top menu of this site.",
                "Choose your name from the list, type your PIN, click **Continue**.",
                "You'll land on Course Home with your name at the top.",
            ],
            "link": {"label": "Go to Sign in", "href": "/login"},
        },
        {
            "num": 5,
            "title": "Type and run your first Python file",
            "summary": "No AI for this one — your fingers on the keyboard.",
            "directions": [
                "In Cursor, create a folder lessons/yourname/ (use your first name, lowercase).",
                "Create a file hello.py in that folder.",
                "Type these two lines yourself (don't copy from AI):",
                '  print("Hello, world!")',
                '  print("I typed this myself.")',
                "Open the terminal in Cursor (Terminal → New Terminal) and run:",
                "  python lessons/yourname/hello.py",
                "You should see both lines printed. If you get an error, read it out loud — that's debugging.",
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
        "id": "fork",
        "label": "Fork the template on GitHub",
        "directions": START_GUIDE["steps"][0]["directions"],
        "link": START_GUIDE["steps"][0]["link"],
    },
    {
        "id": "tools",
        "label": "Install Cursor, Python 3, and Git",
        "directions": START_GUIDE["steps"][1]["directions"],
        "link": START_GUIDE["steps"][1]["link"],
    },
    {
        "id": "clone",
        "label": "Clone your repo and open it in Cursor",
        "directions": START_GUIDE["steps"][2]["directions"],
    },
    {
        "id": "signin",
        "label": "Sign in on this site (name + PIN from your instructor)",
        "directions": START_GUIDE["steps"][3]["directions"],
        "link": START_GUIDE["steps"][3]["link"],
    },
    {
        "id": "hello",
        "label": "Type and run hello.py yourself",
        "directions": START_GUIDE["steps"][4]["directions"],
    },
    {
        "id": "aboutme",
        "label": "Customize your About Me page and merge a PR",
        "directions": START_GUIDE["steps"][5]["directions"],
        "link": START_GUIDE["steps"][5]["link"],
    },
]
