#

# Task: Dynamic QA Validator (v2.1 with Metrics)

# Argument: $ARGUMENT$ (e.g., Issue number or PR number)

#

## Metrics Block (START)

# Set START_TIME = current_timestamp
# Set TASK_STATUS = "fail" (default to failure)
# Set MAX_ITERATIONS = 3 (maximum validation-fix cycles)
# Set CURRENT_ITERATION = 1 (initialize iteration counter)

## Phase 1: Setup

Read `CLAUDE.md`. Get PR details.

### Modular Architecture Support (NEW in v2.4)

If project uses modular architecture:

1. **Detect and load rules:**
   ```
   IS_MODULAR = false
   IF .claude/rules/ directory exists:
     IS_MODULAR = true

   IF IS_MODULAR:
     # Load all global rules for validation reference
     VALIDATION_RULES = {}
     For each file in .claude/rules/*.md:
       VALIDATION_RULES[filename] = parse(file)

     # Load path-specific rules for modified files
     MODIFIED_FILES = get_pr_modified_files($ARGUMENT$)
     For each file in .claude/rules/domain/:
       Parse YAML frontmatter for 'paths'
       IF any MODIFIED_FILE matches paths:
         VALIDATION_RULES[filename] = parse(file)
   ```

2. **Use rules in validation:**
   - Code reviewer validates against `code-standards.md`
   - Security architect validates against `security-policy.md`
   - Acceptance validator validates against `testing-policy.md`
   - Domain-specific rules validate relevant files

**State File Management (v2.2 Enhancement):**

1. **Determine State File Path:**
   ```
   STATE_FILE = ".claude/docs/{feature_name}/validation_state.json"
   ```

2. **Load or Initialize State:**
   - If state file exists: Load current state
     ```json
     {
       "feature_name": "{feature}",
       "pr_number": 123,
       "current_iteration": 2,
       "max_iterations": 3,
       "status": "in_progress",
       "validation_history": [
         {"iteration": 1, "status": "failed", "timestamp": "...", "issues": [...]}
       ]
     }
     ```
   - If state file does not exist: Initialize from template
     ```
     Copy .claude/templates/validation_state.template.json
     Set feature_name, pr_number, created_at
     ```

3. **Extract Iteration Context:**
   - CURRENT_ITERATION = state.current_iteration
   - MAX_ITERATIONS = state.max_iterations (default: 3)
   - If CURRENT_ITERATION > MAX_ITERATIONS: Escalate immediately

## Phase 2: Orchestrate Validation (Sequential + Parallel)

**Per DEPENDENCY_GRAPH.md**: code-reviewer MUST run before acceptance-validator.

### Step 1: Code Review (MANDATORY - Pre-merge gate)

Run `/code-reviewer analyze` skill on modified files:
```
Run /code-reviewer analyze with:
- pr_number: $ARGUMENT$
- timeout: 180000ms
- review_checklist:
  - Code quality and best practices
  - Performance anti-patterns
  - Accessibility issues (if frontend)
  - Documentation completeness
```

**Note**: Security review is handled by `@security-architect` to avoid duplication (see issue 4.1.2 deduplication).

### Step 2: Parallel Validation (After code review passes)

1.  **Invoke Acceptance Validator:** Run `/acceptance-validator validate {feature_name}` skill on the task/PR with timeout: 180000ms.
2.  **Invoke Security Validator:** Run `@security-architect` agent in validation mode on the task/PR with timeout: 300000ms.

These two validations run in parallel after code review completes.

## Phase 3: Review & Decision

1.  **Analyze Feedback:** Read comments from agents.
2.  **Make Decision:**
    - If comments contain `[FAIL]` or `[NEEDS WORK]`: `FINAL_STATUS = "NEEDS_WORK"`.
    - Else: `FINAL_STATUS = "READY"`.

## Phase 4: Action (Enhanced with Iteration Limits)

# CASE 1: Ready to Merge

if `FINAL_STATUS == "READY"`:
  Post comment to PR: "✅ QA VALIDATION PASSED - READY TO MERGE (Iteration {CURRENT_ITERATION}/{MAX_ITERATIONS})"
  Set `TASK_STATUS = "success"`.

  **Update State File:**
  ```json
  {
    "status": "passed",
    "current_iteration": CURRENT_ITERATION,
    "validation_history": [..., {"iteration": N, "status": "passed", "timestamp": "..."}],
    "updated_at": "..."
  }
  ```

  Log metrics with iteration_count = CURRENT_ITERATION

# CASE 2: Needs Work (Within Iteration Limit)

else if `FINAL_STATUS == "NEEDS_WORK"` AND `CURRENT_ITERATION < MAX_ITERATIONS`:
  Post comment to PR: "⚠️ QA VALIDATION FAILED - Triggering feedback loop (Iteration {CURRENT_ITERATION}/{MAX_ITERATIONS})"

  **Update State File:**
  ```json
  {
    "status": "in_progress",
    "current_iteration": CURRENT_ITERATION + 1,
    "validation_history": [..., {"iteration": N, "status": "failed", "timestamp": "...", "issues": [...]}],
    "updated_at": "..."
  }
  ```

  **Optimized Invocation (v2.3 Enhancement):**
  Pass state file path as argument to avoid redundant file reads:
  ```
  Invoke flow-feedback-fix command with:
  - PR_NUMBER: $ARGUMENT$
  - STATE_FILE: $STATE_FILE
  - CURRENT_ITERATION: state.current_iteration + 1
  ```

  Actual invocation:
  ```
  claude -p .claude/commands/flow-feedback-fix.md "$ARGUMENT$ --state-file $STATE_FILE --iteration {NEXT_ITERATION}"
  ```

  **Benefits (v2.3):**
  - Eliminates redundant state file read (was: read in qa-validate, read again in feedback-fix)
  - Passes iteration context directly, reducing I/O
  - State file is still single source of truth, but context is cached in memory during handoff

