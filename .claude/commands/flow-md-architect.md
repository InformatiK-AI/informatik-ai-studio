#

# Task: MD-Architect - CLAUDE.md Creation & Maintenance (v2.2)

# Argument: $ARGUMENTS (mode: create|audit|improve|recreate|migrate-modular)

#

## Metrics Block (START)

# 1. Set START_TIME = current_timestamp

# 2. Set TASK_STATUS = "fail"

# 3. Set ARCHITECTURE_MODE = "modular" (always modular)

<user_request>
#$ARGUMENTS
</user_request>

## Purpose

This command invokes the `claude-md-architect` skill to create, audit, or improve CLAUDE.md files - the project's "constitution" that defines architecture, workflows, and agent coordination.

**v2.2 Changes**: Session file creation now uses explicit Write instruction to ensure files are properly created.

## Usage

```bash
claude -p .claude/commands/flow-md-architect.md create
claude -p .claude/commands/flow-md-architect.md audit
claude -p .claude/commands/flow-md-architect.md improve
claude -p .claude/commands/flow-md-architect.md recreate
claude -p .claude/commands/flow-md-architect.md migrate-modular  # NEW
```

## Phase 1: Mode Detection & Validation

1. **Parse Arguments:** Extract mode from `$ARGUMENTS`.
2. **Validate Mode:** Ensure mode is one of: `create`, `audit`, `improve`, `recreate`, `migrate-modular`.
3. **If no mode provided or invalid:**
   - Ask the user: "What would you like to do with CLAUDE.md?"
   - Options:
     - **create** - Create new CLAUDE.md from scratch
     - **audit** - Analyze existing CLAUDE.md for completeness
     - **improve** - Modernize/enhance existing CLAUDE.md
     - **recreate** - Replace existing CLAUDE.md completely
     - **migrate-modular** - Convert monolithic CLAUDE.md to modular architecture
4. **Set MODE variable** for subsequent phases.

## Phase 2: Context Gathering

1. **Check for existing CLAUDE.md:**
   - If exists: Read current CLAUDE.md to provide context to skill
   - If not exists and mode != "create": Warn the user and suggest switching to "create" mode

2. **Gather project context:**
   - Check for package.json, requirements.txt, or other dependency files
   - Identify project type (web app, API, CLI tool, etc.)
   - Note existing directory structure

3. **Prepare context summary** for skill invocation.

## Phase 2.5: Architecture Setup (Modular-Only)

All projects use modular architecture. No user prompts required.

1. **Set Architecture Mode:**

   ```
   ARCHITECTURE_MODE = "modular"  # Always modular
   Log: "Using modular architecture (standard for all projects)"
   ```

2. **Create modular directories:**

   ```bash
   mkdir -p .claude/rules/domain
   mkdir -p .claude/docs/architecture
   mkdir -p .claude/docs/patterns
   mkdir -p .claude/docs/guides
   mkdir -p .claude/examples
   ```

3. **For existing CLAUDE.md (audit/improve modes):**
   - If project has monolithic CLAUDE.md > 300 lines
   - Automatically trigger migration logic
   - Extract sections to modular files

4. **Migration Logic (MODE == "migrate-modular" or monolithic detected):**

   a) **Analyze existing CLAUDE.md sections:**
   - Identify sections >50 lines (candidates for extraction)
   - Map sections to target files using migration table

   b) **Present migration plan to user:**

   ```
   Migration Plan:
   ├── [code_standards] (75 lines) → .claude/rules/code-standards.md
   ├── [testing_requirements] (60 lines) → .claude/rules/testing-policy.md
   ├── [security_requirements] (45 lines) → .claude/rules/security-policy.md
   ├── [workflow] (30 lines) → .claude/rules/git-workflow.md
   ├── Database schema (100 lines) → .claude/docs/architecture/database-schema.md
   └── API contracts (80 lines) → .claude/docs/architecture/api-contracts.md

   Estimated result: CLAUDE.md reduced from 850 → 180 lines
   ```

   c) **Get user approval before proceeding**

## Phase 3: Invoke claude-md-architect Skill

**IMPORTANT:** The `claude-md-architect` skill contains comprehensive instructions for CLAUDE.md management.

1. **Invoke skill with context:**

   ```
   Use the Skill tool to invoke: claude-md-architect
   ```

2. **Provide skill with:**
   - MODE: The selected mode (create/audit/improve/recreate/migrate-modular)
   - ARCHITECTURE_MODE: "modular" or "monolithic" (from Phase 2.5)
   - CURRENT_CLAUDE_MD: Contents of existing CLAUDE.md (if exists)
   - PROJECT_CONTEXT: Project type, dependencies, structure

