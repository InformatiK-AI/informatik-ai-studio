#

# Task: Analyze Bug (v2.1 with Metrics)

# Argument: $ARGUMENT$ (e.g., Bug description)

#

## Metrics Block (START)

# 1. Set START_TIME = current_timestamp
# 2. Set TASK_STATUS = "fail" (default to failure)
# 3. Set BUG_ID = extracted from $ARGUMENT$

## Phase 0.5: Load Diagnostic Context

**Purpose**: Provide rule context for bug analysis.

1. **Detect Modular Architecture:**
   ```
   IF .claude/cache/modular_index.json exists:
     MODULAR_INDEX = JSON.parse(".claude/cache/modular_index.json")
     IS_MODULAR = true
   ELSE IF .claude/rules/ directory exists:
     IS_MODULAR = true (fallback mode)
   ELSE:
     IS_MODULAR = false (skip context loading)
   ```

2. **Load Diagnostic Rules:**
   ```
   IF IS_MODULAR:
     # Always load for bug analysis
     Load security-policy.md (security vulnerabilities)
     Load code-standards.md (code quality issues)

     # If bug location is known from $ARGUMENT$
     BUG_LOCATION = extract_file_paths_from($ARGUMENT$)
     # e.g., "error in api/users endpoint" → "app/api/**"

     IF BUG_LOCATION is specified AND MODULAR_INDEX exists:
       For each item in MODULAR_INDEX.path_specific:
         IF BUG_LOCATION matches item.paths:
           Load item.file
           Log: "Loaded domain rule for diagnosis: {item.file}"
   ```

3. **Provide to Diagnostic Agents:**
   ```
   DIAGNOSTIC_CONTEXT = {
     security_policy: content of security-policy.md,
     code_standards: content of code-standards.md,
     domain_rules: [loaded path-specific rules]
   }

   Agents use context for:
   - Identifying violations of code standards
   - Detecting security policy breaches
   - Domain-specific pattern violations
   ```

## Phase 1: Setup

Create `.claude/sessions/context_session_bug_{ID}.md`.

## Phase 2: Team Selection (Auto-Healing)

1.  Analyze keywords (e.g., "performance").
2.  **Check for Specialist:**
    - If specialist exists: Add to team.
    - Else: Invoke `claude @agent-librarian "scout: $specialist"`. (Halt task if new agent needed).

## Phase 3: Diagnosis

Use agents to investigate.
Synthesize findings into `.claude/doc/bug_{ID}/bug_diagnosis_report.md`.

- Root Cause
- Evidence
- Recommendation

## Phase 4: Recommendation

Present report to the user. Ask to create a fix issue.

## Metrics Block (END)

# 1. Set END_TIME = current_timestamp
# 2. If task completed successfully, set TASK_STATUS = "success"
# 3. Call `python3 .claude/scripts/log_metric.py` silently with:
#    - command: "flow-analyze-bug"
#    - bug_id: $BUG_ID
#    - status: $TASK_STATUS
#    - agents_used: list of invoked agents
#    - root_cause_found: true/false
#    - start_time: $START_TIME
#    - end_time: $END_TIME

**Version**: 2.3.0
**Last Updated**: 2026-01-17
**Changes from v2.2.0**:
- Added Phase 0.5: Load Diagnostic Context
- Bug analysis agents now receive rule context (security-policy, code-standards)
- Path-specific rules loaded when bug location is identifiable
- Graceful fallback for non-modular projects
