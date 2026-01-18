---
name: preflight-check
description: |
  Performs comprehensive pre-flight validation before flow-feature-build begins. Acts as a safety gate, catching common issues early: validates context files, checks agent availability, verifies CLAUDE.md completeness, checks git status, validates dependencies, and confirms test framework setup. Automatically triggered at the start of flow-feature-build.
version: 1.3.0
---

# Pre-Flight Check Skill

## Purpose

Performs comprehensive pre-flight validation before `flow-feature-build` begins. This skill acts as a safety gate, catching common issues early and preventing wasted effort on doomed-to-fail implementations.

## When to Use This Skill

This skill is **automatically invoked** at the start of `flow-feature-build` (before Phase 1). It can also be manually invoked to check project health:

```
"Run preflight-check before starting implementation"
"Use preflight-check to validate project setup"
```

## Workflow

### Phase 1: Context Validation

1. **Check Feature Context File**
   - Verify that `context_session_feature_{NAME}.md` exists
   - Validate file is not empty
   - Check required sections exist:
     - Overview
     - Objectives
     - Files to modify
     - Key decisions

   **Result**:
   - ✅ PASS: Context file exists and has all sections
   - ⚠️ WARNING: Context file exists but missing optional sections
   - ❌ FAIL: Context file missing or empty

2. **Validate Context Structure**
   - Parse markdown structure
   - Ensure headers are properly formatted
   - Check for placeholder text (e.g., "TODO", "TBD")

   **Result**:
   - ⚠️ WARNING: Found placeholder text, context may be incomplete

### Phase 2: Agent Availability Check

1. **Read Feature Requirements**
   - Parse context file to identify required agents
   - Check keywords:
     - "database" → database-architect
     - "API" → api-contract-designer
     - "backend" → domain-logic-architect
     - "frontend" → frontend-architect
     - "UI components" → frontend-architect

2. **Verify Agent Files Exist**
   - Check `.claude/agents/{agent-name}.md` exists for each required agent
   - Validate agent files are not empty
   - Check YAML front matter is valid

   **Result**:
   - ✅ PASS: All required agents available
   - ⚠️ WARNING: Optional agents missing (e.g., devops-architect)
   - ❌ FAIL: Critical agents missing (use @agent-librarian to draft)

### Phase 3: CLAUDE.md Validation

1. **File Existence**
   - Verify `CLAUDE.md` exists at project root

2. **Required Sections**
   - Check for critical sections:
     - `[stack]` - Tech stack definition
     - `[methodology]` - Development workflow
     - `[core_team]` - Core agents list
     - `[code_standards]` - Coding standards

   **Result**:
   - ❌ FAIL: CLAUDE.md missing or incomplete (run flow-md-architect)

3. **Methodology Validation**
   - Ensure `[methodology].workflow` is set
   - Valid values: "TDD", "RAD", "Standard"

   **Result**:
   - ⚠️ WARNING: workflow not set, will default to "Standard"

4. **Stack Completeness**
   - Verify stack section has:
     - framework (e.g., "React", "Next.js")
     - database (if backend feature)
     - api_type (if API feature)

   **Result**:
   - ⚠️ WARNING: Incomplete stack definition

### Phase 3.5: Modular Architecture Validation (Enhanced v1.3 - JSON Index Support)

**Execute only if modular architecture is detected.**

1. **Detect Modular Architecture (JSON Index Preferred)**
   ```
   IS_MODULAR = false
   USE_JSON_INDEX = false
   MODULAR_INDEX = null

   # Check for machine-readable modular index first (preferred)
   IF .claude/cache/modular_index.json exists:
     MODULAR_INDEX = JSON.parse(".claude/cache/modular_index.json")
     IS_MODULAR = true
     USE_JSON_INDEX = true
     Log: "Using modular_index.json for validation"

   ELSE IF .claude/rules/ directory exists AND contains .md files:
     IS_MODULAR = true
     USE_JSON_INDEX = false
     Log: "Falling back to directory scan (modular_index.json not found)"

   ELSE IF CLAUDE.md contains [modular_index] section:
     IS_MODULAR = true
     USE_JSON_INDEX = false
   ```

