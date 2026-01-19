#!/usr/bin/env python3
"""
Loads and caches project context for flow commands.

Usage:
    python3 load_context.py --feature "auth_system" --output ".claude/cache/context_auth_system.json"

Loads:
    - CLAUDE.md (parsed sections)
    - .claude/rules/*.md (global rules)
    - .claude/rules/domain/*.md (path-specific rules)
    - .claude/docs/{feature}/*.md (agent plans if exist)
    - .claude/cache/modular_index.json (if exists)
"""
import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path


def parse_claude_md(content):
    """Parse CLAUDE.md into sections based on ## [section_name] headers."""
    sections = {}
    current_section = None
    current_content = []

    for line in content.split("\n"):
        # Match section headers like ## [section_name]
        match = re.match(r"^##\s*\[(\w+)\]", line)
        if match:
            if current_section:
                sections[current_section] = "\n".join(current_content).strip()
            current_section = match.group(1)
            current_content = []
        elif current_section:
            current_content.append(line)

    # Don't forget the last section
    if current_section:
        sections[current_section] = "\n".join(current_content).strip()

    return sections


def load_rules(rules_dir):
    """Load all rules from .claude/rules/ directory."""
    rules = {"global": {}, "domain": {}}

    if not rules_dir.exists():
        return rules

    # Load global rules (direct children of rules/)
    for rule_file in rules_dir.glob("*.md"):
        if rule_file.name != ".keep":
            try:
                content = rule_file.read_text(encoding="utf-8")
                rules["global"][rule_file.stem] = content
            except IOError as e:
                print(f"Warning: Could not read {rule_file}: {e}")

    # Load domain-specific rules
    domain_dir = rules_dir / "domain"
    if domain_dir.exists():
        for rule_file in domain_dir.glob("*.md"):
            if rule_file.name != ".keep":
                try:
                    content = rule_file.read_text(encoding="utf-8")
                    rules["domain"][rule_file.stem] = content
                except IOError as e:
                    print(f"Warning: Could not read {rule_file}: {e}")

    return rules


def load_agent_plans(docs_dir, feature):
    """Load agent plans for a specific feature."""
    plans = {}
    feature_dir = docs_dir / feature

    if not feature_dir.exists():
        return plans

    for plan_file in feature_dir.glob("*.md"):
        if plan_file.name != ".keep":
            try:
                content = plan_file.read_text(encoding="utf-8")
                plans[plan_file.stem] = content
            except IOError as e:
                print(f"Warning: Could not read {plan_file}: {e}")

    return plans


def load_session_file(sessions_dir, feature):
    """Load session context file for a feature if it exists."""
    session_content = None
    session_path = None

    # Try different session file patterns
    patterns = [
        f"context_session_feature_{feature}.md",
        f"context_session_epic_{feature}.md",
        f"context_session_project_{feature}.md",
    ]

    for pattern in patterns:
        session_file = sessions_dir / pattern
        if session_file.exists():
            try:
                session_content = session_file.read_text(encoding="utf-8")
                session_path = str(session_file)
                break
            except IOError as e:
                print(f"Warning: Could not read {session_file}: {e}")

    return session_content, session_path


def load_modular_index(cache_dir):
    """Load modular index if it exists."""
    index_file = cache_dir / "modular_index.json"
    if index_file.exists():
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not load modular_index.json: {e}")
    return None


def load_context(args):
    """Load and cache project context."""
    base_path = Path(".")
    cache_dir = Path(".claude/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)

    context = {
        "version": "1.0",
        "feature": args.feature,
        "generated_at": datetime.now().isoformat(),
        "constitution": {},
        "rules": {"global": {}, "domain": {}},
        "plans": {},
        "session": None,
        "session_path": None,
        "docs_index": [],
        "modular_index": None
    }

    # Load CLAUDE.md (the "Constitution")
    claude_md = base_path / "CLAUDE.md"
    if claude_md.exists():
        try:
            content = claude_md.read_text(encoding="utf-8")
            context["constitution"] = parse_claude_md(content)
            print(f"Loaded CLAUDE.md with {len(context['constitution'])} sections")
        except IOError as e:
            print(f"Warning: Could not read CLAUDE.md: {e}")
    else:
        print("Warning: CLAUDE.md not found")

    # Load modular index if exists
    modular_index = load_modular_index(cache_dir)
    if modular_index:
        context["modular_index"] = modular_index
        context["docs_index"] = modular_index.get("on_demand", [])
        print(f"Loaded modular_index.json with {len(context['docs_index'])} on-demand docs")

    # Load rules
    rules_dir = base_path / ".claude" / "rules"
    context["rules"] = load_rules(rules_dir)
    global_count = len(context["rules"]["global"])
    domain_count = len(context["rules"]["domain"])
    print(f"Loaded {global_count} global rules, {domain_count} domain rules")

    # Load agent plans for the feature
    docs_dir = base_path / ".claude" / "docs"
    context["plans"] = load_agent_plans(docs_dir, args.feature)
    print(f"Loaded {len(context['plans'])} agent plans for feature: {args.feature}")

    # Load session file if exists
    sessions_dir = base_path / ".claude" / "sessions"
    session_content, session_path = load_session_file(sessions_dir, args.feature)
    if session_content:
        context["session"] = session_content
        context["session_path"] = session_path
        print(f"Loaded session file: {session_path}")

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2, ensure_ascii=False)

    print(f"Context cached to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Load and cache project context for flow commands"
    )

    parser.add_argument(
        "--feature",
        required=True,
        help="Feature name to load context for"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for cached context JSON"
    )

    args = parser.parse_args()
    load_context(args)


if __name__ == "__main__":
    main()
