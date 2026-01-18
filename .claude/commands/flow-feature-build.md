#

# Task: Dynamic Task Executor (v3.3 Complete - Modular Architecture)

# Modular Components:
# - flow-feature-tdd.md: TDD workflow (Strategy → Red → Green → Refactor)
# - flow-feature-rad.md: RAD workflow (Prototype → Analyze → Iterate → Test)
# - flow-worktree-recovery.md: Git worktree conflict recovery

# Argument: $ARGUMENT$ (e.g., Issue number)

#

## Metrics Block (START)

# 1. Set START_TIME = current_timestamp
# 2. Set TASK_STATUS = "fail" (default to failure)
# 3. Set PREFLIGHT_RETRY_COUNT = 0
# 4. Set MAX_PREFLIGHT_RETRIES = 3
# 5. Set AGENT_TIMEOUT_MS = 300000 (5 minutes per agent)
# 6. Set EXTERNAL_CALL_TIMEOUT_MS = 120000 (2 minutes for external calls)

## Phase 0: Pre-Flight Check (v3.3 - With Retry Loop)

**Purpose**: Validate project readiness before implementation begins. Catches common issues early.

### Timeout Configuration

All external calls in this flow use these timeout values:
- **Agent invocations**: 300000ms (5 minutes)
- **VCS CLI operations**: 120000ms (2 minutes)
- **CI/CD pipeline checks**: 600000ms (10 minutes)
- **Skill invocations**: 180000ms (3 minutes)

### Pre-Flight Check Loop

```
WHILE PREFLIGHT_RETRY_COUNT < MAX_PREFLIGHT_RETRIES:
```

1. **Invoke Pre-Flight Check Skill (with timeout)**
   ```
   Run /preflight-check skill with:
   - timeout: 180000ms
   - validate:
     - Context file exists and is complete
     - Required agents are available
     - CLAUDE.md is valid and has all sections
     - Git working tree status (no conflicts)
     - Dependencies installed
     - Test framework configured
   ```

2. **Analyze Pre-Flight Results**

   The skill returns one of three statuses:

   **✅ GO**: All checks passed
   - Action: `BREAK` loop, proceed to Phase 0.5

   **⚠️ GO WITH WARNINGS**: Minor issues detected
   - Action: Show warnings to user
   - Ask user: "Proceed despite warnings? (y/n)"
   - If user approves: `BREAK` loop, proceed to Phase 0.5
   - If user declines: Abort with guidance

   **❌ NO-GO**: Critical errors detected
   - Action: Attempt auto-remediation
   - `PREFLIGHT_RETRY_COUNT += 1`

   **NO-GO Auto-Remediation (v3.3 Enhancement):**

   a) **Analyze failure type:**
      - If "dependencies missing" → Run `/dependency-installer` skill
      - If "CLAUDE.md incomplete" → Run `/claude-md-architect audit`
      - If "git conflicts" → Show manual resolution steps
      - If "agents unavailable" → Run `@agent-librarian scout`

   b) **Execute remediation:**
      ```
      IF failure_type == "dependencies":
        Run /dependency-installer with timeout: 300000ms
      ELSE IF failure_type == "claude_md":
        Run /claude-md-architect audit with timeout: 180000ms
      ELSE IF failure_type == "agents":
        Run @agent-librarian "scout: {missing_agents}" with timeout: 300000ms
      ELSE:
        # Cannot auto-remediate
        Show detailed error with manual fix instructions
        Ask user: "Fix manually and retry? (y/n)"
        IF user declines: ABORT with status "preflight_failed"
      ```

   c) **Retry pre-flight check** (loop continues)

3. **Max Retries Exceeded**
   ```
   IF PREFLIGHT_RETRY_COUNT >= MAX_PREFLIGHT_RETRIES:
     Log error: "Pre-flight check failed after {MAX_PREFLIGHT_RETRIES} attempts"
     Show summary of all failures
     Set TASK_STATUS = "preflight_failed"
     ABORT with escalation message
   ```

4. **Log Pre-Flight Metrics**
   ```
   python3 .claude/scripts/log_metric.py with:
   - preflight_status: GO/WARNINGS/NO-GO
   - preflight_retry_count: PREFLIGHT_RETRY_COUNT
   - warnings_count: number of warnings
   - errors_count: number of errors
   - remediation_actions: list of auto-remediation attempts
   ```

