# Implementation Orchestrator Skill

## Overview

The **Implementation Orchestrator** is a critical skill in Genesis Factory v5 that coordinates multiple specialist agents during feature implementation. It acts as the "conductor" of the agent orchestra, ensuring:

- ✅ Agents execute in the correct order (database → API → backend → frontend → UI)
- ✅ Plans across agents are coherent and consistent
- ✅ Integration points between layers are validated
- ✅ A unified implementation plan is generated

## Why This Skill Exists

### Problem It Solves

Without orchestration, specialist agents work independently and can produce **incoherent plans**:

**Example of Incoherence:**
- `database-architect` creates a `users` table with `user_id: UUID`
- `api-contract-designer` defines an API expecting `userId: string`
- `domain-logic-architect` implements logic using `user_identifier: int`

**Result**: Implementation fails at runtime due to type mismatches and naming inconsistencies.

### How It Solves It

The orchestrator:

1. **Enforces execution order** - Database changes happen before API design, API before backend, etc.
2. **Validates coherence** - Cross-references schemas, types, naming conventions across all plans
3. **Generates unified plan** - Single source of truth that synthesizes all agent plans
4. **Blocks on critical errors** - Prevents implementation if plans are incoherent

## When It's Used

### Automatic Invocation

The orchestrator is **automatically invoked** in **Phase 1.5** of `flow-feature-build.md`:

```
flow-feature-build (receives issue #42)
  ├─> Phase 1: Setup
  ├─> Phase 2: Agent Planning (database, API, backend, frontend, UI agents create plans)
  ├─> Phase 1.5: Plan Validation Gate (NEW) ← Orchestrator runs here
  │     ├─> Validates plan coherence
  │     ├─> Generates execution order
  │     ├─> Creates unified plan
  │     └─> Decides: PASS / WARNINGS / FAIL
  └─> Phase 3: Implementation (only if PASS or user approves WARNINGS)
```

### Manual Invocation

You can also manually invoke the orchestrator to validate existing plans:

```bash
# Via Claude
"Use implementation-orchestrator to validate plans in .claude/doc/user_auth/"

# Or directly via scripts
python3 .claude/skills/implementation-orchestrator/scripts/validate_plans.py \
  --feature "user_auth" \
  --plans-dir ".claude/doc/user_auth/"
```

## How It Works

### Architecture

```
┌─────────────────────────────────────┐
│   Implementation Orchestrator       │
├─────────────────────────────────────┤
│                                     │
│  Phase 1: Discovery                 │
│    - Detect available agent plans   │
│    - Build dependency graph (DAG)   │
│                                     │
│  Phase 2: Validation                │
│    - Database ↔ API coherence       │
│    - API ↔ Backend coherence        │
│    - Backend ↔ Frontend coherence   │
│    - Frontend ↔ UI coherence        │
│                                     │
│  Phase 3: Orchestration             │
│    - Generate execution order       │
│    - Define checkpoints             │
│                                     │
│  Phase 4: Unified Plan Generation   │
│    - Synthesize all plans           │
│    - Create implementation_plan.md  │
│                                     │
│  Phase 5: User Decision             │
│    - Present validation status      │
│    - Get approval to proceed        │
│                                     │
└─────────────────────────────────────┘
```

### Validation Checks

#### Database ↔ API Contract

- ✅ Field naming conventions match (snake_case in DB, camelCase in API)
- ✅ Data types are compatible (UUID → string, INT → number)
- ✅ Required fields in API exist in database
- ✅ Relationships are consistent (foreign keys match API associations)

#### API Contract ↔ Backend Logic

- ✅ All API endpoints have corresponding backend handlers
- ✅ Request/response schemas match backend data transformations
- ✅ Error codes defined in API are handled in backend
- ✅ Authentication/authorization requirements are consistent

#### Backend Logic ↔ Frontend

- ✅ Frontend calls APIs that exist in backend
- ✅ Request payloads match API contract schemas
- ✅ Frontend handles all possible API responses (success, errors)
- ✅ State management aligns with data models

#### UI Components ↔ Frontend

- ✅ All UI components referenced in frontend plan exist
- ✅ Component props match frontend data structures
- ✅ Design system conventions are consistent

### Execution Order (DAG)

The orchestrator enforces this dependency graph:

