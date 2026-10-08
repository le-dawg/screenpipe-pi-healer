#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import pathlib
import tempfile
from dataclasses import dataclass


@dataclass
class ApplyResult:
    status: str
    changed: bool
    target: str
    detail: str = ""


def load_manifest(path: pathlib.Path) -> dict:
    return json.loads(path.read_text())


def file_contains_all(text: str, fragments: list[str]) -> bool:
    return all(fragment in text for fragment in fragments)


def apply_manifest_to_text(text: str, manifest: dict, check_only: bool = False) -> ApplyResult:
    patch = manifest["patch"]
    target = manifest["target_file"]
    expected = patch["expected_fragment"]

    if file_contains_all(text, expected):
        return ApplyResult(status="healthy", changed=False, target=target)

    anchor = patch["anchor_line"]
    api_from = patch["replace_api_line"]["from"]
    api_to = patch["replace_api_line"]["to"]
    reasoning_from = patch["replace_reasoning_line"]["from"]
    reasoning_to = patch["replace_reasoning_line"]["to"]
    inserts = patch["insert_after_anchor"]

    if anchor not in text:
        return ApplyResult(status="anchor_miss", changed=False, target=target, detail="anchor line missing")
    if api_from not in text:
        return ApplyResult(status="anchor_miss", changed=False, target=target, detail="api replacement anchor missing")
    if reasoning_from not in text:
        return ApplyResult(status="anchor_miss", changed=False, target=target, detail="reasoning replacement anchor missing")

    if check_only:
        return ApplyResult(status="repairable", changed=False, target=target)

    new_text = text.replace(anchor, "\n".join([anchor, *inserts]), 1)
    new_text = new_text.replace(api_from, api_to, 1)
    new_text = new_text.replace(reasoning_from, reasoning_to, 1)

    if not file_contains_all(new_text, expected):
        return ApplyResult(status="repair_failed", changed=False, target=target, detail="patched content did not contain expected fragment")

    return ApplyResult(status="repaired", changed=True, target=target)


def atomic_write(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=path.parent, encoding="utf-8") as handle:
        handle.write(content)
        temp_name = handle.name
    pathlib.Path(temp_name).replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(pathlib.Path(__file__).with_name("screenpipe-pi-heal-manifest.json")))
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    manifest_path = pathlib.Path(args.manifest)
    manifest = load_manifest(manifest_path)
    target = pathlib.Path(manifest["target_file"]).expanduser()

    if not target.exists():
      print(json.dumps({"status": "target_missing", "changed": False, "target": str(target)}))
      return 20

    original = target.read_text()
    result = apply_manifest_to_text(original, manifest, check_only=args.check_only)

    if result.status == "repaired":
        patched = original.replace(
            manifest["patch"]["anchor_line"],
            "\n".join([manifest["patch"]["anchor_line"], *manifest["patch"]["insert_after_anchor"]]),
            1,
        ).replace(
            manifest["patch"]["replace_api_line"]["from"],
            manifest["patch"]["replace_api_line"]["to"],
            1,
        ).replace(
            manifest["patch"]["replace_reasoning_line"]["from"],
            manifest["patch"]["replace_reasoning_line"]["to"],
            1,
        )
        atomic_write(target, patched)

    exit_map = {
        "healthy": 0,
        "repairable": 10,
        "repaired": 11,
        "anchor_miss": 21,
        "repair_failed": 22,
        "target_missing": 20,
    }
    print(json.dumps(result.__dict__))
    return exit_map[result.status]


if __name__ == "__main__":
    raise SystemExit(main())