## Phase 0.5: Load Shared Context (NEW in v3.1, Enhanced v3.5)

**Purpose**: Load project context once and cache it for all agents to eliminate redundant file reads.

1. **Generate Shared Context**
   ```
   python3 .claude/scripts/load_context.py \
     --feature "$FEATURE_NAME" \
     --output ".claude/cache/context_$FEATURE_NAME.json"
   ```

   This creates a cached JSON containing:
   - CLAUDE.md parsed sections (stack, methodology, core_team)
   - Feature context session file
   - All agent plans (if available)
   - Metadata (version, last_updated, status)

2. **Modular Architecture Support (Enhanced v3.5 - JSON Index Priority)**

   **IMPORTANT (v3.5 change)**: Prefer JSON index over parsing CLAUDE.md for reliability.

   ```
   # Check for machine-readable modular index first
   IF .claude/cache/modular_index.json exists:
     MODULAR_INDEX = JSON.parse(".claude/cache/modular_index.json")
     IS_MODULAR = true
     USE_JSON_INDEX = true
     Log: "Using modular_index.json for context loading"

   ELSE IF .claude/rules/ directory exists AND contains .md files:
     IS_MODULAR = true
     USE_JSON_INDEX = false
     Log: "Falling back to directory scan (modular_index.json not found)"

   ELSE:
     IS_MODULAR = false
   ```

   **If IS_MODULAR == true:**

   a) **Auto-load global rules (JSON index preferred):**
   ```
   IF USE_JSON_INDEX:
     For each item in MODULAR_INDEX.auto_loaded:
       Load item.file into context.rules.global[filename]
       Log: "Loaded rule: {item.file} (priority: {item.priority})"
   ELSE:
     # Fallback: scan directory
     For each file in .claude/rules/*.md (excluding domain/):
       Load file content into context.rules.global[filename]
   ```

   b) **Load path-specific rules based on feature (JSON index preferred):**
   ```
   # Analyze feature to determine affected paths
   AFFECTED_PATHS = analyze_feature_paths($FEATURE_NAME)

   IF USE_JSON_INDEX:
     For each item in MODULAR_INDEX.path_specific:
       For each pattern in item.paths:
         IF any AFFECTED_PATH matches pattern:
           Load item.file into context.rules.domain[filename]
           Log: "Loaded domain rule: {item.file} for paths: {matched_paths}"
   ELSE:
     # Fallback: scan domain directory and parse frontmatter
     For each file in .claude/rules/domain/:
       Parse YAML frontmatter for 'paths'
       For each pattern in paths:
         IF any AFFECTED_PATH matches pattern:
           Load file into context.rules.domain[filename]
   ```

   c) **Reference on-demand docs in context (JSON index preferred):**
   ```
   IF USE_JSON_INDEX:
     context.docs_index = MODULAR_INDEX.on_demand
     Log: "Indexed {on_demand.length} on-demand docs from modular_index.json"
   ELSE:
     # Fallback: parse [modular_index] from CLAUDE.md
     context.docs_index = parse_modular_index(CLAUDE.md)
     Log: "Parsed docs index from CLAUDE.md [modular_index] section"

   # Don't load docs yet - just index for reference
   # Agents will request specific docs when needed
   ```

   d) **Validate checksums (optional, JSON index only):**
   ```
   IF USE_JSON_INDEX AND MODULAR_INDEX.validation.checksums exists:
     CHECKSUM_ERRORS = []
     For each item in [...auto_loaded, ...path_specific]:
       IF item.checksum exists:
         current_checksum = sha256(read_file(item.file))
         IF current_checksum != item.checksum:
           CHECKSUM_ERRORS.append(item.file)

     IF CHECKSUM_ERRORS not empty:
       Log WARNING: "Files changed since modular_index.json was generated:"
       For each file in CHECKSUM_ERRORS:
         Log: "  - {file}"
       Log: "Consider running flow-md-architect to regenerate index"
   ```

3. **Benefits**
   - Reduces I/O: 6-8 file reads → 1 read
   - Ensures consistency: All agents use same context version
   - Faster agent execution: No repeated file parsing
   - **Modular**: Only loads relevant domain rules for feature
   - **v3.5**: JSON index provides reliable, structured access

