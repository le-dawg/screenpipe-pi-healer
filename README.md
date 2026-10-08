# Screenpipe Pi Healer

Silent, launch-time self-healing for a very specific but nasty local compatibility break:

- **Screenpipe desktop**
- **local writable Pi runtime**
- **`custom/gpt-6-luna`**
- **tool use + reasoning**
- **Apple Silicon efficiency first**

No Screenpipe fork. No daemon. No polling. No app-bundle surgery.

## Why this exists

On this machine, `gpt-6-luna` could be made to work through the local Pi runtime, but the Screenpipe desktop path kept regenerating a `custom -> openai-completions` shape and fell back into:

- `Function tools with reasoning_effort are not supported for gpt-6-luna in /v1/chat/completions`

The working fix turned out to be a **narrow runtime coercion** in the writable local Pi install. This project packages that fix as an external overlay that can **detect drift on launch and silently repair it**.

## What it does

1. Runs only when you launch Screenpipe through the healer
2. Checks whether the local Pi runtime still contains the required patch
3. Reapplies the patch if drift is detected
4. Verifies the repaired runtime cheaply
5. Launches Screenpipe whether healthy, repaired, or unrecoverable
6. Writes breadcrumbs to a local log so humans can see what happened later

## Why contributors should care

This repo is deliberately tiny, auditable, and hostile to “magic”.

Good things live here:

- narrow compatibility overlays
- patch drift detection
- cheap runtime verification
- reproducible local recovery
- excellent user/developer breadcrumbs

Bad things do not:

- background babysitters
- endless polling
- undocumented binary hacks
- secrets in artifacts
- “works on my machine” handwaving

## Quick Start

### 1. Clone

```bash
git clone https://github.com/le-dawg/screenpipe-pi-healer.git
cd screenpipe-pi-healer
```

### 2. Install the launcher

```bash
tools/screenpipe-pi-healer/screenpipe-pi-heal-install.sh
```

This creates:

- `~/.local/bin/screenpipe-pi-heal-launch`
- `~/Applications/Screenpipe Pi Healed.app`

### 3. Check health

```bash
tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --check
```

### 4. Launch through the healer

```bash
tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --launch-screenpipe
```

Or use:

- `~/Applications/Screenpipe Pi Healed.app`

## Commands

```bash
tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --launch-screenpipe
tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --check
tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --repair
tools/screenpipe-pi-healer/screenpipe-pi-heal.sh --install-launcher
```

## How it works

- The patch target lives in the writable local Pi runtime under `~/.screenpipe/pi-agent`
- The healer itself lives outside that volatile tree
- A manifest defines:
  - target file
  - patch anchor
  - expected healed fragment
  - cheap verification expectations

Healthy launch:

1. detect healthy runtime
2. log `noop_healthy`
3. open Screenpipe

Drifted launch:

1. detect drift
2. apply narrow patch
3. verify repaired runtime
4. log `repaired_ok`
5. open Screenpipe

Unsafe launch:

1. detect drift
2. fail to match anchor safely
3. log `anchor_miss` or `target_missing`
4. open Screenpipe unhealed

## Breadcrumbs

This project takes “future humans will go looking” seriously.

Breadcrumbs exist in:

- code comments
- manifest fields
- verifier output
- launch-time log entries
- compatibility docs
- troubleshooting docs
- tests with fixture diffs

Primary log:

- `~/Library/Logs/screenpipe-pi-healer.log`

## Compatibility

See [docs/COMPATIBILITY.md](docs/COMPATIBILITY.md).

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Troubleshooting

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
