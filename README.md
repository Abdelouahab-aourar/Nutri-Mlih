# The Smart Diet Meal Planner

## Requirements

- [uv](https://docs.astral.sh/uv/) — fast Python package and project manager

## Getting Started

### 1. Install uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or via pip:

```bash
pip install uv
```

### 2. Clone the repository

```bash
git clone https://github.com/Abdelouahab-aourar/The-Smart-Diet-Meal-Planner
cd The-Smart-Diet-Meal-Planner
```

### 3. Set up the environment

uv will automatically create a virtual environment and install all dependencies:

```bash
uv sync
```
## Common Commands

| Task | Command |
|---|---|
| Add a dependency | `uv add requests` |
| Add a dev dependency | `uv add --group dev pytest` |
| Remove a dependency | `uv remove requests` |
| Update all dependencies | `uv sync --upgrade` |
| Show installed packages | `uv pip list` |

## Collaboration Guide
 
### First time — clone the repo
 
```bash
git clone https://github.com/Abdelouahab-aourar/The-Smart-Diet-Meal-Planner
cd The-Smart-Diet-Meal-Planner
uv sync
```
 
---
 
### Create your personal branch
 
Each collaborator works on their own branch named after them. Do this once, right after cloning:
 
```bash
git checkout -b your-name
git push -u origin your-name
```
 
> Example: `git checkout -b abdelouahab` — from now on, **always work on this branch**, never directly on `main`.
 
---
 
### Daily workflow — before you start working
 
Always pull the latest changes from `main` into your branch before touching any code:
 
```bash
git checkout your-name        # make sure you're on your branch
git pull origin main
```
 
If there are conflicts, Git will tell you which files to resolve. Fix them, then:
 
```bash
git add .
git commit -m "resolve merge conflicts with main"
```
 
---
 
### While you work — commit often
 
Small, frequent commits are easier to review and easier to undo:
 
```bash
git add .
git commit -m "short description of what you did"
```
 
---
 
### Push your work
 
Push your branch to the remote so others can see it:
 
```bash
git push origin your-name
```
 
If it's your first push on a new machine:
 
```bash
git push -u origin your-name
```
 
---
 
### Open a Pull Request
 
When your work is ready to be merged into `main`:
 
1. Go to the repository on GitHub.
2. Click **"Compare & pull request"** next to your branch.
3. Write a clear title of your changes.
4. Request a review from a teammate.
5. Once approved, the project maintainer will merge it into `main`.

---
 
### Quick reference
 
| Task | Command |
|---|---|
| Switch to your branch | `git checkout your-name` |
| Pull latest from main | `git pull origin main` |
| Stage all changes | `git add .` |
| Commit | `git commit -m "message"` |
| Push your branch | `git push origin your-name` |
| Check current status | `git status` |
---
 
### Golden rules
 
- ✅ Always pull from `main` before starting work.
- ✅ Commit and push at the end of every session.
- ❌ Never push directly to `main`.
- ❌ Never work on someone else's branch without asking.
