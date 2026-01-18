# Pre-Flight Check Skill

## Overview

The **Pre-Flight Check** skill is a comprehensive validation system that runs before `flow-feature-build` begins. It acts as a safety gate, catching common issues early and preventing wasted effort on implementations that are doomed to fail.

Think of it as an airplane pre-flight checklist: you don't take off without verifying everything is ready.

## Why This Skill Exists

### Problem It Solves

Without pre-flight checks, teams often encounter:

- ❌ Starting implementation only to find context file is missing
- ❌ Invoking agents that don't exist in the project
- ❌ Working with incomplete or invalid CLAUDE.md
- ❌ Merge conflicts blocking git worktree creation
- ❌ Missing dependencies causing test failures
- ❌ CLI tools not installed, breaking automation

**Result**: Wasted time, frustration, and failed implementations.

### How It Solves It

The pre-flight checker validates **7 critical areas** before allowing implementation to proceed:

1. **Context Files** - Feature plans exist and are complete
2. **Agent Availability** - Required agents are present
3. **CLAUDE.md** - Project constitution is valid
4. **Git Status** - Working tree is clean, no conflicts
5. **Dependencies** - npm/pip packages installed
6. **Test Framework** - Tests configured correctly
7. **Required Tools** - CLI tools (git, gh, python) available

**Result**: Issues caught in seconds, not hours.

## When It's Used

### Automatic Invocation

The pre-flight check is **automatically invoked** at the start of `flow-feature-build` (before Phase 1):

```
flow-feature-build (receives feature name)
  ├─> Phase 0: Pre-Flight Check ← Runs here automatically
  │     ├─> 7 validation checks
  │     ├─> Generate report
  │     └─> Decides: GO / GO WITH WARNINGS / NO-GO
  ├─> Phase 0.5: Load Shared Context (if GO/GO WITH WARNINGS)
  ├─> Phase 1: Constitution & Setup
  └─> ... (rest of workflow)
```

### Manual Invocation

You can also manually run pre-flight checks:

```bash
# Via Claude
"Run preflight-check for feature user_auth"

# Or directly
python3 .claude/skills/preflight-check/scripts/preflight.py \
  --feature "user_auth" \
  --output "preflight_report.json"
```

## How It Works

### Validation Phases

#### Phase 1: Context Validation
- ✅ Check `context_session_feature_{NAME}.md` exists
- ✅ Validate file is not empty
- ✅ Verify required sections (Overview, Objectives)
- ⚠️ Check for placeholder text (TODO, TBD)

#### Phase 2: Agent Availability
- ✅ Detect required agents from context
- ✅ Verify agent files exist in `.claude/agents/`
- ✅ Validate YAML front matter

#### Phase 3: CLAUDE.md Validation
- ✅ Check file exists at project root
- ✅ Verify required sections: [stack], [methodology], [core_team]
- ✅ Validate methodology workflow is set (TDD/RAD/Standard)

#### Phase 4: Git Status
- ✅ Check working tree is clean
- ✅ Detect uncommitted changes
- ❌ Detect merge conflicts (blocking)
- ❌ Check if worktree already exists (blocking)

#### Phase 5: Dependency Check
- ✅ Check Node.js: node_modules/ exists
- ✅ Check Python: virtual environment activated
- ⚠️ Warn if dependencies may not be installed

#### Phase 6: Test Framework
- ✅ Check for test configuration (jest.config.js, pytest.ini, etc.)
- ✅ Verify test directory exists (tests/, __tests__/)

#### Phase 7: Required Tools
- ✅ Check git is installed
- ✅ Check python3 is installed
- ✅ Check gh (GitHub CLI) is installed
- ❌ Fail if critical tools missing

### Status Levels

The pre-flight checker uses a **three-tier status system**:

| Status | Meaning | Action |
|--------|---------|--------|
| **GO** | All checks passed | Proceed automatically |
| **GO WITH WARNINGS** | Warnings but no failures | Ask user to confirm |
| **NO-GO** | Critical failures detected | Block execution |

### Report Format

```
================================
PRE-FLIGHT CHECK REPORT
================================

Feature: user_authentication

OVERALL STATUS: GO WITH WARNINGS

✅ PASS (5):
  - Context file exists and is valid
  - All required agents available
  - CLAUDE.md valid, workflow: TDD
  - Working tree is clean
  - All required CLI tools available

⚠️ WARNING (2):
  - Missing sections: Test Strategy
  - node_modules/ not found
    Fix: Run: npm install

❌ FAIL (0):
  (none)

RECOMMENDATION: ⚠️ Proceed with caution. Address warnings if possible.
```

## Examples

### Example 1: Perfect Setup (GO)

**Scenario**: Email notification service, all preconditions met

**Checks**:
- ✅ Context file exists with complete sections
- ✅ All required agents available
- ✅ CLAUDE.md complete and valid
- ✅ Git working tree clean
- ✅ Dependencies installed (node_modules/)
- ✅ Test framework configured (jest.config.js)
- ✅ All tools installed (git, python3, gh)

**Result**: **GO** - Proceeds automatically to Phase 0.5

---

### Example 2: Minor Issues (GO WITH WARNINGS)

**Scenario**: User dashboard, some warnings present