4. **Agent Usage**
   - Agents receive path to cached context JSON
   - Load context with: `context = json.load(open(context_path))`
   - Access sections: `context['constitution']['stack']['framework']`
   - **Access rules**: `context['rules']['global']['code-standards']`
   - **Access domain rules**: `context['rules']['domain']['api-rules']` (if loaded)
   - **Request docs**: Agent can request docs from `context['docs_index']`

**IMPORTANT**: This phase is MANDATORY (v3.3 change). All agents MUST use the cached context JSON to ensure consistency and reduce redundant file reads.

## Phase 1: Constitution & Setup (Enhanced with Worktree Recovery)

1.  **Read Constitution:** `CLAUDE.md` (or load from shared context cache).

2.  **Worktree Creation with Recovery Logic:**

   **Modular Reference**: See `flow-worktree-recovery.md` for detailed recovery implementation.

   **Attempt worktree creation:**
   ```
   git worktree add ./.trees/feature-$ARG -b feature-$ARG
   ```

   **If worktree creation fails (already exists):**

   a) **Detect existing worktree:**
      ```
      git worktree list | grep ".trees/feature-$ARG"
      ```

   b) **Analyze worktree state:**
      - Check last commit date: `git -C ./.trees/feature-$ARG log -1 --format="%ar"`
      - Check for uncommitted changes: `git -C ./.trees/feature-$ARG status --porcelain`
      - Check branch status: `git -C ./.trees/feature-$ARG status -sb`

   c) **Present recovery options to user:**
      ```
      ⚠️ Worktree already exists: .trees/feature-{ARG}

      Worktree Info:
      - Last commit: {LAST_COMMIT_TIME}
      - Uncommitted changes: {CHANGES_COUNT} files
      - Branch: {BRANCH_NAME}

      Recovery Options:
      a) Delete and recreate (FRESH START - will lose uncommitted work)
      b) Continue in existing worktree (RESUME - keep existing work)
      c) Abort command (EXIT - manual cleanup)

      Choose option (a/b/c):
      ```

   d) **Handle user choice:**

      **Option a: Delete and recreate**
      ```bash
      # Remove worktree (force if needed)
      git worktree remove ./.trees/feature-$ARG --force

      # Delete branch if exists
      git branch -D feature-$ARG 2>/dev/null || true

      # Create fresh worktree
      git worktree add ./.trees/feature-$ARG -b feature-$ARG

      # Log action
      echo "Worktree recreated from scratch"
      ```

      **Option b: Continue in existing**
      ```bash
      # Change to existing worktree
      cd ./.trees/feature-$ARG

      # Show status
      git status

      # Warn user about existing state
      echo "⚠️ Continuing with existing worktree. Review uncommitted changes."

      # Log action
      echo "Resumed existing worktree"
      ```

      **Option c: Abort**
      ```bash
      # Exit flow-feature-build
      echo "Command aborted. Clean up manually with:"
      echo "  git worktree remove ./.trees/feature-$ARG"
      echo "  git branch -D feature-$ARG"
      exit 1
      ```

   e) **Log recovery action:**
      ```
      python3 .claude/scripts/log_metric.py with:
      - worktree_recovery_action: "recreated" / "resumed" / "aborted"
      - worktree_path: ".trees/feature-$ARG"
      ```

3.  **Analyze Task:** Read issue details and docs.

## Phase 2: Dynamic Implementation Cycle (Enhanced with Agent Selection)

Check `[methodology].workflow` from CLAUDE.md to determine implementation approach.

### CASE 1: Test-Driven Development (TDD)

**Workflow**: Strategy → Red → Green → Refactor

**Modular Reference**: See `flow-feature-tdd.md` for detailed TDD workflow implementation.

if `WORKFLOW == "TDD"`:

0. **Strategy Phase - Test Planning (v3.3 - dag.json compliance)**
   - Invoke `@test-strategy-planner` agent with timeout: 300000ms
   - Input: Feature requirements, CLAUDE.md, cached context JSON
   - Output: `test_cases.md` with Gherkin scenarios and test strategy
   - **GATE**: Must produce `test_cases.md` before Red Phase begins

1. **Red Phase - Write Failing Test**
   - Invoke `@implementation-test-engineer` agent with timeout: 300000ms
   - Input: `test_cases.md` from Strategy Phase (REQUIRED per dag.json)
   - Agent writes a failing test that captures the desired behavior
   - Run tests to confirm they fail (red)

