"""Student-facing phase guides — Phase 1 at /start, Phases 2–6 at /session/<n>."""

from start_guide import START_GUIDE

SESSION_2_GUIDE = {
    "session_num": 2,
    "phase_num": 2,
    "title": "Phase 2 — Python & git fluency",
    "time_estimate": "About 90–120 minutes with your instructor",
    "intro": (
        "Phase 1 got your tools working and your first page live. Now you write real Python — "
        "lists, loops, functions — and git becomes habit, not mystery. AI can help you explore; "
        "you still explain every line before it ships."
    ),
    "milestones": [
        "Write and reason about lists, loops, functions, and dicts",
        "Branch, commit, merge (merge conflict with help is fine)",
        "Read AI-generated code and explain every line out loud",
    ],
    "steps": [
        {
            "num": 1,
            "title": "Warm up — predict before you run",
            "summary": "The habit that separates guessing from learning.",
            "directions": [
                "Open lessons/yourname/hello.py from Phase 1.",
                "Before running it, say out loud what you think each line will print.",
                "Run it. Were you right? If not, that's the lesson — read the error or output and fix your mental model.",
                "Your instructor will ask you to predict before every run this session. No 'I don't know' — make your best guess.",
            ],
        },
        {
            "num": 2,
            "title": "Build family.py — list → loop → if → function → dict",
            "summary": "One script that grows step by step.",
            "directions": [
                "In lessons/yourname/, create family.py.",
                "Start with a list of three names (real or silly). Print each name in a loop.",
                "Add an if statement — e.g. only print names longer than 4 letters.",
                "Refactor the loop body into a function greet(name) that returns a string.",
                "Convert the list to a dict: name → age (or favorite color). Loop the dict with .items().",
                "Run after each small change. Predict the output first.",
            ],
        },
        {
            "num": 3,
            "title": "Git branches drill",
            "summary": "Try something without breaking main.",
            "directions": [
                "In Cursor's terminal, make sure you're on main and everything is committed.",
                "Create a branch: git checkout -b practice-family",
                "Change one line in family.py. Commit with a message in your own words.",
                "Switch back: git checkout main — notice family.py reverts.",
                "Switch to your branch again and merge into main (your instructor helps if there's a conflict).",
                "Push to GitHub when your instructor says so.",
            ],
        },
        {
            "num": 4,
            "title": "AI literacy — comment before you run",
            "summary": "Use Cursor AI to explore, then prove you understand.",
            "directions": [
                "Ask Cursor to write a short script (e.g. mystery.py) that uses a loop and an if.",
                "Before running: add a comment above every line in your own words — what does it do?",
                "Read those comments out loud to your instructor.",
                "Only then run it. If output surprises you, find which line caused it.",
            ],
        },
        {
            "num": 5,
            "title": "Mini project — read JSON, print formatted output",
            "summary": "Combine what you built with a real file.",
            "directions": [
                "Create people.json in lessons/yourname/ with a list of objects (name, age).",
                "Write read_people.py that opens the file, loads JSON, and prints each person nicely.",
                "Use AI if you're stuck — but you must explain every line before commit.",
                "Commit and push to main (practice files in lessons/ are OK on main).",
            ],
        },
        {
            "num": 6,
            "title": "Phase 2 quiz",
            "summary": "Unlock Phase 3 when you pass (70%+).",
            "directions": [
                "Sign in on this site if you're not already.",
                "Take the Phase 2 quiz — scenario questions, not memorized definitions.",
                "Below 70%? Your instructor helps you review wrong answers, then you retake.",
                "Passed? Phase 3 unlocks on Course Home.",
            ],
            "link": {"label": "Open Phase 2 quiz", "href": "/quiz/phase/2"},
        },
    ],
}