**Checks**:
- ✅ Context file exists
- ✅ Agents available
- ⚠️ CLAUDE.md: Methodology workflow not set
- ⚠️ Git: 3 uncommitted files
- ⚠️ Dependencies: node_modules/ not found
- ✅ Test framework configured
- ✅ Tools installed

**Result**: **GO WITH WARNINGS**

**User Prompt**:
```
Pre-flight check found 3 warnings:
1. Methodology workflow not set (will use Standard)
2. Uncommitted changes in working tree
3. Dependencies may not be installed

Proceed despite warnings? (y/n)
```

**If user selects "y"**: Proceed to Phase 0.5
**If user selects "n"**: Abort, allow user to address warnings

---

### Example 3: Critical Failures (NO-GO)

**Scenario**: Authentication system, multiple critical issues

**Checks**:
- ❌ Context file: Missing
- ❌ Agents: database-architect not found
- ✅ CLAUDE.md: Valid
- ❌ Git: Merge conflicts detected
- ✅ Dependencies: Installed
- ✅ Test framework configured
- ❌ Tools: gh CLI not installed

**Result**: **NO-GO** - Execution blocked

**Error Report**:
```
❌ PRE-FLIGHT CHECK FAILED

Critical errors detected:

1. Context file missing
   Fix: Run: flow-plan feature authentication_system

2. Agent not found: database-architect
   Fix: Invoke @agent-librarian to draft agent

3. Merge conflicts detected
   Fix: Resolve conflicts with "git merge --continue" or "git merge --abort"

4. CLI tool missing: gh
   Fix: Install with: npm install -g @github/cli

Cannot proceed until these errors are resolved.
```

**User must fix errors and re-run pre-flight before continuing.**

## Integration with flow-feature-build

The pre-flight check is invoked at the very start of `flow-feature-build`:

```markdown
## Phase 0: Pre-Flight Check (NEW in v3.1)

1. Invoke preflight-check skill
   ```
   Use preflight-check skill for feature {FEATURE_NAME}
   ```

2. Analyze Results
   - Read pre-flight report
   - Count PASS/WARNING/FAIL statuses

3. Decision Logic
   - **GO**: Proceed to Phase 0.5 (Load Shared Context)
   - **GO WITH WARNINGS**:
     - Show warnings to user
     - Ask: "Proceed despite warnings? (y/n)"
     - If yes → Phase 0.5
     - If no → Abort, allow user to fix
   - **NO-GO**:
     - Block execution
     - Show detailed error report
     - Exit flow-feature-build

4. Log Pre-Flight Metrics
   ```
   python3 .claude/scripts/log_metric.py with:
   - preflight_status: GO/GO_WITH_WARNINGS/NO_GO
   - pass_count: N
   - warning_count: N
   - fail_count: N
   ```
```

## Files Structure

```
.claude/skills/preflight-check/
├── SKILL.md                    # Main skill logic (Claude reads this)
├── README.md                   # This file (human documentation)
└── scripts/
    └── preflight.py            # Pre-flight validation script
```

## Benefits

### Before Pre-Flight Checks

- ❌ Issues discovered mid-implementation
- ❌ Wasted time on doomed implementations
- ❌ Frustration from preventable errors
- ❌ No clear guidance on what's wrong

### After Pre-Flight Checks

- ✅ Issues caught in seconds (before implementation)
- ✅ Clear GO/NO-GO decision point
- ✅ Actionable fix suggestions for all failures
- ✅ Confidence that implementation will succeed

**Time Saved**: 10-30 minutes per feature (average)

## Extending Pre-Flight Checks

You can add custom checks by editing `scripts/preflight.py`:

```python
def check_custom_validation(self):
    """Add your custom check here."""
    # Your validation logic
    if validation_fails:
        self.report.checks.append(CheckResult(
            check_name="Custom Check",
            status="FAIL",
            message="Validation failed",
            fix_suggestion="How to fix this issue"
        ))
```

Common custom checks:
- Environment variables set
- Database connection available
- External API keys configured
- Docker daemon running
- Specific file structure present

## Troubleshooting

### Issue: Pre-flight always shows "Context file missing"

**Cause**: Context file naming mismatch

**Solution**: Ensure context file follows naming pattern:
- `context_session_feature_{feature_name}.md`
- Feature name must match exactly (underscores, not hyphens)

---

### Issue: "Agent not found" but agent exists

**Cause**: Agent file name doesn't match expected pattern

**Solution**: Rename agent file to match pattern:
- File: `.claude/agents/database-architect.md`
- Name in file: `name: database-architect`

---

### Issue: Pre-flight takes too long

**Cause**: Slow git operations or network checks

**Solution**: Skip non-critical checks with environment variable:
```bash
PREFLIGHT_SKIP_SLOW=1 python3 preflight.py --feature "name"
```

## Version History

### v1.0.0 (2026-01-13) - Initial Release

- 7 validation phases
- Three-tier status system (GO/GO WITH WARNINGS/NO-GO)
- Integration with flow-feature-build Phase 0
- Actionable error messages with fix suggestions
- JSON report output for automation

## References

- `SKILL.md` - Main skill logic and workflow
- `scripts/preflight.py` - Validation implementation
- `.claude/commands/flow-feature-build.md` - Integration point (Phase 0)
- `CLAUDE.md` - Project constitution

---

**Status**: Production
**Maintainer**: Genesis Factory Core Team
**Last Updated**: 2026-01-13