3. **Let skill execute:** The skill will handle:
   - Strategic analysis of project needs
   - Factory vertical selection (Astro/Next.js/Python)
   - CLAUDE.md structure generation (modular or monolithic)
   - Agent coordination setup
   - Testing requirements definition
   - **If modular:** Generate rules and docs files

## Phase 4: Review & Validation

1. **Review skill output:**
   - Check that CLAUDE.md has all required sections
   - Verify stack choices align with project needs
   - Ensure agent coordination is properly defined

2. **Show the user the results:**
   - For **create/recreate**: Show new CLAUDE.md structure
   - For **audit**: Show audit findings and recommendations
   - For **improve**: Show proposed improvements
   - For **migrate-modular**: Show migration summary and new structure

3. **Get approval before finalizing.**

## Phase 4.5: Modular Reference Validation

**Executed for all projects (modular architecture is standard).**

1. **Validate File Existence:**

   ```
   MISSING_FILES = []
   ORPHAN_FILES = []

   # Check all files referenced in [modular_index]
   For each entry in CLAUDE.md [modular_index]:
     IF file does not exist:
       MISSING_FILES.append(file_path)

   # Check for orphan files (exist but not referenced)
   For each .md file in .claude/rules/ and .claude/docs/:
     IF file not in [modular_index]:
       ORPHAN_FILES.append(file_path)
   ```

2. **Validate Path-Specific Rules:**

   ```
   INVALID_PATHS = []

   For each file in .claude/rules/domain/:
     Parse YAML frontmatter
     For each path in frontmatter.paths:
       IF path pattern is invalid (syntax error):
         INVALID_PATHS.append({file, path})
   ```

3. **Validate Content Quality:**

   ```
   SIZE_WARNINGS = []

   # Core CLAUDE.md
   IF CLAUDE.md lines > 300:
     SIZE_WARNINGS.append("CLAUDE.md exceeds 300 lines (modular target)")

   # Global rules
   For each file in .claude/rules/:
     IF file lines > 150:
       SIZE_WARNINGS.append("{file} exceeds 150 lines")

   # Path-specific rules
   For each file in .claude/rules/domain/:
     IF file lines > 200:
       SIZE_WARNINGS.append("{file} exceeds 200 lines")
   ```

4. **Generate Validation Report:**

   ```
   === MODULAR VALIDATION REPORT ===

   ✅ PASS / ⚠️ WARNINGS / ❌ FAIL

   File Integrity:
   - Missing files: {MISSING_FILES.length}
   - Orphan files: {ORPHAN_FILES.length}

   Path Rules:
   - Invalid paths: {INVALID_PATHS.length}

   Size Compliance:
   - Warnings: {SIZE_WARNINGS.length}

   {Details if any issues found}
   ```

5. **Handle Validation Results:**

   ```
   IF MISSING_FILES not empty:
     STATUS = FAIL
     "Cannot proceed: Missing referenced files"
     List files that need to be created

   ELSE IF INVALID_PATHS not empty:
     STATUS = FAIL
     "Cannot proceed: Invalid path patterns"
     List files with invalid patterns

   ELSE IF ORPHAN_FILES not empty OR SIZE_WARNINGS not empty:
     STATUS = WARNINGS
     Ask user: "Proceed with warnings? (y/n)"
     If yes: Continue
     If no: Abort for fixes

   ELSE:
     STATUS = PASS
     "Modular structure validated successfully"
   ```

## Phase 5: Post-Processing (Conditional)

**If MODE is "create", "recreate", or "migrate-modular" AND the user approves:**

1. **Trigger hooks-setup skill (OPTIONAL):**
   - Ask the user: "Would you like to set up all hooks (Git, code quality, etc.) now?"
   - If yes:
     ```
     Use the Skill tool to invoke: hooks-setup
     ```
   - If no: Remind the user they can run `/skill hooks-setup` later

2. **Create initial directories:**
   - Create `.claude/agents/` directory
   - Create `.claude/sessions/` directory
   - Create `.claude/logs/` directory
   - Create `.claude/rules/` directory
   - Create `.claude/rules/domain/` directory
   - Create `.claude/docs/` directory
   - Create `.claude/docs/architecture/` directory
   - Create `.claude/docs/patterns/` directory
   - Create `.claude/docs/guides/` directory
   - Create `.claude/examples/` directory

