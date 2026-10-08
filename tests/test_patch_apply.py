from pathlib import Path

from screenpipe_pi_heal_apply import apply_manifest_to_text, load_manifest


def test_apply_repairs_fixture():
    manifest = load_manifest(Path("tools/screenpipe-pi-healer/screenpipe-pi-heal-manifest.json"))
    before = Path("tests/fixtures/provider-composer.before.js").read_text()
    result = apply_manifest_to_text(before, manifest, check_only=False)
    assert result.status == "repaired"
    assert result.changed is True


def test_apply_reports_healthy_when_fragment_present():
    manifest = load_manifest(Path("tools/screenpipe-pi-healer/screenpipe-pi-heal-manifest.json"))
    after = Path("tests/fixtures/provider-composer.after.js").read_text()
    result = apply_manifest_to_text(after, manifest, check_only=False)
    assert result.status == "healthy"
    assert result.changed is False


def test_apply_reports_repairable_in_check_mode():
    manifest = load_manifest(Path("tools/screenpipe-pi-healer/screenpipe-pi-heal-manifest.json"))
    before = Path("tests/fixtures/provider-composer.before.js").read_text()
    result = apply_manifest_to_text(before, manifest, check_only=True)
    assert result.status == "repairable"


def test_apply_reports_anchor_miss():
    manifest = load_manifest(Path("tools/screenpipe-pi-healer/screenpipe-pi-heal-manifest.json"))
    result = apply_manifest_to_text("totally unrelated text", manifest, check_only=False)
    assert result.status == "anchor_miss"
