#!/usr/bin/env python3
"""
Mixin Build Script for InformatiK-AI-meth Skills

This script processes skill SKILL.md files and:
1. Replaces {{include:mixin-name}} directives with actual mixin content
2. Replaces placeholders like {{ANALYZER_SCRIPT}} with skill-specific values
3. Checks for outdated mixin versions

Usage:
    python build_mixins.py                    # Process all skills with {{include:}} directives
    python build_mixins.py senior-frontend    # Process specific skill
    python build_mixins.py --check            # Check for outdated mixins
    python build_mixins.py --dry-run          # Show what would be changed
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class MixinBuilder:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.shared_dir = skills_dir / "_shared"
        self.mixins_json = self.shared_dir / "MIXINS.json"
        self.mixins_data = self._load_mixins_json()
        self.mixin_files: Dict[str, str] = {}
        self._load_mixin_files()

    def _load_mixins_json(self) -> dict:
        """Load the MIXINS.json configuration."""
        if not self.mixins_json.exists():
            print(f"Error: {self.mixins_json} not found")
            sys.exit(1)

        with open(self.mixins_json, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_mixin_files(self) -> None:
        """Load all mixin file contents into memory."""
        for mixin_id, mixin_info in self.mixins_data.get("mixins", {}).items():
            mixin_file = self.shared_dir / mixin_info["file"]
            if mixin_file.exists():
                with open(mixin_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Remove ALL header comments (mixin-version, mixin-id, last-updated)
                    content = re.sub(r'^<!--\s*[\w-]+:.*?-->\s*\n', '', content, flags=re.MULTILINE)
                    self.mixin_files[mixin_id] = content.strip()
            else:
                print(f"Warning: Mixin file not found: {mixin_file}")

    def get_skill_config(self, skill_name: str) -> Optional[dict]:
        """Get the mixin configuration for a specific skill."""
        return self.mixins_data.get("skill_mixin_mapping", {}).get(skill_name)

    def get_mixin_content(self, mixin_id: str, version: str = "1.0.0") -> str:
        """Get the content of a mixin with source marker."""
        content = self.mixin_files.get(mixin_id, "")
        if content:
            marker = f"<!-- mixin-source: {mixin_id} v{version} -->"
            return f"{marker}\n{content}"
        return ""

    def replace_placeholders(self, content: str, placeholders: Dict[str, str]) -> str:
        """Replace {{PLACEHOLDER}} with actual values."""
        for placeholder, value in placeholders.items():
            pattern = r'\{\{' + placeholder + r'\}\}'
            content = re.sub(pattern, value, content)
        return content

    def process_include_directives(self, content: str, skill_config: dict) -> Tuple[str, int]:
        """
        Process {{include:mixin-name}} directives.

        Returns: (new_content, count of replacements)
        """
        count = 0

        def replace_include(match):
            nonlocal count
            mixin_id = match.group(1)
            mixin_info = self.mixins_data.get("mixins", {}).get(mixin_id, {})
            version = mixin_info.get("version", "1.0.0")
            mixin_content = self.get_mixin_content(mixin_id, version)

            if mixin_content:
                # Apply placeholder replacements for this skill
                placeholders = skill_config.get("placeholder_values", {})
                mixin_content = self.replace_placeholders(mixin_content, placeholders)
                count += 1
                return mixin_content
            else:
                print(f"  Warning: Mixin '{mixin_id}' not found")
                return match.group(0)  # Keep original if not found

        pattern = r'\{\{include:([a-z0-9-]+)\}\}'
        new_content = re.sub(pattern, replace_include, content)
        return new_content, count

    def build_skill(self, skill_name: str, dry_run: bool = False) -> Tuple[bool, str]:
        """
        Build a single skill by processing {{include:}} directives.

        Note: This only processes {{include:}} directives, not existing mixin sections.
        Use --check to find outdated existing mixins.

        Returns: (changed: bool, message: str)
        """
        skill_dir = self.skills_dir / skill_name
        skill_file = skill_dir / "SKILL.md"

        if not skill_file.exists():
            return False, f"SKILL.md not found for {skill_name}"

        skill_config = self.get_skill_config(skill_name)
        if not skill_config:
            # Check if file has {{include:}} directives anyway
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            if '{{include:' not in content:
                return False, f"{skill_name}: No mixin configuration (skipped)"
            skill_config = {"placeholder_values": {}}

        with open(skill_file, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Only process {{include:}} directives
        new_content, include_count = self.process_include_directives(original_content, skill_config)

        if include_count == 0:
            return False, f"{skill_name}: No {{{{include:}}}} directives found"

        if dry_run:
            return True, f"{skill_name}: Would process {include_count} include(s) (dry-run)"

        # Write the updated content
        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, f"{skill_name}: Processed {include_count} include(s)"

    def build_all_skills(self, dry_run: bool = False) -> Dict[str, str]:
        """Build all skills that have mixin configurations or {{include:}} directives."""
        results = {}

        # Check all skill directories
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('_'):
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    # Check if it has {{include:}} directives
                    with open(skill_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if '{{include:' in content:
                        changed, message = self.build_skill(skill_dir.name, dry_run)
                        results[skill_dir.name] = message
                        print(f"  {message}")

        if not results:
            print("  No skills with {{include:}} directives found")

        return results

    def check_outdated(self) -> List[str]:
        """Check for skills with outdated mixin versions."""
        outdated = []

        # Check all skill directories
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir() and not skill_dir.name.startswith('_'):
                skill_file = skill_dir / "SKILL.md"
                if not skill_file.exists():
                    continue

                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Find all mixin-source markers in the skill
                markers = re.findall(r'<!-- mixin-source: ([a-z0-9-]+) v([\d.]+) -->', content)

                for mixin_id, skill_version in markers:
                    mixin_info = self.mixins_data.get("mixins", {}).get(mixin_id, {})
                    current_version = mixin_info.get("version", "1.0.0")

                    if skill_version != current_version:
                        outdated.append(f"{skill_dir.name}: {mixin_id} v{skill_version} -> v{current_version}")

        return outdated

    def create_skill_template(self, skill_name: str, mixins: List[str]) -> str:
        """
        Create a new skill template with include directives.

        Example usage:
            builder.create_skill_template("new-skill", ["tech-stack-fullstack", "best-practices-general"])
        """
        template = f"""---