3. **Success message:**

   ```
   CLAUDE.md modular structure successfully [created/migrated]!

   Files created:
   ├── CLAUDE.md (core: {LINE_COUNT} lines)
   ├── .claude/rules/
   │   ├── code-standards.md
   │   ├── testing-policy.md
   │   ├── security-policy.md
   │   ├── git-workflow.md
   │   └── agent-coordination.md
   └── .claude/docs/
       └── architecture/
           └── [generated docs]

   Session artifacts:
   ├── .claude/sessions/context_session_md_architect_{timestamp}.md
   └── .claude/cache/modular_index.json

   Next steps:
   - Review the modular files
   - Customize rules as needed
   - Add path-specific rules in .claude/rules/domain/ if needed
   - Run workflow commands (flow-plan, flow-issue-create, etc.)
   ```

---

## === POST-CONDITIONAL PHASES (ALWAYS EXECUTED) ===

The following phases execute unconditionally for ALL modes (create, audit, improve, recreate, migrate-modular), regardless of Phase 5 conditions or user approval status.

---

## Phase 6.5: Create Context Session File (ALWAYS EXECUTED)

**MANDATORY: This phase executes for ALL modes, regardless of Phase 5 conditions.**

**Purpose**: Create a session file to track progress and enable resume/recovery for downstream commands.

**Location:** `.claude/sessions/context_session_md_architect_{timestamp}.md`

1. **Ensure directories exist (in case Phase 5 was skipped):**

   ```bash
   mkdir -p .claude/sessions
   mkdir -p .claude/cache
   ```

2. **Generate Session File:**

   ```
   SESSION_TIMESTAMP = format(current_timestamp, "YYYYMMDD_HHmmss")
   SESSION_FILE = ".claude/sessions/context_session_md_architect_{SESSION_TIMESTAMP}.md"
   ```

   **IMPORTANT**: Use the Write tool to create the session file:

   ```markdown
   # MD-Architect Session

   ## Metadata

   - Mode: {MODE}
   - Architecture: {ARCHITECTURE_MODE}
   - Timestamp: {START_TIME}
   - Status: {TASK_STATUS}

   ## Files Created

   ### Core File

   - CLAUDE.md (lines: {LINE_COUNT})

   ### Auto-Loaded Rules

   {For each file in .claude/rules/\*.md:}

   - {file_path}

   ### Path-Specific Rules

   {For each file in .claude/rules/domain/:}

   - {file_path} (paths: {frontmatter.paths})

   ### On-Demand Docs

   {For each file in .claude/docs/:}

   - {file_path}

   ## Modular Index

   {Copy of [modular_index] section from CLAUDE.md for reference}

   ## Session Log

   - {START_TIME}: Session started with mode={MODE}
   - {timestamp}: Architecture mode determined: {ARCHITECTURE_MODE}
   - {timestamp}: Files generated: {count}
   - {END_TIME}: Session completed with status={TASK_STATUS}
   ```

   **CRITICAL**: Do NOT skip this step. The session file MUST be created using the Write tool.

3. **Log Session Creation:**
   ```
   Log: "Session file created: {SESSION_FILE}"
   ```

## Phase 6.6: Generate Machine-Readable Modular Index (ALWAYS EXECUTED)

**MANDATORY: This phase executes for ALL modes, regardless of Phase 5 conditions.**

**Purpose**: Create a JSON index file for programmatic access by downstream commands and skills.

**Location:** `.claude/cache/modular_index.json`

1. **Ensure cache directory exists:**

   ```bash
   mkdir -p .claude/cache
   ```

