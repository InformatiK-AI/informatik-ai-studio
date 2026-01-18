# Scripts Documentation

This directory contains executable scripts for the **preflight-check** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `preflight.py` | Pre-flight validation before feature implementation | Production |

---

## preflight.py

**Purpose:** Validates project readiness before starting feature implementation. Checks context files, agent availability, CLAUDE.md, git status, dependencies, and required tools.

### Usage

```bash
python3 preflight.py --feature "feature_name" [--project-root "."] [--output "report.json"]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--feature` | Yes | - | Name of the feature to validate (e.g., "user_auth") |
| `--project-root` | No | `.` | Project root directory path |
| `--output` | No | - | Output file path for JSON report |

### Checks Performed

1. **Context File** - Validates `context_session_feature_{NAME}.md` exists and has required sections
2. **Agent Availability** - Checks if required agents are present in `.claude/agents/`
3. **CLAUDE.md** - Validates existence and required sections ([stack], [methodology], [core_team])
4. **Git Status** - Checks for uncommitted changes, merge conflicts, worktree conflicts
5. **Dependencies** - Validates node_modules or Python venv as applicable
6. **Test Framework** - Checks for jest, vitest, playwright, or pytest configuration
7. **Required Tools** - Validates git, python3, and gh CLI are installed

### Output

**Console Output:**
```
============================================================
PRE-FLIGHT CHECK REPORT
============================================================

Feature: user_auth

OVERALL STATUS: GO_WITH_WARNINGS

✅ PASS (4):
  - Context file exists and is valid
  - All required agents available
  - Git working tree is clean
  - All required CLI tools available

⚠️ WARNING (2):
  - Workflow not set in [methodology] section
    Fix: Set workflow to 'TDD', 'RAD', or 'Standard'
  - node_modules/ not found
    Fix: Run: npm install

RECOMMENDATION: ⚠️ Proceed with caution. Address warnings if possible.
============================================================
```

**JSON Output (when `--output` specified):**
```json
{
  "feature": "user_auth",
  "overall_status": "GO_WITH_WARNINGS",
  "pass_count": 4,
  "warning_count": 2,
  "fail_count": 0,
  "checks": [
    {
      "name": "Context File",
      "status": "PASS",
      "message": "Context file exists and is valid",
      "fix_suggestion": null
    }
  ]
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | GO or GO_WITH_WARNINGS - safe to proceed |
| `1` | NO_GO - critical errors, cannot proceed |

### Example

```bash
# Basic usage
python3 preflight.py --feature "user_authentication"

# With JSON report output
python3 preflight.py --feature "user_authentication" --output ".claude/logs/preflight_report.json"

# Specify project root
python3 preflight.py --feature "shopping_cart" --project-root "/path/to/project"
```

### Dependencies

- Python 3.8+
- Standard library only (no external packages required)
- Requires git CLI to be installed for git status checks
