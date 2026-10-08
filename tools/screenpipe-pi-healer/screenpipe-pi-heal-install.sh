#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
chmod +x "$ROOT_DIR"/screenpipe-pi-heal.sh "$ROOT_DIR"/screenpipe_pi_heal_apply.py "$ROOT_DIR"/screenpipe_pi_heal_verify.py
"$ROOT_DIR/screenpipe-pi-heal.sh" --install-launcher
echo "run_check=$ROOT_DIR/screenpipe-pi-heal.sh --check"
