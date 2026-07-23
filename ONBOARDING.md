# Onboarding a New Learner

See the full checklist in the instructor copy at `family-rydzfski/ONBOARDING.md`. This file mirrors the
student-facing steps for learners working in **their fork** of this repo.

Work top to bottom with your instructor (Dad). Steps marked **[Dad]** need instructor setup.

---

## 0. Prerequisites

- A computer you control (Windows/Mac/Linux).
- A **GitHub account** (create one at github.com if needed).
- Installs for Session 1: **Cursor** (free Hobby tier), **Python 3**, **Git**.

## 1. Fork and clone this repo

1. Fork `coding-course-starter` on GitHub to your account.
2. Clone your fork and open it in Cursor:
   ```bash
   git clone https://github.com/YOUR_USERNAME/coding-course-starter.git
   cd coding-course-starter
   ```

## 2. Create your learner folder

```
cp -r .learners/_TEMPLATE .learners/your-slug
```

Fill in `.learners/your-slug/LEARNER.md` with your profile.

## 3. Quiz enrollment

Your instructor registers your email in the family site quiz. Take quizzes at:
**https://family.rydzfski.com/quiz**

## 4. **[Dad]** Railway + SSO

Your instructor will:
- Authorize your Google email on the family site
- Create a Railway project connected to your fork
- Invite you as Editor on your project

## 5. Phase 0 recon → Session 1

Your Cursor agent writes `recon.md` before your first lesson. Then Phase 1 begins — see
`TRAINING_PROGRAM.md`.