2. **Green Phase - Implement Minimum Code**
   - Invoke architecture team based on feature requirements:
   - **Use dag.json feature_patterns for invocation order**

   **Backend/API changes** (sequential per dag.json layers):
   - Layer 1: Invoke `@database-architect` if database changes needed (timeout: 300000ms)
   - Layer 2: Invoke `@api-contract-designer` if API endpoints/contracts involved (timeout: 300000ms)
   - Layer 3: Invoke `@domain-logic-architect` for business logic design (timeout: 300000ms)

   **Frontend/UI changes**:
   - Invoke `@frontend-architect` for component architecture and UI components (timeout: 300000ms)

   **Full-stack changes** (v3.3 - PARALLEL invocation per dag.json):
   ```
   # Layer 1: Database (sequential)
   Invoke @database-architect (timeout: 300000ms)
   WAIT for database.md

   # Layer 2: API Contract (sequential)
   Invoke @api-contract-designer (timeout: 300000ms)
   WAIT for api_contract.md

   # Layer 3: Backend + Frontend (PARALLEL - same layer in dag.json)
   PARALLEL_INVOKE:
     - @domain-logic-architect (timeout: 300000ms)
     - @frontend-architect (timeout: 300000ms)
   WAIT for ALL: backend.md, frontend.md

   # Layer 4: Security (converge point - MANDATORY)
   Invoke @security-architect (timeout: 300000ms)
   WAIT for security_plan.md
   ```

   **Benefits of parallel invocation:**
   - Reduces total execution time by ~40% for fullstack features
   - domain-logic-architect and frontend-architect are independent (both depend on api_contract.md)
   - Both converge at security-architect gate

3. **Verify Tests Pass**
   - Implement the code following architect plans
   - Run tests to confirm they pass (green)
   - Invoke `@implementation-test-engineer` to verify test coverage

4. **Refactor Phase**
   - Improve code quality while keeping tests passing
   - Run tests continuously during refactoring

### CASE 2: Rapid Application Development (RAD) - Structured Cycles

**Workflow**: Prototype → Analyze → Iterate (max 3 cycles) → Test Last

**Modular Reference**: See `flow-feature-rad.md` for detailed RAD workflow implementation.

else if `WORKFLOW == "RAD"`:

**Setup**:
- Set `MAX_RAD_ITERATIONS = 3` (prevents infinite iteration)
- Set `CURRENT_ITERATION = 1`

**Iteration Cycle** (repeat up to 3 times):

**Iteration 1: Minimal Viable Prototype**

1. **Prototype Phase**
   - Implement core functionality quickly (no UI polish, no edge cases)
   - Focus on "happy path" only
   - Invoke architecture team for guidance (non-blocking):
     - `@domain-logic-architect` (if backend work)
     - `@frontend-architect` (if frontend work)
     - `@database-architect` (if data model changes)

2. **Analysis Phase**
   - Invoke `@experience-analyzer` to analyze the prototype:
     - **If UI-heavy project**: Analyze UX with Playwright (hierarchy, flow, accessibility)
     - **If API-heavy project**: Analyze DX with curl (error messages, consistency)
   - Generate `experience_analysis_iteration_1.md` with findings

3. **Decision Point**
   - Review analysis results
   - Identify **critical issues** (blocking UX/DX problems)
   - If critical issues found → Proceed to Iteration 2
   - If no critical issues → Skip to Testing Phase (Iteration 1 is good enough)

---

**Iteration 2: Refinement** (only if critical issues found)

1. **Refinement Phase**
   - Address **critical issues** from Iteration 1 analysis
   - Examples:
     - UX: Fix navigation flow, improve accessibility, clarify error messages
     - DX: Improve API error responses, add missing validation, fix status codes
   - Do NOT add new features, only improve existing ones

2. **Re-Analysis Phase**
   - Re-invoke `@experience-analyzer` on refined prototype
   - Generate `experience_analysis_iteration_2.md`
   - Compare with Iteration 1 results (improvement delta)

3. **Decision Point**
   - Review improvement from Iteration 1 → Iteration 2
   - If significant improvement AND remaining issues → Proceed to Iteration 3
   - If good enough → Skip to Testing Phase

---

**Iteration 3: Polish** (optional, only if needed)

