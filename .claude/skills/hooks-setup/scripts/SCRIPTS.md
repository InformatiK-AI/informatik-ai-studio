# Scripts Documentation

This directory contains executable scripts for the **hooks-setup** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `setup_hooks.py` | Set up Git hooks (Husky, lint-staged, commitlint) | Production |
| `setup_claude_hooks.py` | Configure Claude Code PostToolUse hooks | Production |

---

## setup_hooks.py

**Purpose:** Automates Git hooks setup based on CLAUDE.md requirements. Installs Husky, lint-staged, and commitlint, then configures pre-commit, commit-msg, and pre-push hooks.

### Usage

```bash
python3 setup_hooks.py [--project-root PATH]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--project-root` | No | `.` | Project root directory path |

### Process

1. **Read CLAUDE.md** - Extracts testing/linting/formatting requirements
2. **Detect Package Manager** - npm, pnpm, or yarn
3. **Install Dependencies** - husky, lint-staged, @commitlint packages
4. **Create Husky Hooks** - pre-commit, commit-msg, pre-push
5. **Configure lint-staged** - Based on detected file types
6. **Configure commitlint** - For conventional commits

### Output

```
📦 Installing dependencies...
✅ Dependencies installed successfully

🔧 Setting up Husky hooks...
✅ Created pre-commit hook
✅ Created commit-msg hook
✅ Created pre-push hook

📝 Configuring lint-staged...
✅ lint-staged configured

✅ Git hooks setup complete!
```

### Dependencies

- Python 3.8+ (stdlib only)
- Requires npm/pnpm/yarn installed
- Requires CLAUDE.md at project root

---

## setup_claude_hooks.py

**Purpose:** Configures Claude Code PostToolUse hooks for automatic linting after file edits. Parses CLAUDE.md to detect languages and generates appropriate hook configurations.

### Usage

```bash
python3 setup_claude_hooks.py [--project-root PATH] [--user-level]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--project-root` | No | `.` | Project root directory path |
| `--user-level` | No | false | Install at user level instead of project |

### Supported Languages

| Language | Linter Command |
|----------|---------------|
| TypeScript/JavaScript | `npx eslint "{file}" --fix` |
| Python | `black "{file}"` |
| Ruby | `rubocop "{file}" --auto-correct` |
| Go | `gofmt -w "{file}"` |
| Rust | `rustfmt "{file}"` |

### Output

Creates/updates `.claude/settings.json` with PostToolUse hooks:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write|NotebookEdit",
        "command": "npx eslint \"$FILE\" --fix 2>/dev/null || true"
      }
    ]
  }
}
```

### Dependencies

- Python 3.8+ (stdlib only)
- Requires CLAUDE.md at project root
