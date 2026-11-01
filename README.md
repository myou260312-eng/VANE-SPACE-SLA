# VANE-SPACE-SLA (v2.0)

Deterministic Multi-Gate Telemetry Validation & Strict Prompt Grounding — v2.0 (demo / test harness)

This repository is a self-contained, testable demonstration of multi-gate telemetry checks and strict prompt grounding. External AI and infra integrations (watsonx, Milvus, FAISS, Redis, PostgreSQL, etc.) are intentionally simulated so the project can run without paid services and remain fully testable in CI.

This v2.0 release includes:
- Deterministic, unit-testable RAG orchestration stub (rag_pipeline.py)
- Strict prompt builder (Python + JavaScript) that reads config from environment variables
- Simulated telemetry validator (vane_space_init.py) with deterministic seeding for tests
- Voice orchestrator demo (extensions-core/voice_agents.py) using environment configuration and structured logging
- Pytest test suite and GitHub Actions CI to enforce tests and coverage
- Sanitized public HTML pages: no personal emails, IDs, or account secrets are published

Quick start

```bash
git clone https://github.com/myou260312-eng/VANE-SPACE-SLA.git
cd VANE-SPACE-SLA
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# run tests
pytest --cov=. --cov-report=term
# run telemetry demo
python vane_space_init.py
# run a RAG demo cycle from Python REPL
python - <<'PY'
from rag_pipeline import run_rag_cycle
print(run_rag_cycle('Check server 01 status', ['Server 01: CPU 42.8% status SECURE'], grounding_strength='strict', seed=42))
PY
```

Environment configuration

This project uses environment variables for anything that would otherwise be a secret or tenant-specific identifier. Copy `.env.example` to `.env` and edit values as needed for local testing. Public defaults are safe placeholders.

Key variables in `.env.example`:
- OUR_IBM_SAAS_ACCOUNT_ID
- OUR_EU_EXPERT_ID
- OUR_CONTRACT_RESELLER_ID
- OUR_CONTRACT_SERVICE_BPA
- OUR_CUSTOMER_INDEX
- OUR_EU_CELLAR_DOC_ID
- OUR_EU_RSS_HASH

Project structure (important files)

- config.py — central config object reading env vars and defining thresholds
- rag_pipeline.py — deterministic RAG orchestration stub (retrieval, prompt-building, inference stub, grounding score)
- strict_prompt_builder.py — Python strict prompt builder (also mirrored in strict_prompt_builder.js for browser demos)
- vane_space_init.py — simulated multi-gate telemetry validator and demo CLI
- extensions-core/voice_agents.py — demo voice orchestrator using env-driven config and logging
- tests/ — pytest suite covering prompt builder, telemetry, RAG flow, and logging
- .github/workflows/ci.yml — CI workflow running pytest + coverage on push and PRs
- .env.example — example env vars (do NOT commit real credentials)
- README.md, CONTRIBUTING.md, SECURITY.md — docs and contributor guidance

Notes about scope and safety

- This repository is a demo. The RAG pipeline and telemetry modules are intentionally self-contained stubs so they can be run in CI without external dependencies or paid services.
- No real credentials, personal emails, or account IDs are included in the public repo. All sensitive values should be provided via environment variables or a secure secret manager in production.
- HTML pages are sanitized and intentionally omit PII. If you need to present public identifiers, add them locally or via environment-driven templating.

Testing and CI

- Unit tests: pytest
- Coverage: pytest-cov (CI enforces a minimum coverage threshold — configurable in `.github/workflows/ci.yml`)
- To run tests locally: `pytest --cov=. --cov-report=term`

## Git workflow and contribution notes

For daily Git operations, branching, and rollback patterns used in this repository, see [docs/git-workflow.md](docs/git-workflow.md).

This repo follows a simple branch model:

- `main` is the stable branch
- `feature/*` is used for new functionality and experiments
- `fix/*` is used for targeted bug fixes
- `hotfix/*` is reserved for urgent recovery work
- `docs/*` is used for documentation and process improvements

Before merging work, always validate locally with the repo's test workflow:

```bash
pytest --cov=. --cov-report=term
```
The CI pipeline in `.github/workflows/ci.yml` runs the same validation on push and pull request events.

## Recommended development flow

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/my-change
# make changes
pytest --cov=. --cov-report=term
git add .
git commit -m "Add my change"
git push -u origin feature/my-change
```

Use this workflow for both feature delivery and controlled rollbacks when needed.
```

