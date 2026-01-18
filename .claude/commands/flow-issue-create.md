#

# Task: Create New VCS Task for Feature

# This command is now agnostic and reads CLAUDE.md

#

## Input

Feature Plan: $ARGUMENTS (Path to context_session.md)

## Metrics Block (START)

# Set START_TIME = current_timestamp

# Set TASK_STATUS = "fail" (default to failure)

# Extract FEATURE_NAME from context_session filename

## Phase 0.5: Validate Session File (NEW in v2.2)

**Purpose**: Ensure session file from flow-plan exists before proceeding.

1. **Parse $ARGUMENTS to get SESSION_FILE path:**

   ```
   SESSION_FILE = $ARGUMENTS

   # If no argument provided, search for recent session files
   IF SESSION_FILE is empty:
     Search .claude/sessions/ for context_session_*.md files
     IF multiple found:
       List files and ask user to choose
     ELSE IF one found:
       SESSION_FILE = found file
     ELSE:
       ERROR: "No session file found. Run /flow-plan first."
       Set TASK_STATUS = "fail_no_session"
       EXIT
   ```

2. **Validate SESSION_FILE exists:**

   ```
   IF SESSION_FILE does not exist:
     ERROR: "Session file not found: {SESSION_FILE}

     Run /flow-plan first to create the session file.

     Example: /flow-plan feature user_authentication"

     Set TASK_STATUS = "fail_no_session"
     EXIT
   ```

3. **Load session file content:**

   ```
   SESSION_CONTENT = Read(SESSION_FILE)

   # Extract FEATURE_NAME from session file
   # Parse the Metadata section for Plan Name
   FEATURE_NAME = extract_plan_name(SESSION_CONTENT)

   Log: "Loaded session file: {SESSION_FILE}"
   Log: "Feature name: {FEATURE_NAME}"
   ```

4. **Validate session file has required sections:**

   ```
   REQUIRED_SECTIONS = ["Metadata", "Summary", "Implementation Plan"]

   FOR each section in REQUIRED_SECTIONS:
     IF section not found in SESSION_CONTENT:
       WARNING: "Session file missing section: {section}"

   IF "Implementation Plan" section is empty or contains placeholder:
     WARNING: "Implementation plan not completed. Consider re-running /flow-plan."
   ```

**GATE**: Cannot proceed to Phase 1 if session file validation fails.

## Phase 1: Constitution & Setup

1.  **Read the Constitution:** Read `CLAUDE.md`.
2.  **VCS Tool Setup:** Identify `VCS_CLI` (`gh` or `glab`).

## Phase 1.5: Load Modular Context

**Purpose**: Provide rule context to test strategy and acceptance criteria agents.

1. **Detect Modular Architecture:**

   ```
   IF .claude/cache/modular_index.json exists:
     MODULAR_INDEX = JSON.parse(".claude/cache/modular_index.json")
     IS_MODULAR = true
   ELSE IF .claude/rules/ directory exists:
     IS_MODULAR = true (fallback mode - scan files directly)
   ELSE:
     IS_MODULAR = false (legacy monolithic mode)
   ```

2. **Load Relevant Rules:**

   ```
   IF IS_MODULAR:
     # Always load for issue creation
     Load testing-policy.md (required for test strategy)
     Load code-standards.md (for code quality expectations)
     Load security-policy.md (for security-sensitive features)

     # Analyze feature to determine path-specific rules
     FEATURE_PATHS = infer_paths_from_feature_name($ARGUMENTS)
     # e.g., "add api endpoint" → likely matches "app/api/**"
     # e.g., "create user dashboard" → likely matches "components/**"

     IF MODULAR_INDEX exists:
       For each item in MODULAR_INDEX.path_specific:
         IF FEATURE_PATHS matches item.paths:
           Load item.file
           Log: "Loaded path-specific rule: {item.file}"
   ```

3. **Pass Context to Agents:**

   ```
   RULE_CONTEXT = {
     testing_policy: content of testing-policy.md,
     code_standards: content of code-standards.md,
     security_policy: content of security-policy.md,
     domain_rules: [loaded path-specific rules]
   }

   @test-strategy-planner receives:
     - RULE_CONTEXT.testing_policy
     - RULE_CONTEXT.domain_rules

   /acceptance-validator receives:
     - Full RULE_CONTEXT
     - Used for AC validation alignment
   ```

## Phase 2: Generate Test Strategy & Acceptance Criteria (AGENT + SKILL DRIVEN)

**IMPORTANT:** This phase uses specialized agents and skills to ensure professional-quality issues.

1. **Invoke `@test-strategy-planner` agent:** Generate `test_cases.md` (Gherkin).
2. **Invoke `/acceptance-validator define {feature_name}` skill:** Refine into `acceptance_criteria.md` (Gherkin).

## Phase 3: Draft GitHub Issue

Create an issue/task body with this **professional structure**:

### User Story

As a [role], I want [feature], So that [benefit].

### Acceptance Criteria (Gherkin)

(Copy from `acceptance_criteria.md`)

### Definition of Done

- [ ] Implementation complete
- [ ] Tests passed (NO EXCEPTIONS)
- [ ] QA Validation passed

## Phase 4: Review

Show the user the draft issue. Wait for approval before creating.

## Phase 5: Create Task

Run `$VCS_CLI issue create --title "$TITLE" --body "$BODY"`.

If issue created successfully:

- Extract ISSUE_NUMBER from output
- Post success message: "✅ Issue #{ISSUE_NUMBER} created successfully"
- Set `TASK_STATUS = "success"`

## Metrics Block (END)

# Set END_TIME = current_timestamp

# Call: python3 .claude/scripts/log_metric.py with:

# - command: "flow-issue-create"

# - feature_name: FEATURE_NAME

# - issue_number: ISSUE_NUMBER (if created)

# - vcs_tool: VCS_CLI

# - status: TASK_STATUS

# - start_time: START_TIME

# - end_time: END_TIME

## Notes

**Version**: 2.2 (with session file validation)
**Changes from v2.1**:

- Added Phase 0.5: Validate Session File
- Session file from flow-plan is now validated before proceeding
- Auto-detection of session files when no argument provided
- Validates required sections exist in session file
- Clear error messages guide users to run /flow-plan first

**Changes from v2.0**:

- Added Phase 1.5: Load Modular Context
- Test strategy and acceptance criteria agents now receive rule context
- Path-specific rules loaded based on feature name analysis
- Graceful fallback for monolithic projects

**Changes from v1.x**:

- Added explicit metrics blocks (START and END)
- Track feature name, issue number, and VCS tool used
- Consistent with metrics tracking across other commands
- Removed hard-coded "Daniel" reference (changed to "Show the user")