1. **Polish Phase**
   - Address **nice-to-have improvements** from Iteration 2
   - Examples:
     - UX: Loading states, animations, micro-interactions
     - DX: Better documentation, helpful examples, consistent naming
   - Focus on quality-of-life enhancements

2. **Final Analysis**
   - Final `@experience-analyzer` check
   - Generate `experience_analysis_iteration_3.md`
   - Document final state

3. **Iteration Limit Reached**
   - Log: "RAD workflow reached max iterations (3)"
   - Proceed to Testing Phase regardless of results

---

**Testing Phase (After Iterations Complete)**

1. **Comprehensive Testing**
   - Invoke `@implementation-test-engineer` to write full test suite
   - Tests cover all iterations (Iteration 1 core + Iteration 2/3 refinements)
   - Ensure test coverage meets requirements

2. **Final Verification**
   - Run all tests
   - Generate test coverage report
   - Document test strategy in `test_cases.md`

**RAD Cycle Summary**:
- Minimum: 1 iteration (if prototype is good)
- Maximum: 3 iterations (enforced limit)
- Each iteration has clear objective: MVP → Refinement → Polish
- Experience analysis after each iteration guides next steps

### CASE 3: Standard Development

**Workflow**: Implement + Test Concurrently

else (Standard):

1. **Planning Phase**
   - Invoke planning team based on feature scope:

   **If database changes needed**:
   - Invoke `@database-architect` for schema design first

   **If API contracts needed**:
   - Invoke `@api-contract-designer` for API design first

   **Then invoke implementation architects**:
   - `@domain-logic-architect` (for backend logic)
   - `@frontend-architect` (for frontend structure and UI components)

2. **Implementation Phase**
   - Implement feature following architect plans
   - Write tests alongside implementation

3. **Verification Phase**
   - Invoke `@implementation-test-engineer` to ensure test quality
   - Verify test coverage meets standards

### Agent Selection Decision Tree

**Step 1: Determine Feature Scope**

Does the feature involve...
- Database schema changes? → Invoke `@database-architect`
- New API endpoints? → Invoke `@api-contract-designer`
- Backend business logic? → Invoke `@domain-logic-architect`
- Frontend components? → Invoke `@frontend-architect`
- Infrastructure/deployment? → Invoke `@devops-architect`

**Step 2: Invoke Required Agents**

Typical agent combinations:
- **Backend-only feature**: database-architect → domain-logic-architect → api-contract-designer
- **Frontend-only feature**: frontend-architect
- **Full-stack feature**: database-architect → api-contract-designer → domain-logic-architect → frontend-architect
- **Infrastructure feature**: devops-architect

**Step 3: Always Include (MANDATORY)**

Regardless of workflow, these agents **MUST** be invoked:

- `@security-architect` - **MANDATORY GATE** (blocks approval if not invoked)
  - Reviews all plans for security vulnerabilities (OWASP Top 10)
  - Must approve before implementation proceeds
  - Produces `security_plan.md`

- `@implementation-test-engineer` - **REQUIRED** (ensures tests are written)
  - Cannot skip in any workflow
  - TDD: Invoked first (red phase)
  - RAD/Standard: Invoked after implementation

**Security Gate Enforcement:**
- If `security_plan.md` does not exist → **BLOCK** Phase 1.5 validation
- If security review has unresolved CRITICAL issues → **BLOCK** implementation
- Security review is NOT optional, even for "quick fixes"

### Special Considerations

**If specialist agent missing**:
- Invoke `@agent-librarian` in "scout" mode to find or draft specialist
- Log warning and continue with available agents
- Flag for later architectural review

## Phase 1.5: Plan Validation Gate (NEW in v3.0)

**Purpose**: Validate coherence across all agent plans before implementation begins.

This phase prevents incoherent implementations by catching errors early.

### Phase 1.5a: Plan Existence Validation (v3.2 Enhancement)

**CRITICAL**: Before checking coherence, verify all required plans exist.

