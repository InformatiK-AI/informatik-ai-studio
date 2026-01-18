"""
Test skill scripts.

Validates:
- All referenced scripts in `scripts/` actually exist
- Scripts have valid Python syntax
"""

import sys
import ast
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from test_utils import (
    get_all_skill_dirs,
    parse_skill_frontmatter,
    check_file_exists,
    extract_scripts_from_skill,
    TestResult
)


def test_scripts_exist() -> TestResult:
    """Test that all referenced scripts exist."""
    result = TestResult("Scripts Exist")

    for skill_dir in get_all_skill_dirs():
        skill_name = skill_dir.name
        frontmatter, content = parse_skill_frontmatter(skill_dir)

        scripts = extract_scripts_from_skill(content)

        for script in scripts:
            script_path = skill_dir / "scripts" / script
            if not check_file_exists(script_path):
                result.add_fail(f"{skill_name}: Missing script '{script}'")
            else:
                result.add_pass()

    return result


def test_scripts_syntax() -> TestResult:
    """Test that Python scripts have valid syntax."""
    result = TestResult("Scripts Syntax")

    for skill_dir in get_all_skill_dirs():
        skill_name = skill_dir.name
        scripts_dir = skill_dir / "scripts"

        if not scripts_dir.exists():
            continue

        for script_path in scripts_dir.glob("*.py"):
            try:
                with open(script_path, "r", encoding="utf-8") as f:
                    source = f.read()
                ast.parse(source)
                result.add_pass()
            except SyntaxError as e:
                result.add_fail(f"{skill_name}/{script_path.name}: Syntax error at line {e.lineno}")
            except Exception as e:
                result.add_fail(f"{skill_name}/{script_path.name}: Parse error: {e}")

    return result


def test_scripts_directory() -> TestResult:
    """Test that skills with scripts have a scripts directory."""
    result = TestResult("Scripts Directory")

    for skill_dir in get_all_skill_dirs():
        skill_name = skill_dir.name
        frontmatter, content = parse_skill_frontmatter(skill_dir)

        scripts = extract_scripts_from_skill(content)
        scripts_dir = skill_dir / "scripts"

        if scripts and not scripts_dir.exists():
            result.add_fail(f"{skill_name}: Scripts mentioned but no 'scripts/' directory")
        elif scripts:
            result.add_pass()

    return result


def main():
    """Run all script tests."""
    print("=" * 60)
    print("SKILL SCRIPTS TESTS")
    print("=" * 60)

    tests = [
        test_scripts_exist,
        test_scripts_syntax,
        test_scripts_directory,
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
