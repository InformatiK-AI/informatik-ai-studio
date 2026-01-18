---
name: implementation-orchestrator
description: |
  Coordinates multiple specialist agents during feature implementation to ensure coherent, well-integrated plans. Acts as the "conductor" of the agent orchestra, managing execution order, validating cross-agent coherence (database ↔ API ↔ backend ↔ frontend), and generating unified implementation plans. Automatically invoked during flow-feature-build Phase 1.5 (Plan Validation Gate).
version: 1.0.0
---

# Implementation Orchestrator

## Purpose

Coordinates multiple specialist agents during feature implementation to ensure coherent, well-integrated plans. This skill acts as the "conductor" of the agent orchestra, managing execution order, validating cross-agent coherence, and generating unified implementation plans.

## When to Use This Skill

This skill is **automatically invoked** by `flow-feature-build.md` during Phase 1.5 (Plan Validation Gate). It should be used when:

- Multiple specialist agents are involved (2+ agents)
- Full-stack features require database, API, backend, and frontend coordination
- Cross-layer consistency is critical (e.g., DB schema matching API contracts)
- Complex features with multiple architectural layers

**Manual Invocation:**
You can also invoke this skill manually to validate existing plans:

```
"Use implementation-orchestrator to validate plans in .claude/docs/{feature_name}/"
```

## Workflow

### Phase 1: Discovery & Agent Detection

1. **Read Feature Context:**
   - Read `context_session_feature_{FEATURE_NAME}.md` to understand feature scope
   - Identify which architectural layers are affected (database, API, backend, frontend, UI)

2. **Detect Agent Plans:**
   - Scan `.claude/docs/{FEATURE_NAME}/` directory for existing plans:
     - `database.md` → database-architect was invoked
     - `api_contract.md` → api-contract-designer was invoked
     - `backend.md` → domain-logic-architect was invoked
     - `frontend.md` → presentation-layer-architect was invoked
     - `ui_components.md` → ui-component-architect was invoked

3. **Build Dependency Graph:**
   - Create execution order based on detected plans (see `references/dependency_graph.md`)
   - Standard order: database → API → backend → frontend → UI

### Phase 2: Coherence Validation

1. **Invoke Validation Script:**

   ```python
   python3 .claude/skills/implementation-orchestrator/scripts/validate_plans.py \
     --feature "{FEATURE_NAME}" \
     --plans-dir ".claude/docs/{FEATURE_NAME}/"
   ```

2. **Cross-Reference Validation Checks:**

   **Database ↔ API Contract:**
   - Extract field names from `database.md` (tables, columns, data types)
   - Extract schemas from `api_contract.md` (request/response models)
   - Validate:
     - ✅ Field naming conventions match (snake_case vs camelCase)
     - ✅ Data types are compatible (UUID vs string, int vs number)
     - ✅ Required fields in API exist in database
     - ✅ Relationships are consistent (foreign keys match API associations)

   **API Contract ↔ Backend Logic:**
   - Extract endpoints from `api_contract.md` (paths, methods, schemas)
   - Extract implementation plan from `backend.md` (services, handlers, routes)
   - Validate:
     - ✅ All API endpoints have corresponding backend handlers
     - ✅ Request/response schemas match backend data transformations
     - ✅ Error codes defined in API are handled in backend
     - ✅ Authentication/authorization requirements are consistent

   **Backend Logic ↔ Frontend:**
   - Extract API client calls from `frontend.md` (fetch calls, mutations, queries)
   - Cross-reference with `api_contract.md` endpoints
   - Validate:
     - ✅ Frontend calls APIs that exist in contract
     - ✅ Request payloads match API contract schemas
     - ✅ Frontend handles all possible API responses (success, errors)
     - ✅ State management aligns with data models

   **UI Components ↔ Frontend:**
   - Extract component hierarchy from `ui_components.md`
   - Cross-reference with `frontend.md` component usage
   - Validate:
     - ✅ All UI components referenced in frontend plan exist
     - ✅ Component props match frontend data structures
     - ✅ Design system conventions are consistent

