# Architecture

## Design goals

1. survive replacement of `~/.screenpipe/pi-agent`
2. repair only on launch
3. keep Apple Silicon overhead tiny
4. never block Screenpipe startup
5. leave strong breadcrumbs for humans

## Core pieces

- `screenpipe-pi-heal.sh`
  Launch wrapper and operator entrypoint

- `screenpipe_pi_heal_apply.py`
  Manifest-driven patch applier

- `screenpipe_pi_heal_verify.py`
  Cheap verifier

- `screenpipe-pi-heal-manifest.json`
  Source of truth for target, anchor, and expected healed fragment

## Why external overlay instead of fork

Forking Screenpipe would turn a narrow machine-level compatibility shim into a permanent upstream merge tax. This project deliberately stays outside the host project and only patches the writable local runtime surface that already exists on the user’s machine.

## Failure model

The healer is allowed to fail safe, not fail closed.

That means:

1. if healthy, do nothing
2. if repairable, repair
3. if no longer safely repairable, log and launch anyway

## Runtime breadcrumbs

The local log is append-only JSONL so operators can inspect:

- whether launch was healthy
- whether drift was repaired
- whether the target file vanished
- whether the patch anchor changed