SESSION_3_GUIDE = {
    "session_num": 3,
    "phase_num": 3,
    "title": "Phase 3 — Extend the real app",
    "time_estimate": "About 2–3 hours (may split across two meetings)",
    "intro": (
        "You stop editing only practice files and start changing this Flask app. "
        "Copy patterns from the guestbook — routes, SQLite, HTMX — don't google generic tutorials."
    ),
    "milestones": [
        "App running locally on your laptop",
        "New route added on a branch",
        "HTMX interactivity copied from /guestbook",
        "Small feature working locally (deploy comes in Phase 4)",
    ],
    "steps": [
        {
            "num": 1,
            "title": "Run the app locally",
            "summary": "See the same site on localhost before you change it.",
            "directions": [
                "Copy .env.example to .env and set SECRET_KEY (ask your instructor).",
                "In terminal: pip install -r requirements.txt",
                "Run: python app.py — open http://127.0.0.1:5000",
                "Click through Home, About Me, Guestbook. Same app, on your machine.",
            ],
        },
        {
            "num": 2,
            "title": "Recon the guestbook — trace the request",
            "summary": "Read .learners/yourname/recon.md, then verify with your eyes.",
            "directions": [
                "Open /guestbook/ locally. Submit a test message.",
                "In Cursor, open blueprints/guestbook/__init__.py and templates/guestbook/",
                "Trace on paper: browser → hx-post → route → database → partial HTML back.",
                "Ask your instructor anything that still feels like magic.",
            ],
            "link": {"label": "Open guestbook locally", "href": "/guestbook/"},
        },
        {
            "num": 3,
            "title": "Add a simple route on a branch",
            "summary": "Your first new URL in the app.",
            "directions": [
                "git checkout -b feature-my-route",
                "Pick an existing blueprint (aboutme is easiest) or ask your instructor about a new one.",
                "Add a route that returns HTML. Run locally and visit the URL.",
                "Predict the URL before you refresh the browser.",
            ],
            "link": {"label": "Preview About Me", "href": "/aboutme/"},
        },
        {
            "num": 4,
            "title": "Copy the HTMX pattern",
            "summary": "Form → hx-post → partial template swap.",
            "directions": [
                "Read guestbook/index.html and _messages.html side by side.",
                "Copy the pattern for your feature: notes wall, poll, or shout box — your pick.",
                "Use the same get_db() / SQLite style as guestbook.",
                "Test locally: submit, see new content without full page reload.",
            ],
        },
        {
            "num": 5,
            "title": "Build your feature to completion",
            "summary": "Working end-to-end on your branch — not deployed yet.",
            "directions": [
                "Empty input, weird characters, too-long text — try breaking it yourself.",
                "Fix what breaks. Explain each fix out loud.",
                "Commit often. Push the branch to GitHub.",
                "Open a PR when your instructor says — they review; they merge.",
            ],
        },
        {
            "num": 6,
            "title": "Phase 3 quiz",
            "summary": "Pass before Phase 4 deploy day.",
            "directions": [
                "Take Phase 3 quiz when your feature works locally.",
                "70%+ to advance. Review wrong answers with your instructor if not.",
            ],
            "link": {"label": "Open Phase 3 quiz", "href": "/quiz/phase/3"},
        },
    ],
}

