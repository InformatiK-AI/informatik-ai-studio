#

# Task: Git Worktree Recovery Module (v1.0)

# This is a modular component of flow-feature-build.md
# Do not invoke directly - called by flow-feature-build when worktree creation fails

#

## Worktree Recovery Logic

**Purpose**: Handle existing worktree conflicts gracefully with user-guided recovery options.

### Prerequisites

- Git worktree creation failed with "already exists" error
- Feature argument: $ARG (e.g., issue number or feature name)
- Worktree path: `.trees/feature-$ARG`

### Phase WR-1: Detect Existing Worktree

1. **Verify Worktree Exists:**
   ```bash
   git worktree list | grep ".trees/feature-$ARG"
   ```

2. **If Not Found:**
   - Error is something else (not existing worktree)
   - Show raw git error and abort

### Phase WR-2: Analyze Worktree State

1. **Gather Worktree Information:**
   ```bash
   # Last commit date
   LAST_COMMIT=$(git -C ./.trees/feature-$ARG log -1 --format="%ar" 2>/dev/null || echo "unknown")

   # Uncommitted changes count
   CHANGES=$(git -C ./.trees/feature-$ARG status --porcelain 2>/dev/null | wc -l)

   # Branch status
   BRANCH_STATUS=$(git -C ./.trees/feature-$ARG status -sb 2>/dev/null | head -1)

   # Check if branch is ahead/behind
   SYNC_STATUS=$(git -C ./.trees/feature-$ARG status -sb 2>/dev/null | grep -o '\[.*\]' || echo "in sync")
   ```

2. **Build State Summary:**
   ```json
   {
     "worktree_path": ".trees/feature-{ARG}",
     "last_commit": "{LAST_COMMIT}",
     "uncommitted_changes": {CHANGES},
     "branch": "{BRANCH_STATUS}",
     "sync_status": "{SYNC_STATUS}"
   }
   ```

### Phase WR-3: Present Recovery Options

**Display to User:**
```
⚠️ Worktree already exists: .trees/feature-{ARG}

Worktree Info:
- Last commit: {LAST_COMMIT}
- Uncommitted changes: {CHANGES} files
- Branch: {BRANCH_STATUS}
- Sync status: {SYNC_STATUS}

Recovery Options:
a) Delete and recreate (FRESH START)
   - Will DELETE all uncommitted work
   - Creates new branch from current HEAD
   - Use when: Previous work is abandoned

b) Continue in existing worktree (RESUME)
   - Keeps all existing work
   - Continues from current state
   - Use when: Resuming interrupted work

c) Abort command (EXIT)
   - No changes made
   - Manual cleanup required
   - Use when: Need to review worktree manually

Choose option (a/b/c):
```

### Phase WR-4: Handle User Choice

#### Option A: Delete and Recreate (FRESH START)

```bash
# Step 1: Remove worktree (force if has uncommitted changes)
git worktree remove ./.trees/feature-$ARG --force

# Step 2: Delete branch if exists
git branch -D feature-$ARG 2>/dev/null || true

# Step 3: Create fresh worktree
git worktree add ./.trees/feature-$ARG -b feature-$ARG

# Step 4: Log action
echo "✅ Worktree recreated from scratch"
```

**Post-Action:**
- Set WORKTREE_RECOVERY = "recreated"
- Return to flow-feature-build Phase 1 (continue with fresh worktree)

#### Option B: Continue in Existing (RESUME)

```bash
# Step 1: Change to existing worktree
cd ./.trees/feature-$ARG

# Step 2: Show current status
git status

# Step 3: Show recent commits
git log --oneline -5

# Step 4: Warning about existing state
echo "⚠️ Continuing with existing worktree. Review uncommitted changes above."
```

**Post-Action:**
- Set WORKTREE_RECOVERY = "resumed"
- Show user the current state
- Return to flow-feature-build Phase 2 (skip constitution read, use existing context)

#### Option C: Abort (EXIT)

```bash
# Step 1: Show cleanup instructions
echo "Command aborted. To clean up manually:"
echo "  git worktree remove ./.trees/feature-$ARG"
echo "  git branch -D feature-$ARG"

# Step 2: Set status and exit
TASK_STATUS = "aborted"
exit 1
```

**Post-Action:**
- Set WORKTREE_RECOVERY = "aborted"
- Set TASK_STATUS = "aborted"
- Exit flow-feature-build entirely

### Phase WR-5: Log Recovery Metrics

```python
log_metric({
    "command": "flow-worktree-recovery",
    "worktree_path": ".trees/feature-{ARG}",
    "recovery_action": WORKTREE_RECOVERY,  # "recreated" | "resumed" | "aborted"
    "uncommitted_changes": CHANGES,
    "last_commit_age": LAST_COMMIT,
    "timestamp": current_timestamp
})
```

### Error Handling

**If worktree removal fails:**
```
Error: Cannot remove worktree. Possible causes:
- Worktree is currently checked out in another terminal
- File system permissions issue
- Files are locked by another process

Suggested actions:
1. Close any editors/terminals using this worktree
2. Run: git worktree remove ./.trees/feature-{ARG} --force
3. If still failing, manually delete the directory
```

**If branch deletion fails:**
```
Warning: Could not delete branch feature-{ARG}.
This may mean the branch doesn't exist locally (expected if worktree was only partially created).
Continuing with worktree creation...
```

---

## Version

**Version**: 1.0.0
**Extracted From**: flow-feature-build.md v3.3
**Created**: 2026-01-17
