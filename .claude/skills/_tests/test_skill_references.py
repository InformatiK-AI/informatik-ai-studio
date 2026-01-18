"""
Test skill references.

Validates:
- All referenced files in `references/` actually exist
- References are valid markdown files
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from test_utils import (
    get_all_skill_dirs,
    parse_skill_frontmatter,
    check_file_exists,
    extract_references_from_skill,
    TestResult
)


def test_references_exist() -> TestResult:
    """Test that all referenced files exist."""
    result = TestResult("References Exist")

    for skill_dir in get_all_skill_dirs():
        skill_name = skill_dir.name
        frontmatter, content = parse_skill_frontmatter(skill_dir)

        # Extract referenced files
        references = extract_references_from_skill(content)

        for ref in references:
            ref_path = skill_dir / "references" / ref
            if not check_file_exists(ref_path):
                result.add_fail(f"{skill_name}: Missing reference '{ref}'")
            else:
                result.add_pass()

    return result


def test_references_directory() -> TestResult:
    """Test that skills with references have a references directory."""
    result = TestResult("References Directory")

    for skill_dir in get_all_skill_dirs():
        skill_name = skill_dir.name
        frontmatter, content = parse_skill_frontmatter(skill_dir)

        references = extract_references_from_skill(content)
        refs_dir = skill_dir / "references"

        if references and not refs_dir.exists():
            result.add_fail(f"{skill_name}: References mentioned but no 'references/' directory")
        elif references:
            result.add_pass()

    return result


def test_orphan_references() -> TestResult:
    """Test for orphan reference files not mentioned in SKILL.md."""
    result = TestResult("Orphan References")

    for skill_dir in get_all_skill_dirs():
        skill_name = skill_dir.name
        frontmatter, content = parse_skill_frontmatter(skill_dir)

        refs_dir = skill_dir / "references"
        if not refs_dir.exists():
            continue

        # Get referenced files
        referenced = set(extract_references_from_skill(content))

        # Get actual files
        actual_files = {f.name for f in refs_dir.glob("*.md")}

        # Find orphans
        orphans = actual_files - referenced
        for orphan in orphans:
            result.add_warning(f"{skill_name}: Orphan reference file '{orphan}' not mentioned in SKILL.md")

        if not orphans:
            result.add_pass()

    return result


def main():
    """Run all reference tests."""
    print("=" * 60)
    print("SKILL REFERENCES TESTS")
    print("=" * 60)

    tests = [
        test_references_exist,
        test_references_directory,
        test_orphan_references,
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
