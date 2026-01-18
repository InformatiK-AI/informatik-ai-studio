#

# Task: Strategic Planner (v3.3.0 - Multi-Scope: Feature/Epic/Project)

# Version: 3.3.0
# Last Updated: 2026-01-17
# Changes:
# - v3.3.0: CRITICAL FIX - Added explicit termination, prohibited plan mode tools, skills run in planning-only mode
# - v3.2.0: Phase 2 now prefers modular_index.json over parsing CLAUDE.md
# - v3.1.0: Added modular architecture support in Phase 2 (Constitution)
# - v3.0.0: Added brainstorming (Phase 0.5), writing-plans (Phase 4), DAG integration, error recovery
# - v2.4.0: Added DAG-integrated team selection
# - v2.3.0: Added error recovery for missing agents
# - v2.2.0: Added hybrid model for team selection

## CRITICAL CONSTRAINTS - READ FIRST

**This command is for PLANNING ONLY. It must NEVER:**
1. Write any production code
2. Create project files (except plan/session documents)
3. Use `EnterPlanMode` or `ExitPlanMode` tools (these are Claude Code native tools that trigger implementation)
4. Offer to implement the plan after completion
5. Call skills with implementation handoff enabled

**Expected Output:** A plan document saved to SESSION_FILE. Nothing more.

**After Completion:** The user must manually run `/flow-issue-create` and then `/flow-feature-build` to implement.

# Argument: $ARGUMENTS ([scope] name)
# - scope: Optional. One of: feature, epic, project. Defaults to feature.
# - name: Required. Name of the feature/epic/project to plan.

#

## Metrics Block (START)

# 1. Set START_TIME = current_timestamp

# 2. Set TASK_STATUS = "fail"

<user_request>
#$ARGUMENTS
</user_request>

## Phase 0: Scope Detection & Argument Parsing

Parse $ARGUMENTS to determine scope and plan name:

1. **Extract first word** from $ARGUMENTS
2. **Check if first word is scope keyword:**
   - If first word is "feature" → Set SCOPE = "feature", PLAN_NAME = rest of arguments
   - If first word is "epic" → Set SCOPE = "epic", PLAN_NAME = rest of arguments
   - If first word is "project" → Set SCOPE = "project", PLAN_NAME = rest of arguments
   - **Else** (no scope keyword) → Set SCOPE = "feature" (default), PLAN_NAME = full $ARGUMENTS

3. **Normalize PLAN_NAME:**
   - Convert to lowercase
   - Replace spaces with underscores
   - Example: "Authentication System" → "authentication_system"

4. **Set SESSION_FILE variable:**
   - If SCOPE == "feature" → SESSION_FILE = `.claude/sessions/context_session_feature_{PLAN_NAME}.md`
   - If SCOPE == "epic" → SESSION_FILE = `.claude/sessions/context_session_epic_{PLAN_NAME}.md`
   - If SCOPE == "project" → SESSION_FILE = `.claude/sessions/context_session_project_{PLAN_NAME}.md`

**Example parsing:**
- Input: "user authentication" → SCOPE = "feature", PLAN_NAME = "user_authentication"
- Input: "epic authentication system" → SCOPE = "epic", PLAN_NAME = "authentication_system"
- Input: "project e-commerce platform" → SCOPE = "project", PLAN_NAME = "e_commerce_platform"

## Phase 0.5: Ideation (MANDATORY - DEPENDENCY_GRAPH Phase 2)

**Purpose**: Explore requirements and design before implementation planning. This phase is MANDATORY per DEPENDENCY_GRAPH.md.

1. **Invoke `brainstorming` Skill (PLANNING-ONLY MODE):**
   ```
   Run /brainstorming skill with:
   - SCOPE: $SCOPE (feature/epic/project)
   - PLAN_NAME: $PLAN_NAME
   - Initial request: $ARGUMENTS
   - MODE: planning-only (CRITICAL: Do NOT ask "Ready to set up for implementation?" - skip the "After the Design" implementation section entirely)
   ```

   **IMPORTANT**: When invoking brainstorming, explicitly instruct it:
   - Do NOT offer to create worktrees
   - Do NOT offer to transition to implementation
   - STOP after documenting the design to brainstorming.md
   - The "After the Design → Implementation" section of the skill must be SKIPPED

2. **Brainstorming Outputs:**
   - Explores user intent and requirements
   - Identifies potential approaches and trade-offs
   - Generates questions for clarification
   - Documents design decisions

