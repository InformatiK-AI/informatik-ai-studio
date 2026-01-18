# Scripts Documentation

This directory contains executable scripts for the **code-reviewer** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `code_quality_checker.py` | Analyze code quality metrics | Production |
| `pr_analyzer.py` | Analyze pull request changes | Production |
| `review_report_generator.py` | Generate formatted review reports | Production |

---

## code_quality_checker.py

**Purpose:** Analyzes code quality metrics for a target file or directory. Identifies code smells, complexity issues, and best practice violations.

### Usage

```bash
python3 code_quality_checker.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Target path to analyze |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Output

```
==================================================
REPORT
==================================================
Target: ./src/components
Status: success
Findings: 12
==================================================
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Analysis completed successfully |
| `1` | Error during analysis |

---

## pr_analyzer.py

**Purpose:** Analyzes pull request changes to identify potential issues, suggest improvements, and highlight areas needing review attention.

### Usage

```bash
python3 pr_analyzer.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | PR diff or directory to analyze |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Output

Analyzes PR changes and provides:
- Summary of changes
- Potential issues detected
- Suggestions for improvement
- Files requiring special attention

---

## review_report_generator.py

**Purpose:** Generates formatted code review reports from analysis results. Supports multiple output formats.

### Usage

```bash
python3 review_report_generator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Analysis results or code path |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Output

Generates structured review report with:
- Executive summary
- Detailed findings by category
- Severity levels (critical, warning, info)
- Actionable recommendations

### Dependencies

All scripts require Python 3.8+ (stdlib only)
