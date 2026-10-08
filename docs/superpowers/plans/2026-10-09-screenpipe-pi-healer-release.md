# Screenpipe Pi Healer Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a standalone public repository for the Screenpipe Pi self-healer, with strong user/developer docs, installable tooling, verification tests, and an upstream GitHub issue/discussion mention path.

**Architecture:** Package the already-proven local runtime repair as an external overlay project: a launch-time shell wrapper, a manifest-driven patch applier, a cheap verifier, and install helpers for macOS. Keep the repair logic outside `~/.screenpipe` so it survives runtime replacement. Release it as a public GitHub repo with high-signal docs and contributor affordances.

**Tech Stack:** Shell, Python 3, JSON manifest, pytest via `uv`, GitHub CLI, macOS launcher generation via `osacompile`, Markdown docs, GitHub Actions.

## Global Constraints

- Repo path: `/Users/thedawgctor/Desktop/dawgctor-personal-tools/screenpipe-pi-healer`
- No whitespace in repo path or internal directories.
- Do not copy private backups, secrets, or `~/.screenpipe` runtime trees into the repo.
- Event-driven only; no daemons, no timers, no file watchers.
- Auto-repair silently on launch, log locally, never block Screenpipe startup.
- The repo must be publishable as `le-dawg/screenpipe-pi-healer` and be public.

---

### Task 1: Build the healer package

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `CONTRIBUTING.md`
- Create: `CHANGELOG.md`
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `tools/screenpipe-pi-healer/screenpipe-pi-heal.sh`
- Create: `tools/screenpipe-pi-healer/screenpipe-pi-heal-apply.py`
- Create: `tools/screenpipe-pi-healer/screenpipe-pi-heal-verify.py`
- Create: `tools/screenpipe-pi-healer/screenpipe-pi-heal-install.sh`
- Create: `tools/screenpipe-pi-healer/screenpipe-pi-heal-manifest.json`
- Create: `docs/ARCHITECTURE.md`
- Create: `docs/COMPATIBILITY.md`
- Create: `docs/TROUBLESHOOTING.md`

### Task 2: Add verification and contributor breadcrumbs

**Files:**
- Create: `tests/test_manifest.py`
- Create: `tests/test_patch_apply.py`
- Create: `tests/fixtures/provider-composer.before.js`
- Create: `tests/fixtures/provider-composer.after.js`
- Create: `.github/workflows/ci.yml`
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`

### Task 3: Publish and announce

**Files:**
- Modify: `README.md`
- Modify: `docs/COMPATIBILITY.md`

**Release actions:**
- Create public repo under `le-dawg`
- Push default branch
- Enable issues and discussions
- Add good GitHub topics
- Comment on a relevant official `mediar-ai/screenpipe` issue or open one if no suitable issue exists