SESSION_4_GUIDE = {
    "session_num": 4,
    "phase_num": 4,
    "title": "Phase 4 — Railway & deploy",
    "time_estimate": "About 60–90 minutes",
    "intro": (
        "Git push becomes a live site. You learn to read Railway logs when something breaks — "
        "because something will break, and that's normal."
    ),
    "milestones": [
        "Understand GitHub → Railway connection",
        "Know where env vars live (Railway Variables, not code)",
        "Watch a successful deploy after a merged PR",
        "See your Phase 3 feature on your phone",
    ],
    "steps": [
        {
            "num": 1,
            "title": "Trace the deploy path",
            "summary": "Commit → push → build → live.",
            "directions": [
                "With your instructor, open Railway dashboard for your project.",
                "Find: connected GitHub repo, branch (main), latest deployment.",
                "Walk through: you merge PR → GitHub webhook → Railway build → Gunicorn starts.",
                "Visit /healthz on the live URL — should return ok.",
            ],
            "link": {"label": "Live health check", "href": "/healthz"},
        },
        {
            "num": 2,
            "title": "Env vars and DATA_DIR",
            "summary": "Secrets and data live outside your code.",
            "directions": [
                "In Railway Variables: SECRET_KEY, INSTRUCTOR_PASSWORD, LEARNER_PIN, DATA_DIR=/data.",
                "Your instructor confirms the volume is mounted at /data.",
                "Never put secrets in git — .env is local only, listed in .gitignore.",
            ],
        },
        {
            "num": 3,
            "title": "Ship your Phase 3 feature",
            "summary": "Merge the PR and watch it go live.",
            "directions": [
                "Instructor merges your Phase 3 PR to main.",
                "Watch the deploy in Railway — green checkmark.",
                "Hard-refresh the live site (Ctrl+Shift+R). Try your feature on your phone.",
            ],
        },
        {
            "num": 4,
            "title": "Debug drill — change not showing?",
            "summary": "Stale cache, wrong branch, or failed deploy.",
            "directions": [
                "Your instructor may simulate a problem — find the real cause.",
                "Check: did the right branch merge? did deploy succeed? hard refresh?",
                "Open Railway deploy logs and runtime logs. Read the traceback out loud.",
            ],
        },
        {
            "num": 5,
            "title": "Phase 4 quiz",
            "summary": "Deploy knowledge check.",
            "directions": [
                "Take Phase 4 quiz after your feature is live on Railway.",
            ],
            "link": {"label": "Open Phase 4 quiz", "href": "/quiz/phase/4"},
        },
    ],
}

SESSION_5_GUIDE = {
    "session_num": 5,
    "phase_num": 5,
    "title": "Phase 5 — Security",
    "time_estimate": "About 90 minutes",
    "intro": (
        "Your app is on the public internet. Learn what attackers try, what HTTPS actually does, "
        "and how to keep secrets out of git."
    ),
    "milestones": [
        "Explain HTTPS in plain English",
        "Keep secrets in Railway Variables / .env only",
        "Describe XSS in one sentence",
        "Write THREATS.md in your repo",
    ],
    "steps": [
        {
            "num": 1,
            "title": "HTTPS on your live URL",
            "summary": "What the lock icon means — and doesn't mean.",
            "directions": [
                "Open your Railway URL. Click the lock in the browser bar.",
                "Explain: HTTPS encrypts traffic in transit. It does not mean 'hackers can't touch my app.'",
            ],
        },
        {
            "num": 2,
            "title": "Secrets hygiene",
            "summary": "If it's in git, assume the world can read it.",
            "directions": [
                "Show .gitignore — .env should be listed.",
                "Run git log -p on a safe example — your instructor shows why committed secrets are permanent.",
                "Compare: code in GitHub vs secrets in Railway Variables.",
            ],
        },
        {
            "num": 3,
            "title": "XSS demo on your guestbook or form",
            "summary": "See autoescaping save you — then understand why.",
            "directions": [
                "Try submitting <script>alert('hi')</script> in a message field.",
                "What happened? Jinja autoescapes by default — explain that in one sentence.",
                "Your instructor may show what | safe would break.",
            ],
            "link": {"label": "Open guestbook", "href": "/guestbook/"},
        },
        {
            "num": 4,
            "title": "Write THREATS.md",
            "summary": "One page threat model in your words.",
            "directions": [
                "Create THREATS.md in your repo root.",
                "Answer: Who might attack this app? What do they want? How would they try? What stops them?",
                "Commit on a branch, PR, merge with instructor review.",
            ],
        },
        {
            "num": 5,
            "title": "Phase 5 quiz",
            "summary": "Security scenarios — pass at 70%+.",
            "directions": [
                "Take Phase 5 quiz after THREATS.md is merged.",
            ],
            "link": {"label": "Open Phase 5 quiz", "href": "/quiz/phase/5"},
        },
    ],
}

