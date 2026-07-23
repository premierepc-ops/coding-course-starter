# Codebase Recon — coding-course-starter (for <NAME>)

_Written by the Cursor agent during Phase 0. Shared with the learner in Phase 3._

> Do a FRESH recon per learner — don't copy an old one. The codebase changes. Fill this in by actually
> reading the repo now, using the Phase 0 checklist in `TRAINING_PROGRAM.md`.

## What kind of app is this?

<stack: Python, Flask, Jinja2, SQLite via site_paths.py>

## How to run it locally

<commands: pip install, cp .env.example .env, python app.py>

## The entry point

<app.py — registers blueprints, healthz, home route>

## Blueprints / sections

<table: blueprint | url prefix | what it does>

## Where data lives

<DATA_DIR, db_path(), Railway volume at /data>

## How secrets are handled

<.env locally, Railway Variables in prod, .gitignore>

## Deploy pipeline

<GitHub push to main → Railway Nixpacks build → Gunicorn on $PORT → healthcheck /healthz>

## What I found that's worth knowing

<anything surprising — flag in notes-for-instructor.md>

## Part B — HTMX reference (Phase 3 addendum)

_Filled in Phase 3 — trace `/guestbook/` in this repo._

<HTMX flow traced, quiz login, reference blueprint>