2. **If IS_MODULAR == true, validate modular structure:**

   a) **Required Rules Existence (JSON Index Preferred):**
   ```
   MISSING_RULES = []

   IF USE_JSON_INDEX:
     # Use JSON index for validation (more reliable)
     For each item in MODULAR_INDEX.auto_loaded WHERE item.required == true:
       IF file item.file does not exist:
         MISSING_RULES.append(item.file)

   ELSE:
     # Fallback: hardcoded list
     REQUIRED_RULES = [
       ".claude/rules/code-standards.md",
       ".claude/rules/testing-policy.md",
       ".claude/rules/security-policy.md",
       ".claude/rules/git-workflow.md",
       ".claude/rules/agent-coordination.md"
     ]

     For each rule in REQUIRED_RULES:
       IF file does not exist:
         MISSING_RULES.append(rule)
   ```

   **Result**:
   - ⚠️ WARNING: Missing rule files: {MISSING_RULES}
   - Suggest: "Run flow-md-architect migrate-modular to create missing rules"

   b) **Reference Integrity Check (JSON Index Preferred):**
   ```
   BROKEN_REFS = []
   ORPHAN_FILES = []

   IF USE_JSON_INDEX:
     # Validate all files in JSON index exist
     ALL_INDEX_FILES = [
       ...MODULAR_INDEX.auto_loaded.map(i => i.file),
       ...MODULAR_INDEX.path_specific.map(i => i.file),
       ...MODULAR_INDEX.on_demand.map(i => i.file)
     ]

     For each file_path in ALL_INDEX_FILES:
       IF file does not exist:
         BROKEN_REFS.append(file_path)

     # Check for orphan files not in JSON index
     ALL_ACTUAL_FILES = scan(.claude/rules/**/*.md, .claude/docs/**/*.md)
     For each actual_file in ALL_ACTUAL_FILES:
       IF actual_file not in ALL_INDEX_FILES:
         ORPHAN_FILES.append(actual_file)

   ELSE:
     # Fallback: parse from CLAUDE.md
     Parse CLAUDE.md for [modular_index] section
     For each file referenced in modular_index:
       IF file does not exist:
         BROKEN_REFS.append(file)

     # Check for orphan files
     For each .md file in .claude/rules/ and .claude/docs/:
       IF file not in modular_index:
         ORPHAN_FILES.append(file)
   ```

   **Result**:
   - ❌ FAIL: Broken references found: {BROKEN_REFS}
   - ⚠️ WARNING: Orphan files detected: {ORPHAN_FILES}

   c) **Path-Specific Rules Validation (JSON Index Preferred):**
   ```
   INVALID_FRONTMATTER = []

   IF USE_JSON_INDEX:
     # Validate path patterns from JSON index
     For each item in MODULAR_INDEX.path_specific:
       IF item.paths is empty or undefined:
         INVALID_FRONTMATTER.append({file: item.file, error: "missing paths in index"})
       ELSE:
         For each path in item.paths:
           IF not valid_glob_pattern(path):
             INVALID_FRONTMATTER.append({file: item.file, error: "invalid pattern: " + path})

   ELSE:
     # Fallback: parse YAML frontmatter from files
     For each file in .claude/rules/domain/:
       TRY:
         Parse YAML frontmatter
         IF 'paths' not in frontmatter:
           INVALID_FRONTMATTER.append({file: "missing paths"})
         ELSE:
           For each path in frontmatter.paths:
             IF not valid_glob_pattern(path):
               INVALID_FRONTMATTER.append({file: "invalid pattern: " + path})
       CATCH:
         INVALID_FRONTMATTER.append({file: "invalid YAML"})
   ```

   **Result**:
   - ❌ FAIL: Invalid path-specific rules: {INVALID_FRONTMATTER}

   d) **Size Compliance (JSON Index Preferred):**
   ```
   SIZE_WARNINGS = []

   IF USE_JSON_INDEX:
     # Use size limits from JSON index
     LIMITS = MODULAR_INDEX.validation.size_limits

     # Core CLAUDE.md
     core_lines = count_lines(CLAUDE.md)
     IF core_lines > LIMITS.core_claude_md:
       SIZE_WARNINGS.append("CLAUDE.md: {core_lines} lines (target: {LIMITS.core_claude_md})")

     # Global rule files
     For each item in MODULAR_INDEX.auto_loaded:
       lines = count_lines(item.file)
       IF lines > LIMITS.global_rules:
         SIZE_WARNINGS.append("{item.file}: {lines} lines (target: {LIMITS.global_rules})")

     # Path-specific rule files
     For each item in MODULAR_INDEX.path_specific:
       lines = count_lines(item.file)
       IF lines > LIMITS.path_rules:
         SIZE_WARNINGS.append("{item.file}: {lines} lines (target: {LIMITS.path_rules})")

   ELSE:
     # Fallback: hardcoded limits
     core_lines = count_lines(CLAUDE.md)
     IF core_lines > 300:
       SIZE_WARNINGS.append("CLAUDE.md: {core_lines} lines (target: 100-300)")

     For each file in .claude/rules/:
       lines = count_lines(file)
       IF lines > 150:
         SIZE_WARNINGS.append("{file}: {lines} lines (target: 50-150)")
   ```

   **Result**:
   - ⚠️ WARNING: Size compliance issues: {SIZE_WARNINGS}

   e) **Checksum Validation (JSON Index Only):**
   ```
   CHECKSUM_MISMATCHES = []

   IF USE_JSON_INDEX:
     For each item in [...MODULAR_INDEX.auto_loaded, ...MODULAR_INDEX.path_specific]:
       IF item.checksum exists AND file exists:
         current_checksum = sha256(read_file(item.file))
         IF current_checksum != item.checksum:
           CHECKSUM_MISMATCHES.append(item.file)

     IF CHECKSUM_MISMATCHES not empty:
       Log WARNING: "Files modified since modular_index.json was generated:"
       For each file in CHECKSUM_MISMATCHES:
         Log: "  - {file}"
       Log: "Consider running flow-md-architect to regenerate index"
   ```

   **Result**:
   - ⚠️ WARNING: Files changed since index generation: {CHECKSUM_MISMATCHES}
   - Suggest: "Run flow-md-architect to regenerate modular_index.json"

