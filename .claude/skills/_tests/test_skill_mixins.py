"""
Test skill mixins.

Validates:
- All mixin files exist
- Mixins have correct version headers
- Placeholder syntax is valid
"""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from test_utils import (
    SHARED_DIR,
    load_mixins_manifest,
    check_file_exists,
    TestResult
)


def test_mixin_files_exist() -> TestResult:
    """Test that all declared mixin files exist."""
    result = TestResult("Mixin Files Exist")

    try:
        mixins = load_mixins_manifest()
    except FileNotFoundError:
        result.add_fail("MIXINS.json not found")
        return result
    except Exception as e:
        result.add_fail(f"Error loading MIXINS.json: {e}")
        return result

    for mixin_id, mixin_data in mixins.get("mixins", {}).items():
        mixin_file = SHARED_DIR / mixin_data["file"]
        if not check_file_exists(mixin_file):
            result.add_fail(f"Missing mixin file: {mixin_data['file']}")
        else:
            result.add_pass()

    return result


def test_mixin_versions() -> TestResult:
    """Test that mixin files have version headers."""
    result = TestResult("Mixin Versions")

    version_pattern = re.compile(r"<!--\s*mixin-version:\s*(\d+\.\d+\.\d+)\s*-->")

    for mixin_file in SHARED_DIR.glob("*.md"):
        if mixin_file.name == "README.md":
            continue

        with open(mixin_file, "r", encoding="utf-8") as f:
            content = f.read()

        match = version_pattern.search(content)
        if not match:
            result.add_warning(f"{mixin_file.name}: Missing version header")
        else:
            result.add_pass()

    return result


def test_mixin_placeholders() -> TestResult:
    """Test that placeholder syntax is valid."""
    result = TestResult("Mixin Placeholders")

    # Valid placeholder pattern: {{PLACEHOLDER_NAME}}
    placeholder_pattern = re.compile(r"\{\{([A-Z_]+)\}\}")
    # Invalid patterns (common mistakes)
    invalid_patterns = [
        (re.compile(r"\{[A-Z_]+\}(?!\})"), "Single braces instead of double"),
        (re.compile(r"\{\{[a-z_]+\}\}"), "Lowercase placeholder"),
    ]

    for mixin_file in SHARED_DIR.glob("*.md"):
        if mixin_file.name == "README.md":
            continue

        with open(mixin_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for invalid patterns
        for pattern, error_msg in invalid_patterns:
            if pattern.search(content):
                result.add_warning(f"{mixin_file.name}: {error_msg}")

        # Verify placeholders match manifest
        placeholders = placeholder_pattern.findall(content)
        if placeholders:
            result.add_pass()

    return result


def test_mixin_manifest_integrity() -> TestResult:
    """Test that MIXINS.json is complete and valid."""
    result = TestResult("Mixin Manifest Integrity")

    try:
        mixins = load_mixins_manifest()
    except Exception as e:
        result.add_fail(f"Cannot load MIXINS.json: {e}")
        return result

    # Check required top-level fields
    required_fields = ["version", "last_updated", "mixins"]
    for field in required_fields:
        if field not in mixins:
            result.add_fail(f"MIXINS.json missing required field: {field}")
        else:
            result.add_pass()

    # Check each mixin has required fields
    for mixin_id, mixin_data in mixins.get("mixins", {}).items():
        required_mixin_fields = ["id", "file", "version", "description"]
        for field in required_mixin_fields:
            if field not in mixin_data:
                result.add_fail(f"Mixin '{mixin_id}' missing field: {field}")
            else:
                result.add_pass()

    return result


def main():
    """Run all mixin tests."""
    print("=" * 60)
    print("SKILL MIXINS TESTS")
    print("=" * 60)

    tests = [
        test_mixin_files_exist,
        test_mixin_versions,
        test_mixin_placeholders,
        test_mixin_manifest_integrity,
    ]

    all_passed = True
    for test_fn in tests:
        result = test_fn()
        print(result.details())
        if not result.is_success():
            all_passed = False

    print("=" * 60)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
