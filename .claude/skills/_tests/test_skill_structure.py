"""
Test skill structure and frontmatter.

Validates:
- SKILL.md exists in each skill directory
- Frontmatter has required fields (name, description)
- Required sections exist in content
"""

import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from test_utils import (
    get_all_skill_dirs,
    parse_skill_frontmatter,
    check_file_exists,
    TestResult
)


def test_skill_structure() -> TestResult:
    """Test that all skills have correct structure."""
    result = TestResult("Skill Structure")

    skill_dirs = get_all_skill_dirs()

    for skill_dir in skill_dirs:
        skill_name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"

        # Check SKILL.md exists
        if not check_file_exists(skill_md):
            result.add_fail(f"{skill_name}: Missing SKILL.md")
            continue

        result.add_pass()

        # Parse frontmatter
        frontmatter, content = parse_skill_frontmatter(skill_dir)

        # Check required frontmatter fields
        if "name" not in frontmatter:
            result.add_fail(f"{skill_name}: Missing 'name' in frontmatter")
        else:
            result.add_pass()

        if "description" not in frontmatter:
            result.add_fail(f"{skill_name}: Missing 'description' in frontmatter")
        else:
            result.add_pass()

        # Check name matches directory
        if frontmatter.get("name") != skill_name:
            result.add_warning(f"{skill_name}: Frontmatter name '{frontmatter.get('name')}' doesn't match directory")

        # Check for common required sections
        required_sections = ["#"]  # At least one heading
        for section in required_sections:
            if section not in content:
                result.add_warning(f"{skill_name}: Missing expected content marker '{section}'")

    return result


def test_skill_has_content() -> TestResult:
    """Test that skills have meaningful content."""
    result = TestResult("Skill Content")

    MIN_CONTENT_LENGTH = 100  # Minimum characters

    for skill_dir in get_all_skill_dirs():
        skill_name = skill_dir.name
        frontmatter, content = parse_skill_frontmatter(skill_dir)

        if len(content.strip()) < MIN_CONTENT_LENGTH:
            result.add_fail(f"{skill_name}: Content too short ({len(content.strip())} chars)")
        else:
            result.add_pass()

    return result


def main():
    """Run all structure tests."""
    print("=" * 60)
    print("SKILL STRUCTURE TESTS")
    print("=" * 60)

    tests = [
        test_skill_structure,
        test_skill_has_content,
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