3. **Modular Validation Summary:**
   ```
   IF BROKEN_REFS not empty OR INVALID_FRONTMATTER not empty:
     MODULAR_STATUS = "FAIL"
   ELSE IF MISSING_RULES not empty OR ORPHAN_FILES not empty OR SIZE_WARNINGS not empty OR CHECKSUM_MISMATCHES not empty:
     MODULAR_STATUS = "WARNING"
   ELSE:
     MODULAR_STATUS = "PASS"

   Log: "Modular validation: {MODULAR_STATUS} (source: {USE_JSON_INDEX ? 'modular_index.json' : 'directory scan'})"
   ```

### Phase 4: Git Status Check

1. **Working Tree Status**
   ```
   git status --porcelain
   ```

   - Check for uncommitted changes
   - Check for untracked files that should be committed

   **Result**:
   - ✅ PASS: Working tree clean
   - ⚠️ WARNING: Uncommitted changes exist (may cause conflicts)
   - ❌ FAIL: Merge conflicts detected (must resolve first)

2. **Branch Status**
   - Verify on correct branch (not on main/master directly)
   - Check if remote branch exists

   **Result**:
   - ⚠️ WARNING: Working on main/master directly (consider feature branch)

3. **Worktree Conflicts**
   - Check if `.trees/feature-{NAME}` already exists
   - If exists, check if it's stale (no recent commits)

   **Result**:
   - ❌ FAIL: Worktree already exists (use recovery logic or delete)

### Phase 5: Dependency Check

1. **Required Tools**
   - Check if required CLI tools are installed:
     - git
     - python3
     - Test framework (npm/pytest based on stack)
     - VCS CLI (gh or glab)

   **Command**:
   ```
   which git && which python3 && which npm && which gh
   ```

   **Result**:
   - ❌ FAIL: Critical tools missing (install before continuing)

2. **Project Dependencies**
   - Check if `package-lock.json` or `requirements.txt` exists
   - Verify dependencies are installed:
     - Node: Check `node_modules/` exists
     - Python: Check virtual environment activated

   **Result**:
   - ⚠️ WARNING: Dependencies may not be installed

   **Auto-Fix (v1.1 Enhancement):**
   - If dependencies missing and user approves: Invoke `/dependency-installer` skill
   - The skill will:
     - Auto-detect package manager (npm, pnpm, yarn, pip, poetry, etc.)
     - Install missing dependencies
     - Verify installation success
   - Continue preflight after successful installation

### Phase 6: Test Framework Validation

1. **Test Configuration**
   - Check if test configuration exists:
     - Node: `jest.config.js`, `vitest.config.ts`, `playwright.config.ts`
     - Python: `pytest.ini`, `tox.ini`

   **Result**:
   - ⚠️ WARNING: Test framework not configured (tests may fail)

2. **Test Directory**
   - Verify test directory exists:
     - Node: `tests/`, `__tests__/`, `src/**/*.test.ts`
     - Python: `tests/`, `test_*.py`

   **Result**:
   - ⚠️ WARNING: No test directory found (create before implementing)

### Phase 7: Generate Pre-Flight Report

1. **Invoke Pre-Flight Script**
   ```
   python3 .claude/skills/preflight-check/scripts/preflight.py \
     --feature "{FEATURE_NAME}" \
     --output ".claude/logs/preflight_report.json"
   ```

2. **Aggregate Results**
   - Count PASS, WARNING, FAIL statuses across all checks
   - Determine overall status:
     - **GO**: No FAIL statuses
     - **GO WITH WARNINGS**: Warnings but no FAIL
     - **NO-GO**: At least one FAIL status

