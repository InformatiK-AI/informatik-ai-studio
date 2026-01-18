---
name: hooks-setup
description: This skill should be invoked automatically after CLAUDE.md is created, modified, or replaced to set up or update Git hooks (Husky, lint-staged, commitlint), Claude Code hooks (PostToolUse linting, pre-commit validation), AND security scanning hooks (semgrep, bandit, gitleaks for vulnerability and secrets detection) based on the project's code quality and security requirements. Also invoke when users explicitly request hook configuration, commit validation, code quality automation, or security scanning.
version: 2.1.0
---

# Code Quality Hooks Orchestrator

Meta-skill that coordinates the setup of all code quality and security hooks.

## Purpose

This skill orchestrates three specialized hook setup skills:

| Sub-Skill | Purpose | Trigger |
|-----------|---------|---------|
| `git-hooks-setup` | Pre-commit, commit-msg, pre-push hooks via Husky | Commit-time validation |
| `claude-code-hooks` | PostToolUse auto-linting after file edits | Real-time linting |
| `security-scanning-hooks` | Vulnerability and secrets detection | Security scanning |

## When to Invoke

### Automatic Triggers
1. **After CLAUDE.md changes** - Primary trigger
2. **During project initialization** - New project setup

### Manual Invocation
- "Set up hooks" / "Configure code quality"
- "Set up Git hooks" → delegates to `git-hooks-setup`
- "Set up Claude Code hooks" → delegates to `claude-code-hooks`
- "Set up security scanning" → delegates to `security-scanning-hooks`

## Orchestration Workflow

```
CLAUDE.md created/modified
         │
         ▼
   hooks-setup (this skill)
         │
         ├── Load modular_index.json (if exists)
         │   └── Determine rules to apply
         │
         ├── git-hooks-setup
         │   └── Husky, lint-staged, commitlint
         │
         ├── claude-code-hooks
         │   └── PostToolUse auto-linting
         │
         └── security-scanning-hooks
             └── semgrep, bandit, gitleaks
```

### Modular Index Integration (v2.1)

When `.claude/cache/modular_index.json` exists, hooks-setup uses it to determine appropriate configurations:

```
IF .claude/cache/modular_index.json exists:
  MODULAR_INDEX = JSON.parse(".claude/cache/modular_index.json")

  # Read rules to determine hook configuration
  For each rule in MODULAR_INDEX.auto_loaded:
    IF rule.file contains "code-standards":
      # Extract linting rules for git-hooks-setup
      LINT_CONFIG = parse_linting_rules(rule.file)

    IF rule.file contains "testing-policy":
      # Extract test requirements for pre-push hooks
      TEST_CONFIG = parse_test_requirements(rule.file)

    IF rule.file contains "security-policy":
      # Configure security scanning based on policy
      SECURITY_CONFIG = parse_security_requirements(rule.file)

  # Pass configurations to sub-skills
  Invoke git-hooks-setup with LINT_CONFIG, TEST_CONFIG
  Invoke security-scanning-hooks with SECURITY_CONFIG

ELSE:
  # Fallback: Parse CLAUDE.md directly
  Parse CLAUDE.md for [code_standards], [testing_requirements], [security_requirements]
```

## Quick Setup

### Full Setup (All Hooks)

Run all three hook types:

```bash
# 1. Git hooks
python .claude/skills/git-hooks-setup/scripts/setup_hooks.py

# 2. Claude Code hooks
python .claude/skills/claude-code-hooks/scripts/setup_claude_hooks.py

# 3. Security scanning (manual tool installation)
pip install semgrep bandit
brew install gitleaks
```

### Selective Setup

Set up only specific hooks:

```bash
# Git hooks only
python .claude/skills/git-hooks-setup/scripts/setup_hooks.py

# Claude Code hooks only
python .claude/skills/claude-code-hooks/scripts/setup_claude_hooks.py
```

## Sub-Skill Details

### git-hooks-setup

**What it configures:**
- Pre-commit: lint-staged (ESLint, Prettier on staged files)
- Commit-msg: commitlint (Conventional Commits validation)
- Pre-push: Tests, type checking, build validation

**Files created:**
- `.husky/pre-commit`
- `.husky/commit-msg`
- `.husky/pre-push`
- `lint-staged.config.js`
- `commitlint.config.js`

### claude-code-hooks

**What it configures:**
- PostToolUse hooks for Edit/Write operations
- Auto-linting for JS/TS/Python/Ruby/Go/Rust
- Auto-fix when linters support it

**Files created:**
- `.claude/settings.json`

### security-scanning-hooks

**What it configures:**
- Semgrep: Multi-language vulnerability detection
- Bandit: Python security scanner
- Gitleaks: Secrets detection

**Prerequisites:**
- Install tools: `pip install semgrep bandit` + `brew install gitleaks`

## Result Summary

After full setup:

```
✅ Code quality hooks configured!

Git Hooks:
• pre-commit: ESLint + Prettier on staged files
• commit-msg: Conventional Commits validation
• pre-push: Tests + type-check + build

Claude Code Hooks:
• PostToolUse: Auto-lint files after edits
• Configuration: .claude/settings.json

Security Scanning:
• semgrep: Vulnerability detection
• gitleaks: Secrets scanning
• bandit: Python security (if applicable)
```

## Delegation Rules

| User Request | Delegated To |
|--------------|--------------|
| "Set up all hooks" | All three sub-skills |
| "Configure Husky" | git-hooks-setup |
| "Set up lint-staged" | git-hooks-setup |
| "Configure commitlint" | git-hooks-setup |
| "Enable auto-linting" | claude-code-hooks |
| "PostToolUse hooks" | claude-code-hooks |
| "Security scanning" | security-scanning-hooks |
| "Detect secrets" | security-scanning-hooks |

## Best Practices

1. **Run all three** for comprehensive code quality + security
2. **Analyze CLAUDE.md first** to understand project requirements
3. **Merge with existing** hooks rather than replacing
4. **Test after setup** to verify hooks work
5. **Keep in sync** with CI/CD pipeline checks

## Legacy Support

This skill maintains backward compatibility with the original combined hooks-setup. All original functionality is preserved across the three sub-skills.

## References

- Git hooks: `git-hooks-setup/references/hook-patterns.md`
- Claude hooks: `claude-code-hooks/references/claude-hook-patterns.md`
- Security: `security-scanning-hooks/references/claude-hook-patterns.md`
