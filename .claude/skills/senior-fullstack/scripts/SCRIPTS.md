# Scripts Documentation

This directory contains executable scripts for the **senior-fullstack** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `project_scaffolder.py` | Scaffold full-stack projects | Production |
| `code_quality_analyzer.py` | Analyze full-stack code quality | Production |
| `fullstack_scaffolder.py` | Generate full-stack feature scaffolds | Production |

---

## project_scaffolder.py

**Purpose:** Scaffolds complete full-stack project structures with frontend, backend, database, and deployment configurations.

### Usage

```bash
python3 project_scaffolder.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Project name or path |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output directory |

### Scaffolded Structure

```
project/
├── frontend/     # React/Next.js application
├── backend/      # Node.js/Express API
├── database/     # Migrations and seeds
├── docker/       # Container configurations
└── docs/         # Documentation
```

---

## code_quality_analyzer.py

**Purpose:** Analyzes code quality across both frontend and backend codebases, ensuring consistent standards.

### Usage

```bash
python3 code_quality_analyzer.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Project path to analyze |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Analysis Includes

- Code complexity metrics
- Test coverage analysis
- Dependency health
- Security vulnerability scan
- Performance patterns

---

## fullstack_scaffolder.py

**Purpose:** Generates coordinated frontend and backend code for new features, ensuring API contracts match.

### Usage

```bash
python3 fullstack_scaffolder.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Feature name |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output directory |

### Generated Files

- Backend API endpoint
- Frontend API client
- Database migration
- TypeScript types (shared)
- Test scaffolds

### Dependencies

All scripts require Python 3.8+ (stdlib only)
