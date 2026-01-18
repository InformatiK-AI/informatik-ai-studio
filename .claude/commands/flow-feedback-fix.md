#

# Task: Implement Feedback Loop (v2.4 with Optimized State Passing)

# Argument: $ARGUMENT$ (e.g., PR number "123" [--state-file path] [--iteration N])

#

## Metrics Block (START)

# 1. Set START_TIME = current_timestamp
# 2. Set TASK_STATUS = "fail" (default to failure)

## Phase 0: Load State Context (v2.4 - Optimized)

**v2.4 Enhancement**: Accept pre-loaded context from flow-qa-validate to avoid redundant file reads.

1. **Parse Arguments:**
   ```
   PR_NUMBER = first argument from $ARGUMENT$

   # Check for optimized arguments (passed by flow-qa-validate v2.3+)
   IF "--state-file" in $ARGUMENT$:
     STATE_FILE = extract value after --state-file
     STATE_PASSED_DIRECTLY = true
   ELSE:
     STATE_FILE = ".claude/state/{feature_name}/validation_state.json"
     STATE_PASSED_DIRECTLY = false

   IF "--iteration" in $ARGUMENT$:
     CURRENT_ITERATION = extract value after --iteration
     ITERATION_PASSED_DIRECTLY = true
   ELSE:
     ITERATION_PASSED_DIRECTLY = false
   ```

2. **Load Iteration Context (Conditional):**
   ```
   IF ITERATION_PASSED_DIRECTLY:
     # Use passed iteration (no file read needed)
     Log: "Using passed iteration context: {CURRENT_ITERATION}"
   ELSE:
     # Fall back to reading state file
     Read STATE_FILE
     CURRENT_ITERATION = state.current_iteration
     Log: "Loaded iteration from state file: {CURRENT_ITERATION}"
   ```

3. **Load Validation History:**
   ```
   # Always read validation history for context (needed for pattern analysis)
   Read STATE_FILE (if not already loaded)
   VALIDATION_HISTORY = state.validation_history
   PR_NUMBER = state.pr_number (verify matches argument)
   ```

4. **Review Previous Attempts:**
   - Parse validation_history to understand what failed before
   - Identify patterns in failures across iterations
   - **Critical:** Do NOT repeat the same fix approach if it failed before

## Phase 1: Analysis

1.  **Get Feedback:** Read PR comments and validation reports from `/acceptance-validator` skill output and `@security-architect` agent.
2.  **Cross-Reference with History:** Compare current issues against validation_history to identify:
    - New issues (not seen before)
    - Recurring issues (need different approach)
    - Partially fixed issues (need completion)
3.  **Identify Failures:** Create actionable plan that addresses root causes (not just symptoms).

## Phase 2: Implementation Cycle (NO EXCEPTIONS)

1.  **Write Failing Test:** Invoke `@implementation-test-engineer` to reproduce the reported bug.
2.  **Run Tests (Expect Fail).**
3.  **Write Fix:** Implement code.
4.  **Run Tests (Expect Pass).**

## Phase 3: Finalize & Re-validate

1.  **Commit & Push:**
    ```
    git commit -m "fix: Address QA feedback (iteration {CURRENT_ITERATION})"
    git push
    ```

2.  **Re-trigger Validation:**
    After push completes, automatically invoke:
    ```
    claude -p .claude/commands/flow-qa-validate.md "$PR_NUMBER"
    ```

    Note: flow-qa-validate will detect this is a re-validation and increment CURRENT_ITERATION

3.  **Set Success Status:**
    Set `TASK_STATUS = "success"` (fix was implemented and committed)

## Metrics Block (END)

# Set END_TIME = current_timestamp
# Call: python3 .claude/scripts/log_metric.py with:
#   - command: "flow-feedback-fix"
#   - pr_number: $PR_NUMBER
#   - iteration: CURRENT_ITERATION
#   - status: TASK_STATUS
#   - start_time: START_TIME
#   - end_time: END_TIME

## Rules

- NO EXCEPTIONS: A new test for the bug is required.
- Address root causes, not symptoms (especially on iteration 2+).
- Always re-trigger validation after fix is committed.

## Notes

**Version**: 2.4.0
**Last Updated**: 2026-01-17

**Changes from v2.3**:
- Optimized state passing from flow-qa-validate (accepts --state-file and --iteration args)
- Reduced redundant file reads by accepting pre-loaded context
- Updated argument parsing for backward compatibility

**Changes from v2.2**:
- Added Phase 0: Load State File for iteration context
- State file is now single source of truth (no more PR comment parsing)
- Cross-reference with validation_history to avoid repeating failed approaches
- Enhanced iteration tracking with persistent state
- Removed --iteration flag from argument (read from state file instead)

**Changes from v2.1**:
- Added CURRENT_ITERATION tracking
- Added automatic re-validation after fix is committed
- Enhanced Phase 1 to review previous iteration attempts
- Added explicit metrics block with iteration tracking
