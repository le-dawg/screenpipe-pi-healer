# Contributing

Thanks for considering a contribution.

## Philosophy

This project exists to keep one very specific local compatibility fix alive without forking Screenpipe. That means:

1. prefer narrow, auditable patches
2. fail safe when upstream drift becomes unrecognizable
3. keep launch-time overhead tiny
4. never hide risky mutations behind vague automation

## Development loop

```bash
uv run pytest -q
tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --check
```

## Scope guardrails

Good contributions:

1. better patch drift detection
2. more robust verification
3. lower-power launch flow
4. clearer docs, logs, and diagnostics

Bad contributions:

1. turning this into a general Screenpipe mod manager
2. adding daemons, timers, or background polling
3. mutating `/Applications/screenpipe.app`
4. storing secrets in repo artifacts or logs

## Reporting upstream drift

If upstream Screenpipe or Pi changes enough that the patch anchor no longer matches, please include:

1. the healer log line
2. the target file snippet around the failed anchor
3. the Screenpipe / Pi versions from `--check`