1. **Build Expected Plans List:**
   Based on agents invoked in Phase 2, build list of expected plan files:
   ```
   EXPECTED_PLANS = ["security_plan.md"]  # ALWAYS required (mandatory gate)

   IF @database-architect invoked: EXPECTED_PLANS.append("database.md")
   IF @api-contract-designer invoked: EXPECTED_PLANS.append("api_contract.md")
   IF @domain-logic-architect invoked: EXPECTED_PLANS.append("backend.md")
   IF @frontend-architect invoked: EXPECTED_PLANS.append("frontend.md")
   IF @devops-architect invoked: EXPECTED_PLANS.append("devops.md")
   ```

   **Note:** `security_plan.md` is ALWAYS in the expected list because `@security-architect` is mandatory.

2. **Check Plan Files Exist:**
   ```
   For each plan in EXPECTED_PLANS:
     Check if .claude/docs/{feature_name}/{plan} exists
     If missing: Add to MISSING_PLANS list
   ```

3. **Handle Missing Plans:**
   - If `MISSING_PLANS` is not empty:
     - **HALT** execution
     - Display error: "Missing required plans: {MISSING_PLANS}"
     - Suggest: "Re-invoke agents or check agent invocation logs"
     - Cannot proceed until all plans exist

4. **Proceed to Coherence Check:**
   - Only if all expected plans exist
   - Continue to step 1 below

### Phase 1.5b: Plan Coherence Validation

1. **Wait for All Agents to Complete**
   - Ensure all invoked agents have generated their plan files:
     - `database.md` (if `@database-architect` was invoked)
     - `api_contract.md` (if `@api-contract-designer` was invoked)
     - `backend.md` (if `@domain-logic-architect` was invoked)
     - `frontend.md` (if `@frontend-architect` was invoked)

2. **Invoke Implementation Orchestrator Skill**
   ```
   Use the implementation-orchestrator skill to:
   - Validate plan coherence across all layers
   - Generate execution order (DAG)
   - Create unified implementation plan
   ```

   The orchestrator will:
   - Check database ↔ API contract coherence (types, naming, schemas)
   - Check API contract ↔ backend coherence (endpoints, handlers, schemas)
   - Check backend ↔ frontend coherence (API calls, state management)
   - Check frontend ↔ UI components coherence (component usage, props)
   - Generate execution order respecting dependencies
   - Synthesize all plans into `implementation_plan.md`

3. **Analyze Validation Status**

   The orchestrator returns one of three statuses:

   **✅ PASS**: All plans are coherent, no issues detected
   - Action: Proceed directly to Phase 2 (Implementation)

   **⚠️ WARNINGS**: Minor inconsistencies detected (e.g., naming convention differences)
   - Action: Show warnings to user
   - Ask user: "Continue with warnings, Fix plans, or Abort?"
   - If user approves: Proceed to Phase 2
   - If user requests fix: Re-invoke affected agents, then re-validate

   **❌ FAIL**: Critical errors detected (e.g., type mismatches, missing endpoints)
   - Action: BLOCK implementation
   - Show detailed error messages
   - Ask user to: "Fix plans manually or re-invoke agents with corrected guidance"
   - MUST re-validate before proceeding
   - Cannot continue to Phase 2 with FAIL status

4. **Use Unified Implementation Plan**

   If validation passes (PASS or approved WARNINGS):
   - Read `implementation_plan.md` as the authoritative guide
   - Follow the execution order defined in unified plan
   - Implement changes layer by layer (database → API → backend → frontend → UI)
   - Verify checkpoints after each layer

5. **Log Validation Metrics**
   ```
   python3 .claude/scripts/log_metric.py with:
   - validation_status: PASS/WARNINGS/FAIL
   - validation_time: duration
   - warnings_count: number of warnings
   - errors_count: number of errors
   ```

## Phase 3: Validation Loop

1.  **Pre-PR Code Review (v3.3 Enhancement - Deduplicated):**
    - Invoke `/code-reviewer analyze` skill on modified files with timeout: 180000ms
    - Review checklist includes:
      - Code quality and best practices
      - Performance anti-patterns
      - Accessibility issues (if frontend)
      - Test coverage verification
      - Documentation completeness

    **NOTE (v3.3 deduplication)**: Security vulnerabilities (OWASP Top 10) are NOT checked here.
    Security review is handled exclusively by `@security-architect` in Phase 2 to avoid duplication.
    The separation of concerns:
    - `@security-architect` (Phase 2): Reviews PLANS for security vulnerabilities
    - `/code-reviewer` (Phase 3): Reviews CODE for quality issues
    - `@security-architect` (flow-qa-validate): Reviews IMPLEMENTATION in validation mode

    - If critical issues found: Fix before proceeding to PR
    - If warnings only: Document in PR description

