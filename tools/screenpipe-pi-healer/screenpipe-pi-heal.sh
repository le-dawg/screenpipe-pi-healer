#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MANIFEST="$ROOT_DIR/screenpipe-pi-heal-manifest.json"
APPLY="$ROOT_DIR/screenpipe_pi_heal_apply.py"
VERIFY="$ROOT_DIR/screenpipe_pi_heal_verify.py"
LOG_FILE="$(python3 - <<'PY' "$MANIFEST"
import json, pathlib, sys
print(json.loads(pathlib.Path(sys.argv[1]).read_text())["heal_log"])
PY
)"

log_event() {
  local status="$1"
  local detail="${2:-}"
  python3 - <<'PY' "$LOG_FILE" "$status" "$detail"
import datetime as dt, json, pathlib, sys
path = pathlib.Path(sys.argv[1]).expanduser()
path.parent.mkdir(parents=True, exist_ok=True)
entry = {
    "ts": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z"),
    "status": sys.argv[2],
    "detail": sys.argv[3],
}
with path.open("a", encoding="utf-8") as fh:
    fh.write(json.dumps(entry) + "\n")
PY
}

apply_status_json() {
  python3 "$APPLY" --manifest "$MANIFEST" "$@"
}

do_check() {
  local out
  out="$(apply_status_json --check-only)"
  echo "$out"
  local status
  status="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["status"])' "$out")"
  if [[ "$status" == "healthy" ]]; then
    python3 "$VERIFY" --manifest "$MANIFEST"
  fi
}

do_launch() {
  local out
  out="$(apply_status_json)"
  local status detail
  status="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["status"])' "$out")"
  detail="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1]).get("detail",""))' "$out")"

  case "$status" in
    healthy)
      log_event "noop_healthy" "$detail"
      ;;
    repaired)
      if python3 "$VERIFY" --manifest "$MANIFEST" >/dev/null; then
        log_event "repaired_ok" "$detail"
      else
        log_event "repair_failed" "post-repair verification failed"
      fi
      ;;
    repairable)
      log_event "repairable_unexpected" "$detail"
      ;;
    anchor_miss|target_missing|repair_failed)
      log_event "$status" "$detail"
      ;;
    *)
      log_event "unknown_status" "$status"
      ;;
  esac

  open -a screenpipe
}

do_install_launcher() {
  mkdir -p "$HOME/.local/bin" "$HOME/Applications"
  cat > "$HOME/.local/bin/screenpipe-pi-heal-launch" <<EOF
#!/usr/bin/env bash
exec "$ROOT_DIR/screenpipe-pi-heal.sh" --launch-screenpipe
EOF
  chmod +x "$HOME/.local/bin/screenpipe-pi-heal-launch"

  osacompile -o "$HOME/Applications/Screenpipe Pi Healed.app" \
    -e "do shell script quoted form of \"$HOME/.local/bin/screenpipe-pi-heal-launch\" & \" >/dev/null 2>&1 &\""
  echo "installed_launcher=$HOME/Applications/Screenpipe Pi Healed.app"
}

case "${1:-}" in
  --launch-screenpipe)
    do_launch
    ;;
  --check)
    do_check
    ;;
  --repair)
    python3 "$APPLY" --manifest "$MANIFEST"
    python3 "$VERIFY" --manifest "$MANIFEST"
    ;;
  --install-launcher)
    do_install_launcher
    ;;
  *)
    cat <<'EOF'
Usage:
  screenpipe-pi-heal.sh --launch-screenpipe
  screenpipe-pi-heal.sh --check
  screenpipe-pi-heal.sh --repair
  screenpipe-pi-heal.sh --install-launcher
EOF
    exit 2
    ;;
esac