3. **Save Brainstorming Results:**
   - Write output to: `.claude/docs/{PLAN_NAME}/brainstorming.md`
   - This becomes input for team selection and planning phases

**GATE**: Cannot proceed to Phase 1 until brainstorming is complete.

## Phase 1: Session Setup

Create the session context file using the SESSION_FILE variable determined in Phase 0.

The file will be one of:
- `.claude/sessions/context_session_feature_{PLAN_NAME}.md` (feature scope)
- `.claude/sessions/context_session_epic_{PLAN_NAME}.md` (epic scope)
- `.claude/sessions/context_session_project_{PLAN_NAME}.md` (project scope)

## Phase 2: Constitution

Read and parse the project's "Constitution" file: `CLAUDE.md`.

### Modular Architecture Support (Enhanced v3.2 - JSON Index Priority)

**IMPORTANT (v3.2 change)**: Prefer JSON index over parsing CLAUDE.md for reliability.

1. **Detect Modular Mode (JSON Index Preferred):**
   ```
   IS_MODULAR = false
   USE_JSON_INDEX = false
   MODULAR_INDEX = null

   # Check for machine-readable modular index first
   IF .claude/cache/modular_index.json exists:
     MODULAR_INDEX = JSON.parse(".claude/cache/modular_index.json")
     IS_MODULAR = true
     USE_JSON_INDEX = true
     Log: "Using modular_index.json for planning context"

   ELSE IF .claude/rules/ directory exists AND contains .md files:
     IS_MODULAR = true
     USE_JSON_INDEX = false
     Log: "Falling back to directory scan (modular_index.json not found)"
   ```

2. **If IS_MODULAR, load additional context:**

   a) **Load global rules (JSON index preferred):**
   ```
   IF USE_JSON_INDEX:
     For each item in MODULAR_INDEX.auto_loaded:
       Load item.file for planning context
       Log: "Loaded rule: {item.file} (purpose: {item.purpose})"
   ELSE:
     # Fallback: scan directory
     For each file in .claude/rules/*.md:
       Load and parse for planning context
   ```

   b) **Parse modular_index (JSON index preferred):**
   ```
   IF USE_JSON_INDEX:
     DOCS_INDEX = MODULAR_INDEX.on_demand
     Log: "Loaded {on_demand.length} on-demand docs from modular_index.json"
   ELSE:
     # Fallback: parse from CLAUDE.md
     IF CLAUDE.md contains [modular_index] section:
       Parse to identify available documentation
       Store in DOCS_INDEX for later reference
   ```

   c) **Identify relevant on-demand docs (JSON index preferred):**
   ```
   IF USE_JSON_INDEX:
     # Use structured load_when hints from JSON
     For each doc in MODULAR_INDEX.on_demand:
       IF SCOPE matches doc.load_when keywords:
         Load doc.file into planning context
         Log: "Loaded on-demand doc: {doc.file} (reason: {doc.load_when})"

   ELSE:
     # Fallback: heuristic matching
     Based on SCOPE and PLAN_NAME, determine which docs to load:

     IF SCOPE involves database:
       Load .claude/docs/architecture/database-schema.md (if exists)

     IF SCOPE involves API:
       Load .claude/docs/architecture/api-contracts.md (if exists)

     IF SCOPE involves authentication:
       Load .claude/docs/patterns/auth-flows.md (if exists)
   ```

3. **Provide context to agents:**
   - Global rules are always provided
   - Relevant on-demand docs are loaded based on scope
   - Agents informed which additional docs are available
   - **v3.2**: JSON index provides structured discovery of available docs

## Phase 3: Team Selection (REFACTORED v2.4 - DAG-Integrated)

**Use dag.json for consistent agent selection across all flows.**

1.  **Load Agent DAG:**
    ```
    Read .claude/agents/dag.json
    Extract:
    - feature_patterns: Predefined agent combinations
    - mandatory_agents: Always include (security-architect)
    - conditional_rules: Trigger conditions for each agent
    ```

2.  **Start with the Core:** Read `[core_team]` list from `CLAUDE.md`.