```
database-architect (Step 1: No dependencies)
    ↓
api-contract-designer (Step 2: Depends on database)
    ↓
domain-logic-architect (Step 3: Depends on API)
    ↓
presentation-layer-architect (Step 4: Depends on backend)
    ↓
ui-component-architect (Step 5: Depends on frontend)
```

See `references/dependency_graph.md` for detailed DAG documentation.

## Scripts

### 1. validate_plans.py

**Purpose**: Validates coherence across multiple agent plans

**Usage**:
```bash
python3 validate_plans.py \
  --feature "user_auth" \
  --plans-dir ".claude/doc/user_auth/" \
  --output "validation_result.json"
```

**Outputs**:
- Console report with errors and warnings
- JSON file with validation results

**Exit Codes**:
- `0` - PASS or WARNINGS
- `1` - FAIL (critical errors)

---

### 2. orchestrate.py

**Purpose**: Generates execution order for agents based on dependency graph

**Usage**:
```bash
python3 orchestrate.py \
  --feature "user_auth" \
  --plans-dir ".claude/doc/user_auth/" \
  --output "execution_plan.json"
```

**Outputs**:
- Console report with execution steps
- JSON file with ordered agent tasks

---

### 3. generate_unified_plan.py

**Purpose**: Synthesizes all agent plans into a single unified implementation plan

**Usage**:
```bash
python3 generate_unified_plan.py \
  --feature "user_auth" \
  --plans-dir ".claude/doc/user_auth/" \
  --output ".claude/doc/user_auth/implementation_plan.md"
```

**Outputs**:
- Markdown file: `implementation_plan.md`
- Includes: validation status, execution order, file changes, integration points, test strategy

**Structure of Unified Plan**:
```markdown
# Unified Implementation Plan: {feature}

1. Validation Status (PASS/WARNINGS/FAIL)
2. Execution Order (Step-by-step DAG)
3. File Changes Summary (all files to create/modify)
4. Cross-Layer Integration (how layers connect)
5. Test Strategy (tests at each layer)
6. Implementation Checkpoints (verify after each step)
7. Detailed Plans (references to agent plans)
```

## Examples

### Example 1: Full-Stack Authentication Feature

**Scenario**: User authentication with database, API, backend, and frontend

**Agent Plans Detected**:
- `database.md` - users table, sessions table
- `api_contract.md` - POST /auth/login, POST /auth/register
- `backend.md` - AuthService, JWT handling
- `frontend.md` - LoginForm, useAuth hook

**Validation Result**:
```
⚠️ WARNINGS (1 warning)

[naming] Password field in database is 'password_hash' but API uses 'password'
  Source: database.md
  Target: api_contract.md
  Note: This is acceptable - transformation happens in backend
```

**Execution Order**:
```
Step 1: database-architect → Create users and sessions tables
Step 2: api-contract-designer → Define /auth/login and /auth/register endpoints
Step 3: domain-logic-architect → Implement AuthService, hash passwords, generate JWT
Step 4: presentation-layer-architect → Build LoginForm, integrate with API
```