3. **Present Report to User**

   **Format**:
   ```
   ================================
   PRE-FLIGHT CHECK REPORT
   ================================

   Feature: user_authentication

   OVERALL STATUS: GO WITH WARNINGS

   ✅ PASS (4):
   - Context file exists and is valid
   - All required agents available
   - Git working tree is clean
   - Required CLI tools installed

   ⚠️ WARNING (2):
   - Methodology workflow not set (defaulting to Standard)
   - Dependencies may not be installed

   ❌ FAIL (0):
   (none)

   RECOMMENDATION: Proceed with caution. Address warnings if possible.
   ```

4. **User Decision**
   - **GO**: Proceed to Phase 1 automatically
   - **GO WITH WARNINGS**: Ask user "Proceed despite warnings? (y/n)"
   - **NO-GO**: Block execution, show detailed errors, suggest fixes

## Integration with flow-feature-build

The pre-flight check is invoked **before Phase 1** of `flow-feature-build`:

```markdown
## Phase 0: Pre-Flight Check (NEW in v3.1)

1. Invoke preflight-check skill
2. Analyze results
3. Decision:
   - GO → Proceed to Phase 0.5
   - GO WITH WARNINGS → Ask user, then proceed or abort
   - NO-GO → Block, show errors, exit
```

## Rules

1. **Never skip pre-flight checks** - Always run before implementation
2. **Fail fast on critical errors** - NO-GO must block execution
3. **User override for warnings** - Allow proceeding with warnings if user accepts risk
4. **Log all checks** - Record results for debugging
5. **Suggest fixes** - Provide actionable guidance for failures

## Examples

### Example 1: All Checks Pass (GO)

**Feature**: Email notification service

**Checks**:
- ✅ Context file: `context_session_feature_email_notifications.md` exists
- ✅ Agents: All required agents available (api-contract-designer, domain-logic-architect)
- ✅ CLAUDE.md: Complete with all sections
- ✅ Git: Working tree clean, on feature branch
- ✅ Dependencies: npm packages installed
- ✅ Tools: git, python3, npm, gh all present

**Result**: GO - Proceed immediately

---

### Example 2: Warnings Present (GO WITH WARNINGS)

**Feature**: User dashboard

**Checks**:
- ✅ Context file exists
- ✅ Agents available
- ⚠️ CLAUDE.md: Methodology workflow not set (will default to Standard)
- ⚠️ Git: 3 uncommitted files (may cause merge conflicts)
- ✅ Dependencies installed
- ⚠️ Tests: No test directory found

**Result**: GO WITH WARNINGS - Ask user to confirm

**User Prompt**:
```
Pre-flight check found 3 warnings:
1. Methodology workflow not set (will use Standard)
2. Uncommitted changes in working tree
3. No test directory found

Proceed despite warnings? (y/n)
```

---

### Example 3: Critical Failures (NO-GO)

**Feature**: Authentication system

**Checks**:
- ❌ Context file: Missing or empty
- ❌ Agents: database-architect not found
- ✅ CLAUDE.md: Valid
- ❌ Git: Merge conflicts detected
- ✅ Dependencies installed
- ❌ Tools: gh CLI not installed

**Result**: NO-GO - Block execution

**Error Report**:
```
❌ PRE-FLIGHT CHECK FAILED

Critical errors detected:

1. Context file missing
   Fix: Run "flow-plan feature authentication_system"

2. Agent not found: database-architect
   Fix: Invoke @agent-librarian to draft agent

3. Merge conflicts detected
   Fix: Resolve conflicts with "git merge --continue" or "git merge --abort"

4. CLI tool missing: gh
   Fix: Install with "npm install -g @github/cli"

Cannot proceed until these errors are resolved.
```

## Version

**Current Version**: 1.3.0
**Last Updated**: 2026-01-17
**Status**: Production

## Changelog

### v1.3.0 (2026-01-17)
- Phase 3.5 now prefers `.claude/cache/modular_index.json` over directory scan
- JSON index provides reliable, structured validation
- Added checksum validation to detect modified files
- Graceful fallback to directory scan if JSON index not found
- Uses size limits from JSON index validation section
- Improved logging to indicate validation source

### v1.2.0 (2026-01-17)
- Added Phase 3.5: Modular Architecture Validation
- Validates modular CLAUDE.md structure (.claude/rules/, .claude/docs/)
- Checks reference integrity in [modular_index]
- Validates path-specific rules YAML frontmatter
- Size compliance checks for modular files
- Auto-detects modular vs monolithic architecture

### v1.1.0 (2026-01-17)
- Integrated `/dependency-installer` skill for auto-fixing missing dependencies
- Updated agent references: presentation-layer-architect → frontend-architect
- Added auto-fix capability with user approval

### v1.0.0 (2026-01-13)
- Initial implementation
- 7 validation phases: Context, Agents, CLAUDE.md, Git, Dependencies, Tests, Report
- Three-tier status: GO, GO WITH WARNINGS, NO-GO
- Integration with flow-feature-build Phase 0
- Actionable error messages with fix suggestions
