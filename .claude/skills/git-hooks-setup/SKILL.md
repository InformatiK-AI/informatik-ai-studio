---
name: git-hooks-setup
description: Set up Git hooks (Husky, lint-staged, commitlint) for commit-time code quality enforcement. Configures pre-commit, commit-msg, and pre-push hooks based on CLAUDE.md requirements.
version: 1.0.0
---

# Git Hooks Setup

Configure Git hooks for commit-time code quality enforcement using Husky, lint-staged, and commitlint.

## Purpose

Automate the configuration of Git hooks to enforce code quality standards at commit time:

- **Pre-commit**: Run linters and formatters on staged files
- **Commit-msg**: Validate commit message format (Conventional Commits)
- **Pre-push**: Run tests, type checking, and build validation

## When to Invoke

### Automatic (via hooks-setup orchestrator)
- After CLAUDE.md is created or modified
- During project initialization

### Manual Invocation
- "Set up Git hooks" / "Configure Husky"
- "Add pre-commit checks"
- "Configure commit message validation"
- "Set up lint-staged"

## Setup Process

### Step 1: Analyze CLAUDE.md

Read CLAUDE.md to extract:
1. Package manager (pnpm/npm/yarn)
2. Linting commands
3. Formatting commands
4. Type checking commands
5. Test commands
6. Build commands
7. Commit message format requirements

### Step 2: Run Setup Script

```bash
python .claude/skills/git-hooks-setup/scripts/setup_hooks.py
```

**What the script does:**
1. Parses CLAUDE.md requirements
2. Installs dependencies (husky, lint-staged, @commitlint/cli)
3. Initializes Husky
4. Creates hook files in `.husky/`
5. Configures lint-staged and commitlint
6. Updates package.json

### Step 3: Verify Installation

After setup:
1. Check `.husky/` directory exists
2. Verify config files created
3. Test with a sample commit

## Hook Configuration

### Pre-commit Hook
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
pnpm lint-staged
```

Runs lint-staged on staged files only for fast execution.

### Commit-msg Hook
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
pnpm exec commitlint --edit "$1"
```

Validates commit message against Conventional Commits format.

### Pre-push Hook
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"
pnpm test && pnpm type-check && pnpm build
```

Runs full test suite and build validation before push.

## Configuration Files

### lint-staged.config.js
```javascript
module.exports = {
  '*.{ts,tsx,js,jsx}': ['eslint --fix', 'prettier --write'],
  '*.{json,md,css}': ['prettier --write'],
};
```

### commitlint.config.js
```javascript
module.exports = {
  extends: ['@commitlint/config-conventional'],
};
```

## Best Practices

1. **Keep pre-commit fast** (< 10 seconds)
2. **Use lint-staged** for staged-only checks
3. **Mirror CI checks** in pre-push hooks
4. **Preserve customizations** when updating hooks

## Customization

See `references/hook-patterns.md` for:
- Advanced lint-staged patterns
- Custom commitlint rules
- Performance optimization
- Merge strategies for existing hooks

## Bypass (Emergency Only)

```bash
git commit --no-verify
git push --no-verify
```