3.  **Match Feature Pattern (dag.json integration):**
    ```
    Analyze request to determine feature_pattern:

    IF request involves database + API + backend + frontend:
      PATTERN = "fullstack"
      AGENTS = dag.feature_patterns.fullstack.sequence +
               dag.feature_patterns.fullstack.parallel_after_api

    ELSE IF request involves only frontend/UI:
      PATTERN = "frontend-only"
      AGENTS = dag.feature_patterns.frontend-only.sequence

    ELSE IF request involves only backend/API:
      PATTERN = "backend-only"
      AGENTS = dag.feature_patterns.backend-only.sequence

    ELSE IF request involves deployment/infrastructure:
      PATTERN = "infrastructure"
      AGENTS = dag.feature_patterns.infrastructure.sequence

    ELSE IF request involves workflow automation:
      PATTERN = "workflow-automation"
      AGENTS = dag.feature_patterns.workflow-automation.sequence

    # Always add mandatory agents
    AGENTS += dag.mandatory_agents.always_invoke
    ```

4.  **Analyze for Additional Specialists:** Check request for keywords (e.g., "database", "performance").
3.  **Recruit Specialists (Auto-Healing with Recovery):**
    - `if specialist_file_exists:` add to team.
    - `else:`
      - Invoke `@agent-librarian "scout: $specialist"` with timeout: 300000ms
      - **Recovery Loop (v2.3 Enhancement):**

      ```
      MISSING_AGENT_RETRIES = 0
      MAX_MISSING_AGENT_RETRIES = 2

      WHILE MISSING_AGENT_RETRIES < MAX_MISSING_AGENT_RETRIES:
        # Step 1: agent-librarian drafts the agent
        agent_draft = @agent-librarian "scout: $specialist"

        # Step 2: Save progress to session file
        Write to SESSION_FILE:
        - progress_state: "waiting_for_agent"
        - missing_agent: $specialist
        - draft_location: agent_draft.path
        - timestamp: current_timestamp

        # Step 3: Ask user for action
        Ask user:
        "Agent '$specialist' not found. @agent-librarian has created a draft.

        Options:
        a) Review draft and approve → Agent will be installed, planning continues
        b) Skip this specialist → Continue with available agents (may affect quality)
        c) Abort planning → Exit and resolve manually

        Choose (a/b/c):"

        IF user_choice == "a":
          # Install the drafted agent
          Move agent_draft to .claude/agents/{specialist}.md
          Add specialist to team
          BREAK  # Continue planning

        ELSE IF user_choice == "b":
          # Skip and continue
          Log warning: "Skipped specialist: $specialist"
          Add to SKIPPED_AGENTS list
          BREAK  # Continue planning without this agent

        ELSE IF user_choice == "c":
          # Abort
          Set TASK_STATUS = "aborted_missing_agent"
          EXIT

        MISSING_AGENT_RETRIES += 1
      ```

      - If max retries exceeded:
        - Log: "Could not recruit specialist after {MAX_MISSING_AGENT_RETRIES} attempts"
        - Continue planning with available agents
        - Add warning to final plan about missing specialist

## Phase 3.5: Scope-Specific Team Adjustment

Based on SCOPE variable, adjust the agent team composition to match planning level:

**If SCOPE == "feature":**
- Use core_team + request-specific specialists (current behavior)
- Focus: Single feature implementation planning

**If SCOPE == "epic":**
- **Mandatory additions to team:**
  - `domain-logic-architect` (coordinate backend across multiple features)
  - `presentation-layer-architect` (coordinate frontend across multiple features)
  - `test-strategy-planner` (epic-level test strategy)
- **Focus:** Multi-feature coordination, dependency mapping, shared infrastructure
- **Outcome:** Plan that coordinates 3-5 related features as cohesive epic

**If SCOPE == "project":**
- **Use full agent roster:**
  - All `core_team` members (security-architect, acceptance-validator, etc.)
  - `domain-logic-architect` (overall system architecture)
  - `presentation-layer-architect` (UI/UX strategy and design system)
  - `test-strategy-planner` (project-wide QA strategy)
  - `ui-component-architect` (design system planning)
  - `experience-analyzer` (DX/UX analysis)
- **Focus:** High-level architecture, epic identification, technology validation
- **Outcome:** Project roadmap with 3-7 epics, architecture decisions, priorities

**Update AGENTS_USED_LIST** with final team composition.

## Phase 4: Plan (Scope-Aware) - Using writing-plans Skill

**IMPORTANT**: Use the `writing-plans` skill for structured plan generation (per DEPENDENCY_GRAPH.md Phase 3).

