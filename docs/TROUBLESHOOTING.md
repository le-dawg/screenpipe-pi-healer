# Troubleshooting

## `anchor_miss`

Meaning:

- the target runtime file changed enough that the healer could not safely patch it

What to do:

1. run `tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --check`
2. inspect the target file mentioned in the output
3. compare it against the manifest anchor
4. update the manifest and tests before repairing

## `target_missing`

Meaning:

- Screenpipe’s local Pi runtime is missing or moved

What to do:

1. launch Screenpipe once normally so it can reinstall or repopulate the runtime
2. run `--check` again

## `verify_failed`

Meaning:

- the patch landed, but the cheap verifier could not prove the runtime resolved `custom/gpt-6-luna` as expected

What to do:

1. inspect the log
2. run `tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --repair`
3. if still failing, inspect the local runtime with the repo tests or adapt the verifier

## Where to look

- Healer log:
  - `~/Library/Logs/screenpipe-pi-healer.log`
- Patch manifest:
  - `tools/screenpipe-pi-healer/screenpipe-pi-heal-manifest.json`
- Tests:
  - `tests/`