2. **Generate modular_index.json:**

   ```json
   {
     "version": "1.0",
     "created": "{ISO_TIMESTAMP}",
     "architecture_mode": "modular",
     "source_claude_md": "CLAUDE.md",
     "session_file": "{SESSION_FILE}",

     "auto_loaded": [
       {
         "file": ".claude/rules/code-standards.md",
         "priority": "high",
         "purpose": "Coding conventions and style guide",
         "required": true,
         "checksum": "{sha256_hash}"
       },
       {
         "file": ".claude/rules/testing-policy.md",
         "priority": "high",
         "purpose": "Testing requirements and coverage targets",
         "required": true,
         "checksum": "{sha256_hash}"
       },
       {
         "file": ".claude/rules/security-policy.md",
         "priority": "high",
         "purpose": "Security requirements and OWASP compliance",
         "required": true,
         "checksum": "{sha256_hash}"
       },
       {
         "file": ".claude/rules/git-workflow.md",
         "priority": "medium",
         "purpose": "Git workflow and branching strategy",
         "required": false,
         "checksum": "{sha256_hash}"
       },
       {
         "file": ".claude/rules/agent-coordination.md",
         "priority": "medium",
         "purpose": "Agent invocation rules and coordination",
         "required": false,
         "checksum": "{sha256_hash}"
       }
     ],

     "path_specific": [
       {
         "file": ".claude/rules/domain/{rule_name}.md",
         "paths": ["src/api/**", "src/routes/**"],
         "purpose": "Domain-specific rules",
         "required": false,
         "checksum": "{sha256_hash}"
       }
     ],

     "on_demand": [
       {
         "file": ".claude/docs/architecture/database-schema.md",
         "load_when": "Database changes",
         "purpose": "Database schema documentation",
         "required": false,
         "checksum": "{sha256_hash}"
       },
       {
         "file": ".claude/docs/architecture/api-contracts.md",
         "load_when": "API changes",
         "purpose": "API contract documentation",
         "required": false,
         "checksum": "{sha256_hash}"
       }
     ],

     "validation": {
       "total_files": "{count}",
       "required_files": "{count}",
       "optional_files": "{count}",
       "size_limits": {
         "core_claude_md": 300,
         "global_rules": 150,
         "path_rules": 200,
         "on_demand_docs": null
       }
     }
   }
   ```

3. **Compute Checksums Function:**

   ```python
   # Checksum computation (conceptual - execute via appropriate method)
   import hashlib

   def compute_checksum(file_path):
       """Compute truncated SHA256 checksum for cache invalidation."""
       with open(file_path, 'rb') as f:
           full_hash = hashlib.sha256(f.read()).hexdigest()
           return f"sha256:{full_hash[:16]}"  # Truncated for readability

   # Example output: "sha256:a1b2c3d4e5f67890"
   ```

   **Alternative (Bash):**

   ```bash
   # For each file, compute checksum
   CHECKSUM=$(sha256sum "$FILE_PATH" | cut -c1-16)
   echo "sha256:$CHECKSUM"
   ```

4. **Populate JSON with actual files and checksums:**

   ```
   TOTAL_CHECKSUMS = 0

   # Scan auto-loaded rules WITH checksums
   For each file in .claude/rules/*.md (excluding domain/):
     checksum = compute_checksum(file)  # ACTUAL HASH, not placeholder
     TOTAL_CHECKSUMS += 1
     Add to auto_loaded[] with:
     - file: relative path
     - priority: "high" if filename in [code-standards, testing-policy, security-policy], else "medium"
     - purpose: extract from file header or frontmatter
     - required: true if priority == "high"
     - checksum: checksum  # REAL VALUE like "sha256:a1b2c3d4e5f6..."

   # Scan path-specific rules WITH checksums
   For each file in .claude/rules/domain/:
     Parse YAML frontmatter for 'paths' and 'purpose'
     checksum = compute_checksum(file)  # ACTUAL HASH
     TOTAL_CHECKSUMS += 1
     Add to path_specific[] with:
     - file: relative path
     - paths: from frontmatter
     - purpose: from frontmatter or file header
     - required: false
     - checksum: checksum  # REAL VALUE

   # Scan on-demand docs WITH checksums
   For each file in .claude/docs/**/*.md:
     checksum = compute_checksum(file)  # ACTUAL HASH
     TOTAL_CHECKSUMS += 1
     Add to on_demand[] with:
     - file: relative path
     - load_when: infer from path (architecture → "Schema/API changes", patterns → "Pattern lookup")
     - purpose: extract from file header
     - required: false
     - checksum: checksum  # REAL VALUE

   # Calculate validation counts
   validation.total_files = auto_loaded.length + path_specific.length + on_demand.length
   validation.required_files = count where required == true
   validation.optional_files = validation.total_files - validation.required_files
   validation.total_checksums = TOTAL_CHECKSUMS
   validation.generated_at = ISO_TIMESTAMP
   ```

5. **Log JSON generation:**
   ```
   Log: "Modular index created: .claude/cache/modular_index.json"
   Log: "  - Auto-loaded rules: {auto_loaded.length}"
   Log: "  - Path-specific rules: {path_specific.length}"
   Log: "  - On-demand docs: {on_demand.length}"
   ```

**Skill Usage Reference:**