1. **Invoke `writing-plans` Skill (PLANNING-ONLY MODE):**
   ```
   Run /writing-plans skill with:
   - SCOPE: $SCOPE
   - PLAN_NAME: $PLAN_NAME
   - SESSION_FILE: $SESSION_FILE
   - BRAINSTORMING_OUTPUT: .claude/docs/{PLAN_NAME}/brainstorming.md
   - CLAUDE_MD: CLAUDE.md contents
   - MODE: planning-only (CRITICAL: Do NOT offer "Execution Handoff" - skip the "After saving the plan, offer execution choice" section entirely)
   ```

   **IMPORTANT**: When invoking writing-plans, explicitly instruct it:
   - Do NOT offer execution options (Subagent-Driven or Parallel Session)
   - Do NOT ask "Which approach?" for implementation
   - STOP after saving the plan to SESSION_FILE
   - The "Execution Handoff" section of the skill must be SKIPPED

2. **Skill generates structured plan** to SESSION_FILE based on SCOPE:

**For SCOPE == "feature":**
- **Current behavior** - Single feature implementation plan
- Include:
  - Feature overview and objectives
  - Files to modify
  - Implementation approach
  - Key technical decisions
  - Dependencies and prerequisites

**For SCOPE == "epic":**
- **Epic-level planning** - Coordinate multiple related features
- Include:
  - Epic overview and business goals
  - **Break down into 3-5 individual features** (list each feature with brief description)
  - Identify dependencies between features (which must come first?)
  - Suggested implementation order (with rationale)
  - Shared components/infrastructure across features
  - Epic acceptance criteria (high-level)
  - Create epic backlog structure

**For SCOPE == "project":**
- **Project-level planning** - High-level architecture and roadmap
- Include:
  - Project vision and objectives
  - High-level architecture diagram (text-based: components, data flow, integrations)
  - Technology stack validation (confirm CLAUDE.md choices are appropriate)
  - **Identify 3-7 major epics** (each epic is a major feature area)
  - Suggest epic priorities (critical → nice-to-have)
  - Risk assessment (technical risks, dependencies, unknowns)
  - Project roadmap outline (phases, milestones)
  - Architecture decisions and trade-offs

## Phase 5: Advice

Use the sub-agents (from `AGENTS_USED_LIST`) _in parallel_ to get knowledge and advice.

**CRITICAL:** Provide each agent with:
- **SESSION_FILE** (the scope-specific context file from Phase 0)
- **CLAUDE.md** (project constitution)
- **SCOPE variable** (so agents understand planning level: feature/epic/project)

This context allows agents to tailor their advice appropriately:
- Feature scope → Focus on implementation details
- Epic scope → Focus on coordination and shared components
- Project scope → Focus on architecture and strategic decisions

## Phase 6: Update & Synthesize

Synthesize all advice into one "master plan" in the SESSION_FILE.

Ensure the master plan reflects the appropriate scope:
- **Feature scope:** Unified implementation plan for single feature
- **Epic scope:** Coordinated plan for multiple features with clear dependencies
- **Project scope:** Comprehensive project roadmap with epics and architecture

## Phase 7: Clarification

Ask the user questions about anything unclear.

## Phase 8: Explicit Termination (MANDATORY)

**THIS IS THE FINAL PHASE. The flow-plan command ENDS here.**

1. **Confirm Plan Location:**
   ```
   Output to user:
   "✅ Plan complete and saved to: {SESSION_FILE}

   **Next Steps (User Action Required):**
   1. Review the plan in {SESSION_FILE}
   2. Run `/flow-issue-create` to create issues from this plan
   3. Run `/flow-feature-build` to implement

   ⚠️ This command does NOT implement - only plans."
   ```

2. **PROHIBITED ACTIONS (After Phase 8):**
   - ❌ Do NOT use `EnterPlanMode` or `ExitPlanMode` tools
   - ❌ Do NOT write production code
   - ❌ Do NOT create project files
   - ❌ Do NOT offer to implement
   - ❌ Do NOT continue to any other phase

3. **Set TASK_STATUS = "success"** and proceed to Metrics Block.

## Metrics Block (END)

# 1. If task completed successfully, set TASK_STATUS = "success"

# 2. Call `python3 .claude/scripts/log_metric.py` silently with:
#    - command: "flow-plan"
#    - scope: $SCOPE (feature/epic/project)
#    - plan_name: $PLAN_NAME
#    - status: $TASK_STATUS
#    - agents_used: $AGENTS_USED_LIST
#    - start_time: $START_TIME
#    - end_time: current_timestamp

**Note:** The metrics help track command usage patterns, scope distribution (feature vs epic vs project), and agent collaboration effectiveness.
