#!/usr/bin/env python3
"""
ABOUTME: Git Hooks Setup Script

Purpose: Automate Git hooks setup based on CLAUDE.md requirements
Responsibilities:
  - Read and parse CLAUDE.md to extract testing/linting/formatting requirements
  - Install required dependencies (husky, lint-staged, @commitlint packages)
  - Create/update Husky hooks (pre-commit, commit-msg, pre-push)
  - Configure lint-staged and commitlint
  - Merge with existing hooks intelligently

Dependencies: None (uses stdlib only)
Usage: python setup_hooks.py [--project-root PATH]

Last Modified: 2026-01-09
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional


class HooksSetup:
    """Manages Git hooks setup for a project based on CLAUDE.md"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.claude_md = project_root / "CLAUDE.md"
        self.package_json = project_root / "package.json"
        self.husky_dir = project_root / ".husky"
        self.skill_dir = Path(__file__).parent.parent

    def read_claude_md(self) -> str:
        """Read CLAUDE.md file"""
        if not self.claude_md.exists():
            raise FileNotFoundError(f"CLAUDE.md not found at {self.claude_md}")
        return self.claude_md.read_text(encoding="utf-8")

    def extract_requirements(self, content: str) -> Dict[str, Any]:
        """Extract testing, linting, and formatting requirements from CLAUDE.md"""
        requirements = {
            "test_command": "pnpm test",
            "lint_command": "pnpm lint",
            "format_command": "pnpm format",
            "type_check_command": "pnpm type-check",
            "build_command": "pnpm build",
            "package_manager": "pnpm",
            "conventional_commits": True,
        }

        # Extract package manager
        if "npm install" in content.lower():
            requirements["package_manager"] = "npm"
        elif "yarn install" in content.lower():
            requirements["package_manager"] = "yarn"

        # Extract commands from CLAUDE.md
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if "pnpm test" in line or "npm test" in line:
                requirements["test_command"] = line.strip("# -`")
            if "pnpm lint" in line or "npm run lint" in line:
                requirements["lint_command"] = line.strip("# -`")
            if "pnpm format" in line or "npm run format" in line:
                requirements["format_command"] = line.strip("# -`")
            if "pnpm type-check" in line or "tsc" in line:
                requirements["type_check_command"] = line.strip("# -`")

        return requirements

    def install_dependencies(self, pkg_manager: str) -> bool:
        """Install husky, lint-staged, and commitlint packages"""
        print("📦 Installing dependencies...")

        dependencies = [
            "husky",
            "lint-staged",
            "@commitlint/cli",
            "@commitlint/config-conventional",
        ]

        try:
            if pkg_manager == "pnpm":
                cmd = ["pnpm", "add", "-D"] + dependencies
            elif pkg_manager == "yarn":
                cmd = ["yarn", "add", "--dev"] + dependencies
            else:
                cmd = ["npm", "install", "--save-dev"] + dependencies

            subprocess.run(cmd, check=True, cwd=self.project_root)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return False

    def init_husky(self, pkg_manager: str) -> bool:
        """Initialize Husky"""
        print("🐕 Initializing Husky...")

        try:
            if pkg_manager == "pnpm":
                cmd = ["pnpm", "exec", "husky", "init"]
            else:
                cmd = ["npx", "husky", "init"]

            subprocess.run(cmd, check=True, cwd=self.project_root)
            print("✅ Husky initialized")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize Husky: {e}")
            return False

    def copy_hook_files(self) -> None:
        """Copy hook files from assets to .husky directory"""
        print("📝 Creating hook files...")

        hooks_src = self.skill_dir / "assets" / "hooks"
        hook_files = ["pre-commit", "commit-msg", "pre-push"]

        for hook_file in hook_files:
            src = hooks_src / hook_file
            dst = self.husky_dir / hook_file

            if src.exists():
                # If hook already exists, merge intelligently
                if dst.exists():
                    print(f"  ⚠️  {hook_file} already exists, merging...")
                    self.merge_hook_file(src, dst)
                else:
                    shutil.copy2(src, dst)
                    print(f"  ✅ Created {hook_file}")

                # Make hook executable (Unix-like systems)
                if os.name != "nt":  # Not Windows
                    os.chmod(dst, 0o755)

    def merge_hook_file(self, src: Path, dst: Path) -> None:
        """Merge existing hook with new hook content"""
        existing_content = dst.read_text(encoding="utf-8")
        new_content = src.read_text(encoding="utf-8")

        # Skip if content is identical
        if existing_content == new_content:
            return

        # Simple merge: append new commands if not already present
        lines_to_add = []
        for line in new_content.split("\n"):
            if (
                line.strip()
                and not line.startswith("#")
                and line not in existing_content
            ):
                lines_to_add.append(line)

        if lines_to_add:
            merged = existing_content.rstrip() + "\n\n# Added by hooks-setup skill\n"
            merged += "\n".join(lines_to_add) + "\n"
            dst.write_text(merged, encoding="utf-8")
            print(f"    Merged new commands into {dst.name}")

    def update_package_json(self, pkg_manager: str) -> None:
        """Update package.json with lint-staged configuration and scripts"""
        print("📄 Updating package.json...")

        if not self.package_json.exists():
            print("  ⚠️  package.json not found, skipping")
            return

        with open(self.package_json, "r", encoding="utf-8") as f:
            package_data = json.load(f)

        # Add lint-staged configuration reference
        if "lint-staged" not in package_data:
            package_data["lint-staged"] = {}
            print("  ✅ Added lint-staged configuration reference")

        # Add prepare script for Husky
        if "scripts" not in package_data:
            package_data["scripts"] = {}

        if "prepare" not in package_data["scripts"]:
            package_data["scripts"]["prepare"] = "husky"
            print("  ✅ Added prepare script for Husky")

        # Write updated package.json
        with open(self.package_json, "w", encoding="utf-8") as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
            f.write("\n")  # Add trailing newline

    def copy_config_files(self) -> None:
        """Copy commitlint and lint-staged config files to project root"""
        print("⚙️  Copying configuration files...")

        # Copy commitlint.config.js
        commitlint_src = self.skill_dir / "assets" / "commitlint.config.js"
        commitlint_dst = self.project_root / "commitlint.config.js"

        if not commitlint_dst.exists() and commitlint_src.exists():
            shutil.copy2(commitlint_src, commitlint_dst)
            print("  ✅ Created commitlint.config.js")
        elif commitlint_dst.exists():
            print("  ℹ️  commitlint.config.js already exists, skipping")

        # Copy lint-staged.config.js
        lint_staged_src = self.skill_dir / "assets" / "lint-staged.config.js"
        lint_staged_dst = self.project_root / "lint-staged.config.js"

        if not lint_staged_dst.exists() and lint_staged_src.exists():
            shutil.copy2(lint_staged_src, lint_staged_dst)
            print("  ✅ Created lint-staged.config.js")
        elif lint_staged_dst.exists():
            print("  ℹ️  lint-staged.config.js already exists, skipping")

    def run_setup(self) -> bool:
        """Run the complete setup process"""
        print("🚀 Setting up Git hooks based on CLAUDE.md...\n")

        try:
            # Read and parse CLAUDE.md
            claude_content = self.read_claude_md()
            requirements = self.extract_requirements(claude_content)
            pkg_manager = requirements["package_manager"]

            print(f"📋 Detected package manager: {pkg_manager}")
            print(f"📋 Detected commands:")
            print(f"   - Test: {requirements['test_command']}")
            print(f"   - Lint: {requirements['lint_command']}")
            print(f"   - Format: {requirements['format_command']}")
            print()

            # Install dependencies
            if not self.install_dependencies(pkg_manager):
                return False

            # Initialize Husky
            if not self.husky_dir.exists():
                if not self.init_husky(pkg_manager):
                    return False
            else:
                print("🐕 Husky already initialized")

            # Copy hook files
            self.copy_hook_files()

            # Copy configuration files
            self.copy_config_files()

            # Update package.json
            self.update_package_json(pkg_manager)

            print("\n✅ Git hooks setup completed successfully!")
            print("\n📌 Next steps:")
            print("   1. Review hook files in .husky/ directory")
            print("   2. Customize commitlint.config.js if needed")
            print("   3. Customize lint-staged.config.js if needed")
            print("   4. Test hooks by making a commit")

            return True

        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            import traceback

            traceback.print_exc()
            return False


def main():
    """Main entry point"""
    # Determine project root
    if len(sys.argv) > 2 and sys.argv[1] == "--project-root":
        project_root = Path(sys.argv[2]).resolve()
    else:
        # Assume script is run from project root or .claude/skills/hooks-setup/scripts/
        current = Path.cwd()
        if (current / "CLAUDE.md").exists():
            project_root = current
        elif (current.parent.parent.parent.parent / "CLAUDE.md").exists():
            project_root = current.parent.parent.parent.parent
        else:
            print(
                "❌ Could not find CLAUDE.md. Please run from project root or use --project-root"
            )
            sys.exit(1)

    print(f"📁 Project root: {project_root}\n")

    setup = HooksSetup(project_root)
    success = setup.run_setup()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
