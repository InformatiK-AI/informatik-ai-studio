---
name: security-scanning-hooks
description: Configure security scanning hooks for vulnerability detection and secrets scanning. Uses semgrep, bandit, and gitleaks for automated security analysis on code changes.
version: 1.0.0
---

# Security Scanning Hooks

Automated security vulnerability scanning and secrets detection integrated with Claude Code.

## Purpose

Add real-time security scanning to catch issues as code is written:

- **Semgrep**: Multi-language vulnerability detection (OWASP, injection, etc.)
- **Bandit**: Python-specific security scanner
- **Gitleaks**: Secrets and credential detection
- **Pattern detection**: Regex-based hardcoded secrets scanning

## When to Invoke

### Automatic (via hooks-setup orchestrator)
- After CLAUDE.md is created or modified
- When security requirements are detected

### Manual Invocation
- "Set up security scanning"
- "Add vulnerability detection"
- "Scan for secrets in code"
- "Detect hardcoded passwords"
- "Run semgrep/bandit/gitleaks"

## Tool Installation

```bash
# Semgrep (recommended for all projects)
pip install semgrep
# OR
brew install semgrep

# Bandit (Python projects)
pip install bandit

# Gitleaks (all projects)
brew install gitleaks
# OR download from GitHub releases
```

## Hook Configuration

### PostToolUse Security Hook

```json
{
  "description": "Security vulnerability and secrets scanning",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v semgrep >/dev/null 2>&1; then semgrep --config=auto \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; if command -v bandit >/dev/null 2>&1 && [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then bandit \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; if command -v gitleaks >/dev/null 2>&1; then gitleaks detect --source=\"$CLAUDE_TOOL_FILE_PATH\" --no-git 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

## Tool Capabilities

### Semgrep
- Multi-language vulnerability detection
- OWASP Top 10 coverage
- SQL injection, XSS, command injection
- Community rules with `--config=auto`
- Supports: JS, TS, Python, Go, Ruby, Java, and more

### Bandit (Python only)
- Python-specific security issues
- Hardcoded passwords detection
- Weak cryptography detection
- Severity ratings

### Gitleaks
- Secrets detection across all file types
- API keys, tokens, credentials
- Pattern matching + entropy analysis
- Works without git (`--no-git` flag)

### Pattern Detection (Zero Dependencies)
```bash
if grep -qE '(password|secret|key|token)\s*=\s*["'\''][^"'\'']{8,}' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
  echo "Warning: Potential hardcoded secrets detected"
fi
```

## Graceful Degradation

The hook checks if each tool is installed before running:
- If a tool isn't installed, it's skipped (no errors)
- Pattern-based detection always runs (no dependencies)
- Minimum: Pattern detection provides basic secrets scanning

## Best Practices

1. **Install recommended tools**: semgrep + gitleaks at minimum
2. **Never block workflow**: All commands use `|| true`
3. **Review warnings immediately**: Don't ignore findings
4. **Update tools regularly**: Security scanners need updates
5. **Configure ignore files**: `.semgrepignore`, `.gitleaksignore`
6. **Test with known vulnerabilities**: Verify hooks catch issues

## Test Security Hooks

### Test secrets detection
```typescript
// test-secrets.ts
const API_KEY = "sk_test_EXAMPLE_KEY_DO_NOT_USE";
const PASSWORD = "hardcoded_password_123";
```

### Test vulnerability detection (Python)
```python
# test-vuln.py
import os
eval(user_input)  # Security issue: eval with user input
```

## Combined Configuration

Combine security scanning with linting in one hook:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi; if command -v semgrep >/dev/null 2>&1; then semgrep --config=auto \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; if command -v gitleaks >/dev/null 2>&1; then gitleaks detect --source=\"$CLAUDE_TOOL_FILE_PATH\" --no-git 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

## Notes

- Security hooks provide **warnings**, not errors (non-blocking)
- Tools check for installation before running
- For CI/CD, use stricter configurations with blocking failures
- See `references/claude-hook-patterns.md` for advanced patterns