3. **Generate Validation Report:**
   - If validations pass → `validation_status = "PASS"`
   - If warnings found → `validation_status = "WARNINGS"` (show list of warnings)
   - If critical errors found → `validation_status = "FAIL"` (block implementation)

### Phase 3: Orchestration & Execution Order

1. **Invoke Orchestration Script:**

   ```python
   python3 .claude/skills/implementation-orchestrator/scripts/orchestrate.py \
     --feature "{FEATURE_NAME}" \
     --plans-dir ".claude/docs/{FEATURE_NAME}/"
   ```

2. **Define Execution Order (DAG):**

   Based on detected plans, build execution sequence:

   ```
   Step 1: Database Changes (if database.md exists)
     - Create migrations
     - Update schema
     - Add indexes

   Step 2: API Contract (if api_contract.md exists)
     - Define OpenAPI/GraphQL schemas
     - Generate API documentation

   Step 3: Backend Implementation (if backend.md exists)
     - Implement business logic
     - Create API handlers/routes
     - Add data access layer

   Step 4: Frontend Integration (if frontend.md exists)
     - Create API client
     - Implement state management
     - Add page/component logic

   Step 5: UI Components (if ui_components.md exists)
     - Build component library
     - Integrate with frontend
   ```

3. **Generate Execution Checkpoints:**
   - Each step includes verification checkpoint:
     - Database: Run migrations, verify schema
     - API: Validate contract, generate docs
     - Backend: Run unit tests, verify API responses
     - Frontend: Run integration tests
     - UI: Run component tests, visual regression

### Phase 4: Unified Plan Generation

1. **Invoke Plan Generation Script:**

   ```python
   python3 .claude/skills/implementation-orchestrator/scripts/generate_unified_plan.py \
     --feature "{FEATURE_NAME}" \
     --plans-dir ".claude/docs/{FEATURE_NAME}/" \
     --output ".claude/docs/{FEATURE_NAME}/implementation_plan.md"
   ```

2. **Synthesize Master Plan:**

   The unified plan includes:

   ```markdown
   # Unified Implementation Plan: {FEATURE_NAME}

   ## Validation Status

   [PASS/WARNINGS/FAIL with details]

   ## Execution Order (DAG)

   [Step-by-step sequence with dependencies]

   ## File Changes Summary

   [All files to create/modify across all layers]

   ## Cross-Layer Integration Points

   [How database connects to API, API to backend, backend to frontend]

   ## Test Strategy

   [Tests required at each layer, integration tests]

   ## Implementation Checkpoints

   [Verification steps after each phase]

   ## Warnings & Recommendations

   [Any coherence warnings or best practice suggestions]
   ```

3. **Save Unified Plan:**

   **Primary Method (Script-Based):**
   - The `generate_unified_plan.py` script (invoked in Step 1) writes the file automatically
   - Output path: `.claude/docs/{FEATURE_NAME}/implementation_plan.md`
   - Verify the file was created successfully

   **Fallback (If Script Missing or Fails):**
   - If the script doesn't exist or fails, use the Write tool to create the file manually
   - Use the template structure from Step 2 above
   - **CRITICAL**: Do NOT skip this step - the unified plan file MUST exist for implementation to proceed

   **Result:**
   - The unified plan becomes the authoritative guide for implementation
   - Downstream commands (flow-feature-build) depend on this file existing

### Phase 5: User Decision

1. **Present Results to User:**

   Show validation status:
   - ✅ **PASS**: "All plans are coherent. Ready to implement."
   - ⚠️ **WARNINGS**: "Plans have {N} warnings. Review recommended before implementation."
   - ❌ **FAIL**: "Plans have critical errors. Cannot proceed with implementation."

2. **For WARNINGS or FAIL:**

   Ask user:

   ```
   Options:
   a) Fix plans and re-validate
   b) Continue with warnings (not recommended for FAIL)
   c) Abort implementation
   ```

3. **User Choice Handling:**
   - **Fix plans**: Re-invoke affected agents to address issues
   - **Continue**: Proceed to implementation (log warning acceptance)
   - **Abort**: Exit flow-feature-build, allow manual review

## Examples

### Example 1: Full-Stack Feature (All Agents)

