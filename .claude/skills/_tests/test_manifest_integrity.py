"""
Test manifest integrity.

Validates:
- MANIFEST.json matches actual skill directories
- All skills in manifest exist
- No orphan skills (directories without manifest entry)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from test_utils import (
    get_skill_names,
    load_manifest,
    TestResult
)


def test_manifest_skills_exist() -> TestResult:
    """Test that all skills in manifest exist as directories."""
    result = TestResult("Manifest Skills Exist")

    try:
        manifest = load_manifest()
    except Exception as e:
        result.add_fail(f"Cannot load MANIFEST.json: {e}")
        return result

    actual_skills = set(get_skill_names())
    manifest_skills = set(manifest.get("skills", {}).keys())

    # Check manifest skills exist
    for skill in manifest_skills:
        if skill not in actual_skills:
            result.add_fail(f"Manifest lists '{skill}' but directory doesn't exist")
        else:
            result.add_pass()

    return result


def test_no_orphan_skills() -> TestResult:
    """Test that all skill directories are in manifest."""
    result = TestResult("No Orphan Skills")

    try:
        manifest = load_manifest()
    except Exception as e:
        result.add_fail(f"Cannot load MANIFEST.json: {e}")
        return result

    actual_skills = set(get_skill_names())
    manifest_skills = set(manifest.get("skills", {}).keys())

    # Check for orphan skills
    orphans = actual_skills - manifest_skills
    for orphan in orphans:
        result.add_warning(f"Skill directory '{orphan}' not in MANIFEST.json")

    if not orphans:
        result.add_pass()

    return result


def test_category_skills_exist() -> TestResult:
    """Test that all skills listed in categories exist in main skills dict."""
    result = TestResult("Category Skills Exist")

    try:
        manifest = load_manifest()
    except Exception as e:
        result.add_fail(f"Cannot load MANIFEST.json: {e}")
        return result

    all_skills = set(manifest.get("skills", {}).keys())

    for category, data in manifest.get("categories", {}).items():
        for skill in data.get("skills", []):
            if skill not in all_skills:
                result.add_fail(f"Category '{category}' lists '{skill}' but not in skills dict")
            else:
                result.add_pass()

    return result


def test_manifest_version() -> TestResult:
    """Test that manifest has valid version."""
    result = TestResult("Manifest Version")

    try:
        manifest = load_manifest()
    except Exception as e:
        result.add_fail(f"Cannot load MANIFEST.json: {e}")
        return result

    if "version" not in manifest:
        result.add_fail("MANIFEST.json missing 'version' field")
    else:
        version = manifest["version"]
        # Simple semver check
        import re
        if not re.match(r"^\d+\.\d+\.\d+$", version):
            result.add_warning(f"Version '{version}' doesn't follow semver")
        else:
            result.add_pass()

    if "last_updated" not in manifest:
        result.add_warning("MANIFEST.json missing 'last_updated' field")
    else:
        result.add_pass()

    return result


def main():
    """Run all manifest integrity tests."""
    print("=" * 60)
    print("MANIFEST INTEGRITY TESTS")
    print("=" * 60)

    tests = [
        test_manifest_skills_exist,
        test_no_orphan_skills,
        test_category_skills_exist,
        test_manifest_version,
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