File: docs/git-workflow.md
```markdown name=docs/git-workflow.md
# Git workflow and command cheat sheet for VANE-SPACE-SLA

This repository is structured for small, testable, reviewable changes. The default branch is `main`, and feature work should be done in short-lived branches before merging through a pull request.

## Branch strategy

Use this flow for work in `myou260312-eng/VANE-SPACE-SLA`:

- `main` — protected, stable branch for release-ready code
- `feature/<short-name>` — feature work and major changes
- `fix/<short-name>` — bug fixes and clean-up work
- `hotfix/<issue>` — urgent production issue recovery
- `docs/<topic>` — documentation or process updates

Example branch names:

```bash
git checkout -b feature/rag-grounding-audit
git checkout -b fix/telemetry-seed-validation
git checkout -b hotfix/ci-coverage-threshold
```

Always verify the repo is clean before starting work:

```bash
git status
git pull --ff-only origin main
```

Before creating a PR, run the project checks used in CI:

```bash
pytest --cov=. --cov-report=term
```

The CI workflow in `.github/workflows/ci.yml` runs pytest with coverage and will fail if the threshold is not met.

---

## Everyday Git cheat sheet

### 1) Start a feature branch

```bash
git switch main
git pull --ff-only origin main
git switch -c feature/my-change
```

### 2) Check status and inspect changes

```bash
git status
git diff
git diff --staged
```

### 3) Stage and commit changes

```bash
git add .
git commit -m "Add telemetry validation for strict grounding"
```

### 4) Push the branch

```bash
git push -u origin feature/my-change
```

### 5) Open a pull request

```bash
gh pr create --base main --head feature/my-change --fill
```

---

## `git stash`

Use `git stash` when you need to pause work and switch contexts without committing.

### Typical usage

```bash
git stash push -m "WIP: telemetry validation"
git switch main
git pull --ff-only origin main
git switch feature/another-task
git stash pop
```

### Useful stash commands

```bash
git stash list
git stash show stash@{0}
git stash apply stash@{0}
git stash pop stash@{0}
git stash drop stash@{0}
```

Use case in this repo:
- working on a fast fix while the CI branch is checked
- switching to a docs branch
- temporarily saving unfinished RAG or telemetry work

---

## `git cherry-pick`

Use `git cherry-pick` to copy a specific commit from one branch to another without merging the whole branch.

### Example

```bash
git log --oneline
git checkout main
git cherry-pick a1b2c3d
```

If you only want to bring one clean fix from `hotfix/ci` into `main`:

```bash
git switch main
git cherry-pick <commit-sha>
```

If conflicts appear:

```bash
git status
# resolve conflicts in files
git add <resolved-file>
git cherry-pick --continue
```

Abort the cherry-pick:

```bash
git cherry-pick --abort
```

Use case in this repo:
- a fix from a `hotfix/*` branch should be applied to `main`
- a test addition from a feature branch should be replayed elsewhere

---

## `git revert`

Use `git revert` when you need to undo a committed change safely and preserve history.

### Example

```bash
git log --oneline
git revert a1b2c3d
```

This creates a new commit that reverses the selected commit. It is safe for shared branches.

### Revert multiple commits

```bash
git revert HEAD~3..HEAD
```

### Revert a merge commit

```bash
git revert -m 1 <merge-commit-sha>
```

If conflicts occur:

```bash
git status
# resolve the conflict
git add <resolved-file>
git revert --continue
```

Abort:

```bash
git revert --abort
```

Use case in this repo:
- you pushed a bad commit to `main`
- a telemetry or prompt change needs to be reversed without rewriting history

---

## `git reset`

Use `git reset` to move the current branch pointer backward. This changes local history and should be used carefully.

### Soft reset

Keep the changes, but move them back to the index:

```bash
git reset --soft HEAD~1
```

### Mixed reset

Move back one commit and unstage the changes:

```bash
git reset HEAD~1
```

### Hard reset

Discard the commit and all changes:

```bash
git reset --hard HEAD~1
```

### Reset to a specific commit

```bash
git reset --hard a1b2c3d
```

### Unstage a file without losing its content

```bash
git reset HEAD config.py
```

Use case in this repo:
- undo a mistaken commit before push
- clean up an unfinished patch on a feature branch

Warning:
- `git reset --hard` is destructive, especially on shared branches.
- Prefer `git revert` if the commit has already been pushed.

---

## Recommended team workflow for this repo

1. Start from `main`.
2. Create a feature branch such as `feature/telemetry-hardening`.
3. Make small, meaningful changes only.
4. Run the local validation suite:

```bash
pytest --cov=. --cov-report=term
```

5. Commit with a clear message:

```bash
git commit -m "Add strict grounding coverage for telemetry gates"
```

6. Push the branch and open a PR.
7. Ensure CI passes before merge.
8. Use `git revert` for rollback and `git stash` for temporary interruptions.
9. Delete the feature branch after merge.

```bash
git switch main
git pull --ff-only origin main
git branch -d feature/telemetry-hardening
```

---

## Quick command reference

```bash
git status
git switch main
git switch -c feature/my-change
git add .
git commit -m "Describe the change"
git push -u origin feature/my-change
git stash push -m "WIP: save progress"
git stash pop
git cherry-pick <commit-sha>
git revert <commit-sha>
git reset --soft HEAD~1
git reset --hard HEAD~1
```
This workflow is intentionally lightweight for a Python-based test harness repo where rapid iteration and CI validation are important.


## License
MIT — see [LICENSE](license.md) file.

Contact / Support 
- For maintenance, open an issue in this repository: https://github.com/myou260312-eng/VANE-SPACE-SLA/issues

---

This repository was prepared as a sanitized, testable demonstration for VANE-SPACE-SLA v2.0. If you want help connecting real vector stores or an LLM provider, open an issue and I can propose an integration plan and implementation steps.