| Skill                  | How It Uses modular_index.json                |
| ---------------------- | --------------------------------------------- |
| `preflight-check`      | Validates all `required: true` files exist    |
| `hooks-setup`          | Reads rules to configure appropriate hooks    |
| `acceptance-validator` | Loads testing-policy.md for test requirements |
| `security-architect`   | Loads security-policy.md for security checks  |
| `flow-feature-build`   | Phase 0.5 loads rules based on feature paths  |
| `flow-plan`            | Phase 2 loads relevant docs for planning      |

## Phase 6.7: Session Artifact Validation (ALWAYS EXECUTED)

**MANDATORY: Verify session artifacts were created before completing.**

1. **Validate Session File:**

   ```
   IF NOT exists(".claude/sessions/context_session_md_architect_{SESSION_TIMESTAMP}.md"):
     ERROR: "Session file creation failed"
     TASK_STATUS = "fail"
     Log: "FATAL: Session file was not created"
     Exit with error
   ```

2. **Validate Modular Index:**

   ```
   IF NOT exists(".claude/cache/modular_index.json"):
     ERROR: "Modular index creation failed"
     TASK_STATUS = "fail"
     Log: "FATAL: Modular index JSON was not created"
     Exit with error
   ```

3. **Log Success:**

   ```
   Log: "Session artifacts validated successfully"
   Log: "  - Session file: .claude/sessions/context_session_md_architect_{SESSION_TIMESTAMP}.md"
   Log: "  - Modular index: .claude/cache/modular_index.json"
   ```

---

## Phase 7: Documentation Update (Optional)

**If `.claude/commands/README.md` exists:**

- Add entry for `flow-md-architect.md` command
- Document usage and modes

## Metrics Block (END)

# 1. Set TASK_STATUS = "success"

# 2. Call `python3 .claude/scripts/log_metric.py` silently with:

# - command: "flow-md-architect"

# - mode: $MODE

# - status: $TASK_STATUS

# - start_time: $START_TIME

# - end_time: current_timestamp

---

## Notes for Claude

- This command is a lightweight orchestrator - the heavy lifting is done by the `claude-md-architect` skill
- The skill has comprehensive knowledge of Factory Verticals and CLAUDE.md structure
- Always read existing CLAUDE.md before invoking skill (provides important context)
- After CLAUDE.md creation, consider triggering hooks-setup for complete project setup
- Metric tracking helps monitor command usage and success rates

## Command Metadata

- **Version:** 3.2
- **Created:** 2026-01-10
- **Last Updated:** 2026-01-17
- **Dependencies:** claude-md-architect skill, optional hooks-setup skill
- **Related Commands:** hooks-setup skill, preflight-check skill

## Changelog

### v3.2 (2026-01-17)

- **FEAT**: Implemented actual checksum generation in Phase 6.6
- Added explicit compute_checksum() function with Python and Bash alternatives
- Checksums now use truncated SHA256 format: "sha256:{first_16_chars}"
- Added total_checksums and generated_at to validation metadata
- Enables downstream cache invalidation when rules change

### v3.1 (2026-01-17)

- **FIX**: Added explicit "(ALWAYS EXECUTED)" markers to Phases 6.5 and 6.6
- Added phase boundary separator "=== POST-CONDITIONAL PHASES ===" before Phase 6.5
- Added directory creation step at start of Phase 6.5 (ensures .claude/sessions/ and .claude/cache/ exist)
- Added Phase 6.7: Session Artifact Validation gate
- These changes ensure session files and modular index are created for ALL modes (including audit/improve)

### v3.0 (2026-01-17)

- **BREAKING**: Modular architecture is now the only supported mode
- Removed monolithic architecture option and user prompts
- Simplified Phase 2.5: Architecture Setup (no detection logic needed)
- All projects now automatically use modular structure
- Phase 4.5 and 6.6 now execute unconditionally
- Updated success messages to modular-only format

### v2.2 (2026-01-18)

- Fixed Phase 6.5: Added explicit Write instruction for session file creation
- Session file is now properly created using the Write tool
- Prevents session file from being silently skipped

### v2.1 (2026-01-17)

- Added Phase 6.5: Context Session File Creation
- Added Phase 6.6: Machine-Readable Modular Index Generation
- Renumbered Phase 6 to Phase 7 (Documentation Update)

### v2.0 (2026-01-17)

- Added `migrate-modular` mode for converting monolithic to modular architecture
- Added Phase 2.5: Architecture Mode Detection
- Added Phase 4.5: Modular Reference Validation
- Support for both modular and monolithic architectures

### v1.0 (2026-01-10)

- Initial implementation with create, audit, improve, recreate modes
