#!/usr/bin/env python3
"""
ABOUTME: Claude Code Hooks Setup Script

Purpose: Automatically configure PostToolUse hooks for Claude Code based on CLAUDE.md
Responsibilities:
  - Parse CLAUDE.md to extract linting tools and languages
  - Detect package manager (pnpm, npm, yarn, bun)
  - Generate appropriate hook configurations
  - Create/update .claude/settings.json
  - Support multi-language projects

Usage:
  python setup_claude_hooks.py [--project-root PATH] [--user-level]

Last Modified: 2026-01-10
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


class ClaudeHooksSetup:
    """Configure Claude Code PostToolUse hooks for auto-linting"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.claude_md_path = project_root / "CLAUDE.md"
        self.settings_path = project_root / ".claude" / "settings.json"

        # Language to linter mapping
        self.linter_commands = {
            "javascript": 'npx eslint "{file}" --fix 2>/dev/null || true',
            "typescript": 'npx eslint "{file}" --fix 2>/dev/null || true',
            "python": 'black "{file}" 2>/dev/null || true',
            "ruby": 'rubocop "{file}" --auto-correct 2>/dev/null || true',
            "go": 'gofmt -w "{file}" 2>/dev/null || true',
            "rust": 'rustfmt "{file}" 2>/dev/null || true',
        }

        # File extension to language mapping
        self.extension_map = {
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".mjs": "javascript",
            ".cjs": "javascript",
            ".py": "python",
            ".rb": "ruby",
            ".go": "go",
            ".rs": "rust",
        }

    def read_claude_md(self) -> str:
        """Read CLAUDE.md content"""
        if not self.claude_md_path.exists():
            raise FileNotFoundError(f"CLAUDE.md not found at {self.claude_md_path}")

        return self.claude_md_path.read_text(encoding="utf-8")

    def detect_languages(self, content: str) -> List[str]:
        """Detect languages used in the project from CLAUDE.md"""
        languages = set()

        # Check stack section
        if "[stack]" in content:
            # Look for common language/framework mentions
            patterns = {
                "typescript": r"TypeScript|\.tsx?",
                "javascript": r"JavaScript|\.jsx?|React|Vue|Svelte|Astro",
                "python": r"Python|Flask|Django|FastAPI|\.py",
                "ruby": r"Ruby|Rails|\.rb",
                "go": r"\bGo\b|Golang|\.go",
                "rust": r"Rust|\.rs",
            }

            for lang, pattern in patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    languages.add(lang)

        return sorted(languages)

    def detect_linters(self, content: str) -> Dict[str, str]:
        """Detect linting tools from CLAUDE.md"""
        linters = {}

        # Check for ESLint
        if re.search(r"ESLint|eslint", content, re.IGNORECASE):
            linters["javascript"] = "eslint"
            linters["typescript"] = "eslint"

        # Check for Prettier (formatting, not linting)
        if re.search(r"Prettier|prettier", content, re.IGNORECASE):
            # Prettier can be added as secondary formatting step
            pass

        # Check for Python linters
        if re.search(r"Black\b", content):
            linters["python"] = "black"
        elif re.search(r"Ruff\b", content):
            linters["python"] = "ruff"
        elif re.search(r"Pylint", content):
            linters["python"] = "pylint"

        # Check for Ruby linters
        if re.search(r"RuboCop|rubocop", content, re.IGNORECASE):
            linters["ruby"] = "rubocop"

        return linters

    def detect_package_manager(self) -> str:
        """Detect package manager from lock files"""
        if (self.project_root / "pnpm-lock.yaml").exists():
            return "pnpm"
        elif (self.project_root / "yarn.lock").exists():
            return "yarn"
        elif (self.project_root / "bun.lockb").exists():
            return "bun"
        elif (self.project_root / "package-lock.json").exists():
            return "npm"
        else:
            return "npx"  # Default fallback

    def build_hook_command(self, languages: List[str], package_manager: str) -> str:
        """Build the shell command for PostToolUse hook"""
        if not languages:
            return ""

        # Build conditional chain for multiple languages
        conditions = []

        for lang in languages:
            extensions = [ext for ext, l in self.extension_map.items() if l == lang]
            if not extensions:
                continue

            # Build file extension checks
            ext_checks = " || ".join(
                [f'"$CLAUDE_TOOL_FILE_PATH" == *{ext}' for ext in extensions]
            )

            # Get linter command
            cmd = self.linter_commands.get(lang, "")
            if not cmd:
                continue

            # Replace {file} with environment variable
            cmd = cmd.replace("{file}", "$CLAUDE_TOOL_FILE_PATH")

            # Adjust for package manager
            if package_manager == "pnpm" and "npx" in cmd:
                cmd = cmd.replace("npx", "pnpm exec")
            elif package_manager == "yarn" and "npx" in cmd:
                cmd = cmd.replace("npx", "yarn")

            conditions.append(f"if [[ {ext_checks} ]]; then {cmd}")

        # Join conditions with elif
        if len(conditions) == 1:
            return conditions[0] + "; fi"
        else:
            command = conditions[0]
            for cond in conditions[1:]:
                command += "; el" + cond
            command += "; fi"
            return command

    def generate_hook_config(self, languages: List[str]) -> Dict:
        """Generate Claude Code hook configuration"""
        package_manager = self.detect_package_manager()
        command = self.build_hook_command(languages, package_manager)

        return {
            "description": "Automatically run linting tools after file modifications",
            "hooks": {
                "PostToolUse": [
                    {
                        "matcher": "Edit|Write",
                        "hooks": [{"type": "command", "command": command}],
                    }
                ]
            },
        }

    def merge_with_existing(self, new_config: Dict) -> Dict:
        """Merge new hook config with existing settings"""
        if not self.settings_path.exists():
            return new_config

        try:
            existing = json.loads(self.settings_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            return new_config

        # Simple merge: replace PostToolUse hooks
        # More sophisticated merge could preserve other hooks
        if "hooks" not in existing:
            existing["hooks"] = {}

        existing["hooks"]["PostToolUse"] = new_config["hooks"]["PostToolUse"]

        # Update description if not present
        if "description" not in existing:
            existing["description"] = new_config["description"]

        return existing

    def write_settings(self, config: Dict):
        """Write configuration to .claude/settings.json"""
        # Ensure .claude directory exists
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)

        # Write JSON with nice formatting
        self.settings_path.write_text(json.dumps(config, indent=2), encoding="utf-8")

    def run(self) -> Dict:
        """Main execution flow"""
        print(f"[*] Analyzing CLAUDE.md at {self.claude_md_path}...")

        # Read and parse CLAUDE.md
        content = self.read_claude_md()
        languages = self.detect_languages(content)
        linters = self.detect_linters(content)

        if not languages:
            print("[!] No languages detected in CLAUDE.md")
            print(
                "    Make sure [stack] section includes language/framework information"
            )
            return {}

        print(f"[+] Detected languages: {', '.join(languages)}")
        print(f"[+] Detected linters: {linters}")

        # Generate hook configuration
        config = self.generate_hook_config(languages)

        # Merge with existing settings
        merged_config = self.merge_with_existing(config)

        # Write to settings.json
        self.write_settings(merged_config)

        print(f"\n[SUCCESS] Claude Code hooks configured!")
        print(f"[*] Configuration written to: {self.settings_path}")
        print(f"\nPostToolUse hook will run on: {', '.join(languages)} files")
        print("\nYour files will be automatically linted as Claude Code edits them!")

        return merged_config


def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Set up Claude Code hooks based on CLAUDE.md"
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--user-level",
        action="store_true",
        help="Generate user-level configuration (print to stdout)",
    )

    args = parser.parse_args()

    try:
        setup = ClaudeHooksSetup(args.project_root)
        config = setup.run()

        if args.user_level:
            print("\n" + "=" * 60)
            print("User-level configuration (add to your Claude Code settings):")
            print("=" * 60)
            print(json.dumps(config, indent=2))

    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
