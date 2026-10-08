#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import tempfile


def load_manifest(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())


def verify_fragment(target: pathlib.Path, expected_fragments: list[str]) -> tuple[bool, str]:
    if not target.exists():
        return False, "target_missing"
    text = target.read_text(errors="replace")
    missing = [frag for frag in expected_fragments if frag not in text]
    if missing:
        return False, f"missing_fragment:{missing[0]}"
    return True, "fragment_ok"


def verify_runtime(manifest: dict) -> tuple[bool, str]:
    verification = manifest["verification"]
    bun_path = pathlib.Path(verification["bun_path"])
    if not bun_path.exists():
        return False, "bun_missing"

    with tempfile.NamedTemporaryFile("w", suffix=".mjs", delete=False, encoding="utf-8") as handle:
        handle.write(
            f"""
import {{ ModelRuntime }} from "/Users/thedawgctor/.screenpipe/pi-agent/node_modules/@earendil-works/pi-coding-agent/dist/core/model-runtime.js";
const runtime = await ModelRuntime.create({{
  authPath: "{verification['auth_path']}",
  modelsPath: "{verification['models_path']}",
  allowModelNetwork: false,
  refreshOnCreate: false,
}});
const model = runtime.getModel("{verification['expected_provider']}", "{verification['expected_model']}");
console.log(JSON.stringify({{
  provider: model?.provider,
  model: model?.id,
  api: model?.api,
  reasoning: model?.reasoning
}}));
"""
        )
        temp_js = handle.name
    try:
        proc = subprocess.run(
            [str(bun_path), temp_js],
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            return False, f"runtime_probe_failed:{proc.stderr.strip() or proc.stdout.strip()}"
        payload = json.loads(proc.stdout.strip())
        if payload.get("provider") != verification["expected_provider"]:
            return False, "provider_mismatch"
        if payload.get("model") != verification["expected_model"]:
            return False, "model_mismatch"
        if payload.get("api") != verification["expected_api"]:
            return False, "api_mismatch"
        if payload.get("reasoning") is not verification["expected_reasoning"]:
            return False, "reasoning_mismatch"
        return True, "runtime_ok"
    finally:
        pathlib.Path(temp_js).unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(pathlib.Path(__file__).with_name("screenpipe-pi-heal-manifest.json")))
    args = parser.parse_args()

    manifest = load_manifest(pathlib.Path(args.manifest))
    target = pathlib.Path(manifest["target_file"]).expanduser()
    fragments = manifest["patch"]["expected_fragment"]

    ok, detail = verify_fragment(target, fragments)
    if not ok:
        print(json.dumps({"status": "verify_failed", "detail": detail, "target": str(target)}))
        return 30

    ok, runtime_detail = verify_runtime(manifest)
    if not ok:
        print(json.dumps({"status": "verify_failed", "detail": runtime_detail, "target": str(target)}))
        return 31

    print(json.dumps({"status": "verify_ok", "detail": runtime_detail, "target": str(target)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
