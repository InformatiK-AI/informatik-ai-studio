# Scripts Documentation

This directory contains executable scripts for the **senior-backend** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `api_scaffolder.py` | Generate API endpoint scaffolds | Production |
| `database_migration_tool.py` | Manage database migrations | Production |
| `api_load_tester.py` | Load test API endpoints | Production |

---

## api_scaffolder.py

**Purpose:** Generates REST or GraphQL API endpoint scaffolds with proper structure, validation, and error handling.

### Usage

```bash
python3 api_scaffolder.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | API endpoint name or path |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output directory |

### Generated Files

- Route/handler definitions
- Request/response schemas
- Validation middleware
- Unit test scaffolds
- OpenAPI documentation

---

## database_migration_tool.py

**Purpose:** Manages database migrations including generation, execution, rollback, and status checking.

### Usage

```bash
python3 database_migration_tool.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Migration name or command |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Supported Operations

- Generate new migration
- Run pending migrations
- Rollback last migration
- Check migration status
- Generate migration from schema diff

---

## api_load_tester.py

**Purpose:** Performs load testing on API endpoints to measure performance, identify bottlenecks, and validate scalability.

### Usage

```bash
python3 api_load_tester.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | API endpoint URL or config file |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Metrics Reported

- Requests per second
- Response time percentiles (p50, p95, p99)
- Error rates
- Throughput analysis

### Dependencies

All scripts require Python 3.8+ (stdlib only)
