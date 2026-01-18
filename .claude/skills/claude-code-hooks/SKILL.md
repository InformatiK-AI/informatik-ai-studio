---
name: claude-code-hooks
description: Configure Claude Code PostToolUse hooks for real-time auto-linting. Automatically runs linters after Edit/Write operations for immediate code quality feedback.
version: 1.0.0
---

# Claude Code Hooks Setup

Configure PostToolUse hooks for real-time auto-linting as Claude Code edits files.

## Purpose

Enable automatic linting after every file edit by Claude Code:

- **PostToolUse hooks**: Run after Edit or Write tool operations
- **Auto-fix**: Apply linter fixes automatically
- **Multi-language**: Support for JS/TS/Python/Ruby/Go/Rust

## When to Invoke

### Automatic (via hooks-setup orchestrator)
- After CLAUDE.md is created or modified
- During project initialization

### Manual Invocation
- "Set up Claude Code hooks"
- "Enable auto-linting on file edits"
- "Configure PostToolUse hooks"
- "Run ESLint automatically after changes"

## Setup Process

### Step 1: Analyze CLAUDE.md

Identify:
1. Languages used in project
2. Linting tools (ESLint, Prettier, Black, etc.)
3. Package manager (for command execution)
4. Auto-fix capabilities

### Step 2: Run Setup Script

```bash
python .claude/skills/claude-code-hooks/scripts/setup_claude_hooks.py
```

**What the script does:**
1. Parses CLAUDE.md for linting tools
2. Detects package manager
3. Generates PostToolUse hook configuration
4. Creates/updates `.claude/settings.json`

### Step 3: Verify Installation

1. Edit a file with linting issues
2. Verify linter runs automatically
3. Check auto-fixes are applied

## Hook Configuration

### .claude/settings.json

```json
{
  "description": "Auto-lint files after Claude Code edits",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

## Language-Specific Patterns

### JavaScript/TypeScript
```bash
npx eslint "$CLAUDE_TOOL_FILE_PATH" --fix 2>/dev/null || true
```

### Python
```bash
black "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
```

### Ruby
```bash
rubocop "$CLAUDE_TOOL_FILE_PATH" --auto-correct 2>/dev/null || true
```

### Go
```bash
gofmt -w "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
```

### Rust
```bash
rustfmt "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
```

## Multi-Language Configuration

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then black \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts || \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

## Best Practices

1. **Graceful failure**: Always use `2>/dev/null || true`
2. **Auto-fix when possible**: Use `--fix` flags
3. **Check file extensions**: Use proper bash pattern matching
4. **Project-level config**: Use `.claude/settings.json` for teams
5. **Test with CLAUDE_TOOL_FILE_PATH**: Verify commands work

## Customization

See `references/claude-hook-patterns.md` for:
- Advanced hook patterns
- Conditional execution
- Performance optimization
- Debugging hooks

## Troubleshooting

### Hooks not running
1. Check `.claude/settings.json` exists
2. Verify JSON syntax is valid
3. Test command manually with CLAUDE_TOOL_FILE_PATH

### Linter not found
1. Ensure linter is in package.json
2. Check npx/pnpm exec path resolution
3. Install missing dependencies