# CASE 3: Escalate to Human Review (Max Iterations Reached)

else if `FINAL_STATUS == "NEEDS_WORK"` AND `CURRENT_ITERATION >= MAX_ITERATIONS`:

  **Step 1: Post PR Comment**
  Post comment to PR: "🚨 ESCALATE TO HUMAN REVIEW - Max validation attempts ({MAX_ITERATIONS}) reached"

  **Step 2: Generate Structured Escalation Report (v2.3 Enhancement)**

  Generate escalation report with structured data:
  ```markdown
  ## Escalation Report: PR #{PR_NUMBER}

  ### Summary
  - Feature: {FEATURE_NAME}
  - Validation attempts: {CURRENT_ITERATION}/{MAX_ITERATIONS}
  - Status: ESCALATED TO HUMAN REVIEW

  ### Iteration History
  | Iteration | Status | Issues Found | Issues Fixed |
  |-----------|--------|--------------|--------------|
  | 1         | failed | [list]       | N/A          |
  | 2         | failed | [list]       | [partial]    |
  | 3         | failed | [list]       | [partial]    |

  ### Persistent Issues (Not Resolved)
  [List issues that appeared in multiple iterations]

  ### Root Cause Analysis
  [Automated analysis of why issues persist]

  ### Recommended Actions
  1. [Specific recommendation based on issue pattern]
  2. [Architectural review if structural issues]
  3. [Manual code review for complex logic]

  ### Labels
  - `needs-human-review`
  - `qa-escalated`
  - `priority: high`
  ```

  **Step 3: Create Escalation Issue (v2.3 Enhancement)**
  ```bash
  # Create GitHub issue for tracking escalated PRs
  gh issue create \
    --title "QA Escalation: PR #{PR_NUMBER} - {FEATURE_NAME}" \
    --body "{ESCALATION_REPORT}" \
    --label "needs-human-review,qa-escalated,priority-high"

  # Link issue to PR
  gh pr comment {PR_NUMBER} --body "Escalation issue created: #{ISSUE_NUMBER}"
  ```

  **Step 4: Update State File**
  ```json
  {
    "status": "escalated",
    "escalation_issue": ISSUE_NUMBER,
    "escalation_reason": "max_iterations_reached",
    "persistent_issues": [...],
    "validation_history": [..., {"iteration": N, "status": "escalated", "timestamp": "...", "issues": [...]}],
    "updated_at": "..."
  }
  ```

  **Step 5: Notify and Log**
  Set `TASK_STATUS = "escalated"`.

  Log structured metrics:
  ```
  python3 .claude/scripts/log_metric.py with:
  - status: "escalated"
  - iteration_count: CURRENT_ITERATION
  - persistent_issues_count: N
  - escalation_issue_number: ISSUE_NUMBER
  - escalation_reason: "max_iterations_reached"
  ```

  Notify user:
  ```
  🚨 This PR requires human review.

  The automated validation-fix cycle has reached its limit ({MAX_ITERATIONS} attempts).
  An escalation issue has been created: #{ISSUE_NUMBER}

  Persistent issues that could not be automatically resolved:
  [List top 3 persistent issues]

  Recommended next steps:
  1. Review the escalation issue for full analysis
  2. Consider architectural changes if issues are structural
  3. Schedule a code review session
  ```

## Metrics Block (END)

# Set END_TIME = current_timestamp
# Call: python3 .claude/scripts/log_metric.py with:
#   - command: "flow-qa-validate"
#   - argument: $ARGUMENT$
#   - status: TASK_STATUS ("success", "escalated", or "fail")
#   - iteration_count: CURRENT_ITERATION
#   - max_iterations: MAX_ITERATIONS
#   - start_time: START_TIME
#   - end_time: END_TIME

## Notes

**Version**: 2.4.0
**Last Updated**: 2026-01-17

**Changes from v2.3**:
- Added modular architecture support in Phase 1
- Loads global rules from .claude/rules/ for validation
- Loads path-specific rules based on modified files
- Validators use rules files for consistent enforcement

**Changes from v2.2**:
- Added code-reviewer before acceptance-validator (per DEPENDENCY_GRAPH.md)
- Added structured escalation with GitHub issue creation
- Optimized iteration counter passing to flow-feedback-fix
- Added timeout configuration for all external calls

**Changes from v2.1**:
- Added MAX_ITERATIONS limit (default: 3 attempts)
- Added CURRENT_ITERATION tracking across validation cycles
- Added escalation logic when max iterations reached
- Enhanced metrics to track iteration count
- Added clear status indicators in PR comments (✅ ⚠️ 🚨)
