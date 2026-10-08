# Upstream issue note

This repository exists because the local Screenpipe desktop path for Pi can regenerate a `custom -> openai-completions` provider shape during `Pi config merged`, which breaks `gpt-6-luna` tool use with the well-known `reasoning_effort` error on Chat Completions.

## Observed behavior

- standalone local Pi path can be made to work
- Screenpipe desktop path rewrites the effective provider shape on launch
- the embedded path then fails on:
  - `Function tools with reasoning_effort are not supported for gpt-6-luna in /v1/chat/completions`

## What this repo is

- not a Screenpipe fork
- not an app-bundle patch
- not a daemon

It is a small external overlay that:

1. checks the writable local Pi runtime on launch
2. silently reapplies the narrow runtime patch if drift is detected
3. verifies the repaired runtime cheaply
4. launches Screenpipe

Repo:

https://github.com/le-dawg/screenpipe-pi-healer

## Why mention it upstream

Even if Screenpipe does not want to adopt this exact overlay, the issue is useful because it documents:

1. the failing route
2. the runtime layer that actually controls behavior
3. a concrete user-space mitigation others can inspect