2.  **Create PR:** Use `$VCS_CLI`.
3.  **CI/CD:** Monitor pipeline.
4.  **QA Validation:** Invoke `flow-qa-validate` command.
5.  **Feedback:** If validation fails, invoke `flow-feedback-fix` command.

---

## Appendix A: Standardized Invocation Syntax (v3.3)

**IMPORTANT**: All flow commands MUST use consistent syntax for agent and skill invocations.

### Agent Invocation Syntax

Use `@agent-name` prefix for all agent invocations:

```
# Correct syntax:
Invoke @database-architect with timeout: 300000ms
Invoke @security-architect in validation mode
Invoke @implementation-test-engineer with input: test_cases.md

# Incorrect (do NOT use):
Invoke database-architect agent...
Run the database architect...
Call @database-architect agent...
```

### Skill Invocation Syntax

Use `/skill-name` prefix for all skill invocations:

```
# Correct syntax:
Run /preflight-check skill
Run /acceptance-validator validate {feature_name}
Run /code-reviewer analyze with timeout: 180000ms
Run /brainstorming skill with SCOPE: feature

# Incorrect (do NOT use):
Invoke acceptance-validator skill...
Run acceptance-validator validate...
Use the preflight-check skill...
```

### Timeout Specification

Always include timeout for external calls:

```
# Correct:
Run /skill-name with timeout: 180000ms
Invoke @agent-name with timeout: 300000ms

# Default timeouts:
- Agent invocations: 300000ms (5 minutes)
- Skill invocations: 180000ms (3 minutes)
- VCS CLI operations: 120000ms (2 minutes)
- CI/CD checks: 600000ms (10 minutes)
```

### Flow Command References

Use `flow-*` prefix for command invocations:

```
# Correct:
Invoke flow-qa-validate command
Invoke flow-feedback-fix command

# Incorrect:
Run qa-validate...
Invoke the QA validation flow...
```

---

## Appendix B: State File Locations (v3.3)

Standardized file locations for consistency:

| Type | Location | Purpose |
|------|----------|---------|
| Session context | `.claude/sessions/context_session_{scope}_{name}.md` | Ephemeral planning context |
| Validation state | `.claude/state/{feature_name}/validation_state.json` | Persistent iteration tracking |
| Cached context | `.claude/cache/context_{feature_name}.json` | Cached CLAUDE.md + plans |
| Agent plans | `.claude/docs/{feature_name}/*.md` | Generated architecture plans |
| Logs | `.claude/logs/` | Metric logs and audit trails |

---

## Metrics Block (END)

# 1. Set END_TIME = current_timestamp
# 2. If task completed successfully, set TASK_STATUS = "success"
# 3. Call `python3 .claude/scripts/log_metric.py` silently with:
#    - command: "flow-feature-build"
#    - feature: $FEATURE_NAME
#    - workflow: $WORKFLOW (TDD/RAD/Standard)
#    - status: $TASK_STATUS
#    - agents_used: list of invoked agents
#    - preflight_retries: $PREFLIGHT_RETRY_COUNT
#    - start_time: $START_TIME
#    - end_time: $END_TIME

**Version**: 3.5.0
**Last Updated**: 2026-01-17
**Changes from v3.4**:
- Phase 0.5 now prefers `.claude/cache/modular_index.json` over parsing CLAUDE.md
- JSON index provides reliable, structured access to modular rules and docs
- Added checksum validation for detecting changed files since index generation
- Graceful fallback to directory scan if JSON index not found
- Improved logging for modular context loading

**Changes from v3.3**:
- Enhanced Phase 0.5 with modular architecture support
- Auto-loads global rules from .claude/rules/
- Loads path-specific domain rules based on feature paths
- Indexes on-demand docs from [modular_index]
- Agents can access rules via context.rules.global/domain

**Changes from v3.2**:
- Added Phase 0 retry loop with auto-remediation
- Made Phase 0.5 context cache mandatory
- Added test-strategy-planner to TDD workflow
- Enabled parallel agent invocation for fullstack features
- Created modular workflow files (TDD, RAD, worktree recovery)
- Added standardized invocation syntax (Appendix A)
- Standardized state file locations (Appendix B)
- Added timeout configuration for all external calls
