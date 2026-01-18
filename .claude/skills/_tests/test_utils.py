"""
Utility functions for skill testing.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Base paths
SKILLS_DIR = Path(__file__).parent.parent
SHARED_DIR = SKILLS_DIR / "_shared"
MANIFEST_PATH = SKILLS_DIR / "MANIFEST.json"
MIXINS_PATH = SHARED_DIR / "MIXINS.json"


def get_all_skill_dirs() -> List[Path]:
    """Get all skill directories (excluding _shared, _tests)."""
    return [
        d for d in SKILLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith("_")
    ]


def get_skill_names() -> List[str]:
    """Get all skill names."""
    return [d.name for d in get_all_skill_dirs()]


def load_manifest() -> Dict:
    """Load the main MANIFEST.json."""
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_mixins_manifest() -> Dict:
    """Load the MIXINS.json."""
    with open(MIXINS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_skill_frontmatter(skill_path: Path) -> Tuple[Dict, str]:
    """
    Parse SKILL.md frontmatter and content.
    Returns (frontmatter_dict, content_string).
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return {}, ""

    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse YAML frontmatter
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            import yaml
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
            except:
                frontmatter = {}
            body = parts[2]

    return frontmatter, body


def check_file_exists(path: Path) -> bool:
    """Check if a file exists."""
    return path.exists() and path.is_file()


def check_dir_exists(path: Path) -> bool:
    """Check if a directory exists."""
    return path.exists() and path.is_dir()


def extract_references_from_skill(content: str) -> List[str]:
    """Extract reference file paths from skill content."""
    # Match patterns like `references/filename.md`
    pattern = r"`references/([^`]+\.md)`"
    matches = re.findall(pattern, content)
    return list(set(matches))


def extract_scripts_from_skill(content: str) -> List[str]:
    """Extract script file paths from skill content."""
    # Match patterns like `scripts/filename.py`
    pattern = r"scripts/([^`\s]+\.py)"
    matches = re.findall(pattern, content)
    return list(set(matches))


class TestResult:
    """Container for test results."""

    def __init__(self, name: str):
        self.name = name
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.errors: List[str] = []
        self.warnings_list: List[str] = []

    def add_pass(self):
        self.passed += 1

    def add_fail(self, message: str):
        self.failed += 1
        self.errors.append(message)

    def add_warning(self, message: str):
        self.warnings += 1
        self.warnings_list.append(message)

    def is_success(self) -> bool:
        return self.failed == 0

    def summary(self) -> str:
        status = "PASS" if self.is_success() else "FAIL"
        return f"[{status}] {self.name}: {self.passed} passed, {self.failed} failed, {self.warnings} warnings"

    def details(self) -> str:
        lines = [self.summary()]
        for error in self.errors:
            lines.append(f"  ERROR: {error}")
        for warning in self.warnings_list:
            lines.append(f"  WARNING: {warning}")
        return "\n".join(lines)