**Scenario:** User authentication feature involving database, API, backend, frontend

**Detected Plans:**

- `database.md` (users table, sessions table)
- `api_contract.md` (POST /auth/login, POST /auth/register)
- `backend.md` (AuthService, JWT handling)
- `frontend.md` (LoginForm, useAuth hook)

**Validation:**

- ✅ Users table fields match API request schemas
- ✅ JWT token format consistent across API contract and backend
- ⚠️ Warning: Password field in database is `password_hash` but API uses `password` (acceptable, transformation in backend)
- ✅ Frontend LoginForm sends correct payload to POST /auth/login

**Result:** WARNINGS (1 warning, acceptable)

**Unified Plan:**

```
Step 1: Database - Create users and sessions tables
Step 2: API - Define /auth/login and /auth/register endpoints
Step 3: Backend - Implement AuthService, hash passwords, generate JWT
Step 4: Frontend - Build LoginForm, integrate with API
```

---

### Example 2: Backend-Only Feature (Subset of Agents)

**Scenario:** Email notification service (no database or frontend changes)

**Detected Plans:**

- `api_contract.md` (POST /notifications/send)
- `backend.md` (EmailService, SMTP integration)

**Validation:**

- ✅ API endpoint matches backend EmailService handler
- ✅ Request schema (to, subject, body) matches backend implementation

**Result:** PASS

**Unified Plan:**

```
Step 1: API - Define /notifications/send endpoint
Step 2: Backend - Implement EmailService, configure SMTP
```

---

### Example 3: Critical Error (Incoherent Plans)

**Scenario:** E-commerce cart feature with schema mismatch

**Detected Plans:**

- `database.md` (cart table with `user_id: UUID`)
- `api_contract.md` (GET /cart expects `userId: string` in query params)
- `backend.md` (CartService uses `user_identifier: int`)

**Validation:**

- ❌ FAIL: Database uses UUID, API uses string, Backend uses int
- ❌ FAIL: Field naming inconsistent (user_id vs userId vs user_identifier)

**Result:** FAIL (Critical errors, cannot proceed)

**Action:** Block implementation, show errors to user, suggest re-invoking agents with explicit type/naming guidance

---

## Integration with flow-feature-build

The orchestrator is invoked in **Phase 1.5: Plan Validation Gate** of `flow-feature-build.md`:

```markdown
## Phase 1.5: Plan Validation Gate (NEW in v3.0)

1. **Wait for all agents to complete their plans**

2. **Invoke Implementation Orchestrator:**
   Use the implementation-orchestrator skill to:
   - Validate plan coherence
   - Generate unified implementation plan
   - Determine if implementation can proceed

3. **Decision based on validation status:**
   - PASS → Proceed to Phase 2 (Implementation)
   - WARNINGS → Ask user to review, then proceed or fix
   - FAIL → Halt, ask user to fix plans, re-validate

4. **Use unified plan for implementation:**
   - Read implementation_plan.md (not individual agent plans)
   - Follow execution order defined in unified plan
   - Verify checkpoints after each step
```

## Rules

1. **Always validate before implementation** - Never skip validation gate
2. **Respect execution order (DAG)** - Database before API before Backend before Frontend
3. **Block on critical errors** - FAIL status must halt implementation
4. **Log all validations** - Record validation results for metrics
5. **Generate unified plan** - Single source of truth for implementation
6. **User approval required** - For WARNINGS, get explicit user consent to proceed

## References

- `references/dependency_graph.md` - Detailed DAG documentation
- `.claude/scripts/validate_plans.py` - Plan coherence validation logic
- `.claude/scripts/orchestrate.py` - Agent execution orchestration
- `.claude/scripts/generate_unified_plan.py` - Master plan synthesis

## Version

**Current Version:** 1.0.0
**Last Updated:** 2026-01-13
**Status:** Production

## Changelog

### v1.0.0 (2026-01-13)

- Initial implementation
- Cross-layer validation (database ↔ API ↔ backend ↔ frontend)
- DAG-based execution ordering
- Unified plan generation
- Integration with flow-feature-build Phase 1.5
