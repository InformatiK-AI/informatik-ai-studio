# Scripts Documentation

This directory contains executable scripts for the **implementation-orchestrator** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `validate_plans.py` | Validate coherence across agent plans | Production |
| `orchestrate.py` | Generate agent execution order (DAG) | Production |
| `generate_unified_plan.py` | Synthesize unified implementation plan | Production |

---

## validate_plans.py

**Purpose:** Validates consistency across multiple agent plans (database, API, backend, frontend, UI). Detects mismatches in naming conventions, types, schemas, and integration points.

### Usage

```bash
python3 validate_plans.py --feature "feature_name" --plans-dir ".claude/doc/feature_name/" [--output "report.json"]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--feature` | Yes | - | Feature name for reporting |
| `--plans-dir` | Yes | - | Directory containing plan files |
| `--output` | No | - | Output file for JSON validation report |

### Plan Files Processed

The script looks for these files in the plans directory:
- `database.md` - Database schema and migrations
- `api_contract.md` - API endpoint definitions
- `backend.md` - Backend business logic
- `frontend.md` - Frontend implementation
- `ui_components.md` - UI component library

### Validation Checks

1. **Database ↔ API Contract**
   - Field naming conventions (snake_case vs camelCase)
   - Data type compatibility (UUID vs string, int vs number)
   - Required fields alignment

2. **API Contract ↔ Backend**
   - All API endpoints have backend handlers
   - Request/response schemas match
   - Error codes are handled

3. **Backend ↔ Frontend**
   - Frontend calls existing API endpoints
   - Request payloads match API contracts
   - Error handling coverage

4. **Frontend ↔ UI Components**
   - All referenced UI components are defined
   - Component props match data structures

### Output

**Console:**
```
============================================================
Plan Validation Report: user_auth
============================================================

Status: WARNINGS
Errors: 0
Warnings: 1

⚠️  WARNINGS:
  [naming] Naming convention mismatch: DB uses 'created_at', API should use 'createdAt' (camelCase)
    Source: database.md
    Target: api_contract.md
```

**JSON Report:**
```json
{
  "feature": "user_auth",
  "status": "WARNINGS",
  "error_count": 0,
  "warning_count": 1,
  "errors": [],
  "warnings": [
    {
      "severity": "warning",
      "category": "naming",
      "message": "Naming convention mismatch...",
      "source_file": "database.md",
      "target_file": "api_contract.md"
    }
  ]
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | PASS or WARNINGS - can proceed |
| `1` | FAIL - critical errors found |

---

## orchestrate.py

**Purpose:** Generates agent execution order based on dependency graph (DAG). Ensures agents are invoked in correct sequence: database → API → backend → frontend → UI.

### Usage

```bash
python3 orchestrate.py --feature "feature_name" --plans-dir ".claude/doc/feature_name/" [--output "execution_plan.json"]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--feature` | Yes | - | Feature name |
| `--plans-dir` | Yes | - | Directory containing plan files |
| `--output` | No | - | Output file for JSON execution plan |

### Dependency Graph

```
database-architect
       ↓
api-contract-designer
       ↓
domain-logic-architect
       ↓
presentation-layer-architect
       ↓
ui-component-architect
```

### Output

**Console:**
```
============================================================
Agent Execution Plan
============================================================

Step 1: database-architect
  Plan: database.md
  Description: Create database schema and migrations
  Dependencies: None
  Checkpoint: Run migrations, verify schema with database inspection

Step 2: api-contract-designer
  Plan: api_contract.md
  Description: Define API contracts (OpenAPI/GraphQL schemas)
  Dependencies: database-architect
  Checkpoint: Validate contract syntax, generate API documentation

[...]

Total steps: 4
============================================================
```

**JSON Output:**
```json
{
  "feature": "user_auth",
  "steps": [
    {
      "step_number": 1,
      "agent": "database-architect",
      "plan_file": "database.md",
      "dependencies": [],
      "description": "Create database schema and migrations",
      "checkpoint": "Run migrations, verify schema with database inspection"
    }
  ]
}
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Execution plan generated successfully |
| `1` | Error (plans directory not found) |

---

## generate_unified_plan.py

**Purpose:** Synthesizes multiple agent plans into a single unified implementation plan. Integrates validation results, execution order, file changes, and test strategy.

### Usage

```bash
python3 generate_unified_plan.py --feature "feature_name" \
    --plans-dir ".claude/doc/feature_name/" \
    --output ".claude/doc/feature_name/implementation_plan.md"
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--feature` | Yes | Feature name |
| `--plans-dir` | Yes | Directory containing plan files |
| `--output` | Yes | Output file for unified plan (Markdown) |

### Process

1. **Load Plans** - Reads all available plan files
2. **Run Validation** - Invokes `validate_plans.py`
3. **Run Orchestration** - Invokes `orchestrate.py`
4. **Generate Plan** - Synthesizes unified markdown document

### Output

Generates a comprehensive Markdown document with:

1. **Validation Status** - PASS/WARNINGS/FAIL with details
2. **Execution Order** - Step-by-step agent sequence
3. **File Changes Summary** - All files to create/modify
4. **Cross-Layer Integration** - How layers connect
5. **Test Strategy** - Tests required at each layer
6. **Implementation Checkpoints** - Verification steps
7. **Detailed Plans** - References to source plans

### Example

```bash
# Generate unified plan for user authentication feature
python3 generate_unified_plan.py \
    --feature "user_authentication" \
    --plans-dir ".claude/doc/user_authentication/" \
    --output ".claude/doc/user_authentication/implementation_plan.md"
```

Output:
```
Loading agent plans...
Running validation...
Running orchestration...
Generating unified plan...

✅ Unified implementation plan generated: .claude/doc/user_authentication/implementation_plan.md
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Unified plan generated successfully |
| `1` | Error (plans directory not found) |

### Dependencies

- Requires `validate_plans.py` in same directory
- Requires `orchestrate.py` in same directory
- Python 3.8+ standard library only