name: {skill_name}
description: [Add description here]
version: 1.0.0
---

# {skill_name.replace('-', ' ').title()}

[Add overview here]

## Quick Start

[Add quick start guide here]

"""
        for mixin_id in mixins:
            template += f"{{{{include:{mixin_id}}}}}\n\n"

        return template


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Build skills with mixin processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build_mixins.py                    # Process all {{include:}} directives
  python build_mixins.py senior-frontend    # Process specific skill
  python build_mixins.py --check            # Check for outdated mixin versions
  python build_mixins.py --dry-run          # Preview changes

Note: This script only processes {{include:mixin-name}} directives.
Existing mixin-source sections are not auto-updated to prevent issues.
Use --check to find outdated mixins, then manually update if needed.
        """
    )
    parser.add_argument("skill", nargs="?", help="Specific skill to build (default: all)")
    parser.add_argument("--check", action="store_true", help="Check for outdated mixins")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed")
    parser.add_argument("--skills-dir", type=Path, help="Path to skills directory")
    parser.add_argument("--template", nargs="+", metavar=("SKILL_NAME", "MIXIN"),
                        help="Generate template: --template new-skill mixin1 mixin2")
    args = parser.parse_args()

    # Determine skills directory
    if args.skills_dir:
        skills_dir = args.skills_dir
    else:
        # Default: assume script is in _shared/ directory
        script_dir = Path(__file__).parent
        skills_dir = script_dir.parent

    print(f"Skills directory: {skills_dir}")

    builder = MixinBuilder(skills_dir)

    if args.template:
        skill_name = args.template[0]
        mixins = args.template[1:] if len(args.template) > 1 else []
        template = builder.create_skill_template(skill_name, mixins)
        print(f"\nTemplate for {skill_name}:\n")
        print(template)
        return

    if args.check:
        print("\nChecking for outdated mixins...")
        outdated = builder.check_outdated()
        if outdated:
            print("\nOutdated mixins found:")
            for item in outdated:
                print(f"  - {item}")
            print(f"\nTo update, manually edit the skill's SKILL.md file")
            print("or use {{include:mixin-name}} directive and run build")
        else:
            print("All mixins are up to date!")
        return

    if args.skill:
        print(f"\nBuilding skill: {args.skill}")
        changed, message = builder.build_skill(args.skill, args.dry_run)
        print(f"  {message}")
    else:
        print("\nProcessing skills with {{include:}} directives...")
        results = builder.build_all_skills(args.dry_run)

        if results:
            # Summary
            changed = sum(1 for msg in results.values() if "Processed" in msg or "Would process" in msg)
            print(f"\nSummary: {changed}/{len(results)} skills {'would be ' if args.dry_run else ''}processed")


if __name__ == "__main__":
    main()