SESSION_6_GUIDE = {
    "session_num": 6,
    "phase_num": 6,
    "title": "Phase 6 — Capstone & demo night",
    "time_estimate": "Multiple sessions — plan 1–2 weeks",
    "intro": (
        "You pick a feature, write a spec, build it, deploy it, and explain every line to your instructor. "
        "This is graduation."
    ),
    "milestones": [
        "CAPSTONE.md written and instructor-approved",
        "Feature built and deployed on Railway",
        "Demo night — explain every line",
        "Final quiz passed",
    ],
    "steps": [
        {
            "num": 1,
            "title": "Write your capstone spec",
            "summary": "One paragraph before any code.",
            "directions": [
                "Create .learners/yourname/CAPSTONE.md",
                "What does it do? Who uses it? What does success look like?",
                "Your instructor signs off on scope before you build.",
            ],
        },
        {
            "num": 2,
            "title": "Build on a branch",
            "summary": "Daily commits. Scoped AI prompts.",
            "directions": [
                "git checkout -b capstone",
                "Build the feature copying patterns from this codebase (routes, DB, HTMX).",
                "Use AI in batches — one scoped prompt per milestone, not ten micro-prompts.",
                "Every commit message in your own words.",
            ],
        },
        {
            "num": 3,
            "title": "Edge cases + README",
            "summary": "Polish like a real ship.",
            "directions": [
                "Test empty input, weird characters, too-long text.",
                "Write a README for your feature — how to use it, what files you touched.",
                "Open PR. Instructor reviews and merges. Verify on live URL.",
            ],
        },
        {
            "num": 4,
            "title": "Final exam",
            "summary": "All phases — locked until phase quizzes are done.",
            "directions": [
                "Complete any remaining phase quizzes first.",
                "Take the final at /quiz/final — 100 questions, no lookups.",
            ],
            "link": {"label": "Quiz dashboard", "href": "/quiz/"},
        },
        {
            "num": 5,
            "title": "Demo night",
            "summary": "Walk through every file. Explain every line.",
            "directions": [
                "Screen share or sit together. You drive.",
                "Any line you can't explain gets removed or rewritten before you graduate.",
                "Celebrate — you shipped something real.",
            ],
        },
    ],
}

SESSION_GUIDES: dict[int, dict] = {
    1: {**START_GUIDE, "session_num": 1, "phase_num": 1},
    2: SESSION_2_GUIDE,
    3: SESSION_3_GUIDE,
    4: SESSION_4_GUIDE,
    5: SESSION_5_GUIDE,
    6: SESSION_6_GUIDE,
}


def session_url(session_num: int) -> str:
    if session_num == 1:
        return "/start"
    return f"/session/{session_num}"


def session_unlocked(session_num: int, unlocked_phase: int, is_instructor: bool, signed_in: bool) -> bool:
    if is_instructor:
        return True
    if session_num == 1:
        return True
    if not signed_in:
        return False
    return unlocked_phase >= session_num


def _session_short_title(num: int, title: str) -> str:
    for prefix in (f"Phase {num} — ", f"Session {num} — "):
        if title.startswith(prefix):
            return title[len(prefix) :]
    return title


def sessions_for_nav(unlocked_phase: int, is_instructor: bool, signed_in: bool) -> list[dict]:
    out = [
        {
            "num": 0,
            "title": "Phase 0 — Meet your tools",
            "short_title": "Meet your tools",
            "href": "/tools",
            "phase_num": 0,
            "unlocked": True,
        }
    ]
    for num in sorted(SESSION_GUIDES):
        guide = SESSION_GUIDES[num]
        title = guide["title"]
        out.append(
            {
                "num": num,
                "title": title,
                "short_title": _session_short_title(num, title),
                "href": session_url(num),
                "phase_num": guide.get("phase_num", num),
                "unlocked": session_unlocked(num, unlocked_phase, is_instructor, signed_in),
            }
        )
    return out
