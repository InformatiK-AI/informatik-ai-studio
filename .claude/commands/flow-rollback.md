#

# Task: Feature Rollback Handler (v1.0)

# Argument: $ARGUMENTS (feature_name [--mode soft|hard])

#

## Purpose

Provides rollback functionality when feature implementation fails mid-way. Cleans up worktrees, reverts commits, and resets state files to a known-good state.

## Metrics Block (START)

# 1. Set START_TIME = current_timestamp
# 2. Set TASK_STATUS = "fail" (default to failure)
# 3. Set ROLLBACK_MODE = "soft" (default)

## Phase 0: Argument Parsing

1. **Extract feature name:**
   ```
   FEATURE_NAME = first argument from $ARGUMENTS
   ```

2. **Extract mode (optional):**
   ```
   IF "--mode hard" in $ARGUMENTS:
     ROLLBACK_MODE = "hard"
   ELSE IF "--mode soft" in $ARGUMENTS:
     ROLLBACK_MODE = "soft"
   ELSE:
     ROLLBACK_MODE = "soft"  # Default
   ```

3. **Validate feature exists:**
   ```
   Check for any of:
   - .trees/feature-{FEATURE_NAME} (worktree)
   - .claude/docs/{FEATURE_NAME}/ (plans)
   - .claude/state/{FEATURE_NAME}/ (state files)

   IF none exist:
     Error: "Feature '{FEATURE_NAME}' not found. Nothing to rollback."
     EXIT
   ```

## Phase 1: State Analysis

1. **Gather current state:**
   ```bash
   # Check worktree existence
   WORKTREE_EXISTS = git worktree list | grep "feature-{FEATURE_NAME}"

   # Check for uncommitted changes
   IF WORKTREE_EXISTS:
     UNCOMMITTED_CHANGES = git -C .trees/feature-{FEATURE_NAME} status --porcelain | wc -l

   # Check for commits on feature branch
   COMMITS_ON_BRANCH = git log main..feature-{FEATURE_NAME} --oneline | wc -l

   # Check for open PR
   PR_EXISTS = gh pr list --head feature-{FEATURE_NAME} --json number
   ```

2. **Build state summary:**
   ```json
   {
     "feature_name": "{FEATURE_NAME}",
     "worktree_exists": true/false,
     "uncommitted_changes": N,
     "commits_on_branch": N,
     "pr_exists": true/false,
     "pr_number": N or null,
     "plans_exist": true/false,
     "state_files_exist": true/false
   }
   ```

3. **Display state to user:**
   ```
   Feature Rollback Analysis: {FEATURE_NAME}

   Current State:
   - Worktree: {EXISTS/NOT FOUND}
   - Uncommitted changes: {N} files
   - Commits on branch: {N}
   - Open PR: {#N or NONE}
   - Agent plans: {EXIST/NOT FOUND}
   - State files: {EXIST/NOT FOUND}

   Rollback Mode: {ROLLBACK_MODE}
   ```

## Phase 2: Rollback Options

### Mode: SOFT (Default)

**Preserves commits and PR, only cleans up local state.**

1. **Preserve work:**
   - Keep commits on feature branch
   - Keep open PR (if exists)
   - Stash uncommitted changes

2. **Clean up local state:**
   ```bash
   # Stash uncommitted changes (if any)
   IF UNCOMMITTED_CHANGES > 0:
     cd .trees/feature-{FEATURE_NAME}
     git stash push -m "rollback-stash-{timestamp}"
     echo "Uncommitted changes stashed"

   # Remove worktree but keep branch
   git worktree remove .trees/feature-{FEATURE_NAME}
   ```

3. **Archive state files:**
   ```bash
   # Move state files to archive
   mkdir -p .claude/archive/{FEATURE_NAME}/{timestamp}
   mv .claude/docs/{FEATURE_NAME}/* .claude/archive/{FEATURE_NAME}/{timestamp}/
   mv .claude/state/{FEATURE_NAME}/* .claude/archive/{FEATURE_NAME}/{timestamp}/
   mv .claude/cache/context_{FEATURE_NAME}.json .claude/archive/{FEATURE_NAME}/{timestamp}/
   ```