**User Decision**: Accept warning (it's a known transformation), proceed with implementation.

---

### Example 2: Backend-Only Notification Service

**Scenario**: Email notification service (no database or frontend changes)

**Agent Plans Detected**:
- `api_contract.md` - POST /notifications/send
- `backend.md` - EmailService, SMTP integration

**Validation Result**:
```
✅ PASS

All plans are coherent. Ready to implement.
```

**Execution Order**:
```
Step 1: api-contract-designer → Define /notifications/send endpoint
Step 2: domain-logic-architect → Implement EmailService, configure SMTP
```

**User Decision**: Proceed immediately (no issues).

---

### Example 3: Critical Error - Schema Mismatch

**Scenario**: E-commerce cart feature with type inconsistencies

**Agent Plans Detected**:
- `database.md` - cart table with `user_id: UUID`
- `api_contract.md` - GET /cart expects `userId: string`
- `backend.md` - CartService uses `user_identifier: int`

**Validation Result**:
```
❌ FAIL (2 critical errors)

[type] Database uses UUID, API uses string, Backend uses int
  Source: database.md
  Target: api_contract.md, backend.md

[naming] Field naming inconsistent (user_id vs userId vs user_identifier)
  Source: database.md
  Target: api_contract.md, backend.md
```

**User Decision**: BLOCKED - Cannot proceed. Must fix plans and re-validate.

## Integration with flow-feature-build

The orchestrator is seamlessly integrated into `flow-feature-build.md` v3.0:

### Phase 1.5: Plan Validation Gate (NEW)

```markdown
## Phase 1.5: Plan Validation Gate

1. Wait for all agents to complete their plans

2. Invoke Implementation Orchestrator:
   Use the implementation-orchestrator skill to:
   - Validate plan coherence
   - Generate unified implementation plan
   - Determine if implementation can proceed

3. Decision based on validation status:
   - PASS → Proceed to Phase 2 (Implementation)
   - WARNINGS → Ask user to review, then proceed or fix
   - FAIL → Halt, ask user to fix plans, re-validate

4. Use unified plan for implementation:
   - Read implementation_plan.md (not individual agent plans)
   - Follow execution order defined in unified plan
   - Verify checkpoints after each step
```

## Files Structure

```
.claude/skills/implementation-orchestrator/
├── SKILL.md                        # Main skill logic (Claude reads this)
├── README.md                       # This file (human documentation)
├── scripts/
│   ├── validate_plans.py           # Plan coherence validator
│   ├── orchestrate.py              # Execution order generator
│   └── generate_unified_plan.py    # Unified plan synthesizer
└── references/
    └── dependency_graph.md         # Detailed DAG documentation
```

## Benefits

### Before Orchestrator (v2.2)

- ❌ Agents worked independently
- ❌ No coherence validation
- ❌ Errors discovered late (during implementation or QA)
- ❌ Manual coordination required
- ❌ High risk of integration failures

### After Orchestrator (v3.0)

- ✅ Agents coordinated with DAG
- ✅ Coherence validated before implementation
- ✅ Errors caught early (during planning)
- ✅ Automatic coordination
- ✅ 40-60% reduction in integration errors (estimated)

## Metrics & Monitoring

The orchestrator logs metrics for analysis:

```python
# Metrics tracked
- plan_validation_time: Time to validate all plans
- coherence_warnings_count: Number of warnings detected
- coherence_errors_count: Number of errors detected
- execution_plan_generation_time: Time to generate execution order
- unified_plan_generation_time: Time to synthesize unified plan
```

Metrics are logged to `.claude/logs/orchestrator_metrics.json` for post-execution analysis.

## Troubleshooting

### Issue: "Plans directory not found"

**Cause**: The plans directory doesn't exist or path is incorrect

**Solution**: Ensure agents have completed planning phase before invoking orchestrator

---

### Issue: "No plan files detected"

**Cause**: No agent plan files (database.md, api_contract.md, etc.) exist

**Solution**: Verify that agents were successfully invoked in Phase 2 of flow-feature-build

---

### Issue: "Validation fails with type mismatches"

**Cause**: Agents used inconsistent types across layers

**Solution**:
1. Review validation errors
2. Re-invoke affected agents with explicit type guidance
3. Update CLAUDE.md with type conventions if needed

---

### Issue: "FAIL status blocks implementation"

**Cause**: Critical errors detected in plan coherence

**Solution**:
1. Review detailed error messages
2. Fix plans manually or re-invoke agents
3. Re-run orchestrator to validate fixes
4. Proceed only after achieving PASS or acceptable WARNINGS

## Version History

### v1.0.0 (2026-01-13) - Initial Release

- Cross-layer validation (database ↔ API ↔ backend ↔ frontend ↔ UI)
- DAG-based execution ordering
- Unified plan generation
- Integration with flow-feature-build Phase 1.5
- Python scripts for validation, orchestration, and plan synthesis

## References

- `SKILL.md` - Main skill logic and workflow
- `references/dependency_graph.md` - Detailed DAG documentation
- `.claude/commands/flow-feature-build.md` - Integration point (Phase 1.5)
- `CLAUDE.md` - Project constitution (see [skills_framework] section)

## Contributing

To enhance the orchestrator:

1. **Add new validation checks** - Edit `scripts/validate_plans.py`
2. **Extend dependency graph** - Update `scripts/orchestrate.py` and `references/dependency_graph.md`
3. **Improve unified plan format** - Edit `scripts/generate_unified_plan.py`
4. **Test changes** - Run scripts manually on test features
5. **Update documentation** - Keep SKILL.md and README.md in sync

---

**Status**: Production
**Maintainer**: Genesis Factory Core Team
**Last Updated**: 2026-01-13
