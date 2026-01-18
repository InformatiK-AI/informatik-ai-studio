# Scripts Documentation

This directory contains executable scripts for the **dependency-installer** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `install_dependencies.py` | Auto-detect and install project dependencies | Production |

---

## install_dependencies.py

**Purpose:** Automated dependency installation across multiple languages and package managers. Detects package manager from lock files and runs appropriate install commands.

### Usage

```bash
python3 install_dependencies.py [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--force` | No | Force reinstall even if already installed |
| `--skip-audit` | No | Skip security audit after installation |
| `--dev` | No | Include development dependencies |
| `--help` | No | Show help message |

### Supported Package Managers

| Language | Package Managers | Lock Files |
|----------|-----------------|------------|
| Node.js | npm, pnpm, yarn, bun | package-lock.json, pnpm-lock.yaml, yarn.lock, bun.lockb |
| Python | pip, poetry, pipenv | requirements.txt, poetry.lock, Pipfile.lock |
| Ruby | bundler | Gemfile.lock |
| Rust | cargo | Cargo.lock |
| Go | go mod | go.sum |
| PHP | composer | composer.lock |

### Detection Order

1. Checks for lock files in project root
2. Falls back to manifest files (package.json, requirements.txt, etc.)
3. Defaults to most common package manager for language

### Output

```
⏳ Detecting package manager...
✅ Detected: pnpm (Node.js)

⏳ Installing dependencies...
✅ Dependencies installed successfully

⏳ Running security audit...
✅ No vulnerabilities found
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Dependencies installed successfully |
| `1` | Installation failed |

### Dependencies

- Python 3.8+ (stdlib only)
- Requires the detected package manager to be installed