4. **Output:**
   ```
   ✅ Soft rollback complete for '{FEATURE_NAME}'

   Preserved:
   - Feature branch: feature-{FEATURE_NAME}
   - Commits: {N}
   - PR: #{PR_NUMBER} (if exists)
   - Stashed changes: rollback-stash-{timestamp}

   Cleaned up:
   - Worktree removed
   - Plans archived to .claude/archive/{FEATURE_NAME}/{timestamp}/
   - State files archived

   To resume work later:
     git worktree add .trees/feature-{FEATURE_NAME} feature-{FEATURE_NAME}
     cd .trees/feature-{FEATURE_NAME}
     git stash pop
   ```

### Mode: HARD

**Completely removes all traces of the feature. DESTRUCTIVE.**

1. **Confirm with user:**
   ```
   ⚠️ HARD ROLLBACK WARNING

   This will PERMANENTLY DELETE:
   - All commits on feature-{FEATURE_NAME} branch
   - The feature branch itself
   - All uncommitted changes
   - All agent plans and state files
   - Close PR #{PR_NUMBER} (if exists)

   This action CANNOT be undone.

   Type 'DELETE {FEATURE_NAME}' to confirm:
   ```

2. **Close PR (if exists):**
   ```bash
   IF PR_EXISTS:
     gh pr close {PR_NUMBER} --comment "Closed by flow-rollback (hard mode)"
   ```

3. **Remove worktree and branch:**
   ```bash
   # Force remove worktree (including uncommitted changes)
   git worktree remove .trees/feature-{FEATURE_NAME} --force

   # Delete feature branch (force to delete unmerged)
   git branch -D feature-{FEATURE_NAME}
   ```

4. **Delete all state files:**
   ```bash
   rm -rf .claude/docs/{FEATURE_NAME}/
   rm -rf .claude/state/{FEATURE_NAME}/
   rm -f .claude/cache/context_{FEATURE_NAME}.json
   rm -rf .claude/sessions/context_session_*_{FEATURE_NAME}.md
   ```

5. **Output:**
   ```
   ✅ Hard rollback complete for '{FEATURE_NAME}'

   Deleted:
   - Worktree: .trees/feature-{FEATURE_NAME}
   - Branch: feature-{FEATURE_NAME}
   - Commits: {N} (permanently deleted)
   - PR: #{PR_NUMBER} (closed)
   - All plans and state files

   The feature has been completely removed.
   ```

## Phase 3: Cleanup Verification

1. **Verify cleanup:**
   ```bash
   # Check nothing remains
   WORKTREE_CHECK = git worktree list | grep "feature-{FEATURE_NAME}" || true
   BRANCH_CHECK = git branch --list "feature-{FEATURE_NAME}" || true
   DOCS_CHECK = ls .claude/docs/{FEATURE_NAME}/ 2>/dev/null || true

   IF any checks return content:
     Warning: "Some artifacts may still exist. Manual cleanup may be needed."
   ```

2. **Log rollback action:**
   ```
   python3 .claude/scripts/log_metric.py with:
   - command: "flow-rollback"
   - feature_name: {FEATURE_NAME}
   - mode: {ROLLBACK_MODE}
   - commits_removed: {N} (for hard mode)
   - pr_closed: {PR_NUMBER or null}
   - status: "success"
   ```

## Metrics Block (END)

# 1. Set END_TIME = current_timestamp
# 2. Set TASK_STATUS = "success"
# 3. Call `python3 .claude/scripts/log_metric.py` silently with:
#    - command: "flow-rollback"
#    - feature_name: $FEATURE_NAME
#    - mode: $ROLLBACK_MODE
#    - status: $TASK_STATUS
#    - start_time: $START_TIME
#    - end_time: $END_TIME

---

## Usage Examples

```bash
# Soft rollback (default) - preserves commits and PR
claude -p .claude/commands/flow-rollback.md my-feature

# Hard rollback - deletes everything
claude -p .claude/commands/flow-rollback.md my-feature --mode hard
```

## Version

**Version**: 1.0.0
**Created**: 2026-01-17
**Related Commands**: flow-feature-build, flow-worktree-recovery
