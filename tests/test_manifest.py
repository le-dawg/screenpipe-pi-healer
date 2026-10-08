import json
from pathlib import Path


def test_manifest_has_expected_shape():
    manifest = json.loads(
        Path("tools/screenpipe-pi-healer/screenpipe-pi-heal-manifest.json").read_text()
    )
    assert manifest["target_file"].endswith("provider-composer.js")
    assert manifest["verification"]["expected_api"] == "openai-responses"
    assert manifest["verification"]["expected_model"] == "gpt-6-luna"
    assert len(manifest["patch"]["expected_fragment"]) >= 4
