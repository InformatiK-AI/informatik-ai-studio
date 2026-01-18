#

# Task: Reload Modular Rules Index

# Argument: (none required)

#

## Metrics Block (START)

# 1. Set START_TIME = current_timestamp
# 2. Set TASK_STATUS = "fail" (default to failure)

## Purpose

Regenerate `.claude/cache/modular_index.json` after rules or docs are modified.
Lightweight alternative to `flow-md-architect audit`.

Use this command when:
- You've added, modified, or deleted rule files
- You've updated documentation files
- You need to refresh checksums without full CLAUDE.md audit
- Cache invalidation is needed for downstream commands

## Phase 1: Validate Prerequisites

1. **Check CLAUDE.md exists:**
   ```
   IF NOT exists("CLAUDE.md"):
     ERROR: "CLAUDE.md not found. Run `/flow-md-architect create` first."
     Exit with error
   ```

2. **Check .claude/rules/ directory exists:**
   ```
   IF NOT exists(".claude/rules/"):
     ERROR: "Modular structure not found. Run `/flow-md-architect create` first."
     Exit with error
   ```

3. **Ensure cache directory exists:**
   ```bash
   mkdir -p .claude/cache
   ```

## Phase 2: Scan Files

### 2.1 Compute Checksums Function

```python
import hashlib

def compute_checksum(file_path):
    """Compute truncated SHA256 checksum for cache invalidation."""
    with open(file_path, 'rb') as f:
        full_hash = hashlib.sha256(f.read()).hexdigest()
        return f"sha256:{full_hash[:16]}"
```

**Alternative (Bash):**
```bash
CHECKSUM=$(sha256sum "$FILE_PATH" | cut -c1-16)
echo "sha256:$CHECKSUM"
```

### 2.2 Scan Auto-Loaded Rules

```
AUTO_LOADED = []
For each file in .claude/rules/*.md (excluding domain/):
  checksum = compute_checksum(file)
  priority = "high" if filename in [code-standards, testing-policy, security-policy] else "medium"
  purpose = extract_from_header(file)  # First comment or heading

  AUTO_LOADED.append({
    file: relative_path,
    priority: priority,
    purpose: purpose,
    required: priority == "high",
    checksum: checksum
  })
```

### 2.3 Scan Path-Specific Rules

```
PATH_SPECIFIC = []
For each file in .claude/rules/domain/*.md:
  checksum = compute_checksum(file)
  frontmatter = parse_yaml_frontmatter(file)

  PATH_SPECIFIC.append({
    file: relative_path,
    paths: frontmatter.paths or [],
    purpose: frontmatter.purpose or extract_from_header(file),
    required: false,
    checksum: checksum
  })
```

### 2.4 Scan On-Demand Docs

```
ON_DEMAND = []
For each file in .claude/docs/**/*.md:
  checksum = compute_checksum(file)

  # Infer load_when from path
  IF path contains "architecture":
    load_when = "Schema/API changes"
  ELSE IF path contains "patterns":
    load_when = "Pattern lookup"
  ELSE IF path contains "guides":
    load_when = "Setup/deployment tasks"
  ELSE:
    load_when = "On request"

  ON_DEMAND.append({
    file: relative_path,
    load_when: load_when,
    purpose: extract_from_header(file),
    required: false,
    checksum: checksum
  })
```

## Phase 3: Generate Index

1. **Build modular_index.json:**

   ```json
   {
     "version": "1.0",
     "created": "{ISO_TIMESTAMP}",
     "architecture_mode": "modular",
     "source_claude_md": "CLAUDE.md",

     "auto_loaded": [...AUTO_LOADED],

     "path_specific": [...PATH_SPECIFIC],

     "on_demand": [...ON_DEMAND],

     "validation": {
       "generated_at": "{ISO_TIMESTAMP}",
       "total_files": AUTO_LOADED.length + PATH_SPECIFIC.length + ON_DEMAND.length,
       "total_checksums": AUTO_LOADED.length + PATH_SPECIFIC.length + ON_DEMAND.length,
       "required_files": count where required == true,
       "optional_files": count where required == false
     }
   }
   ```

2. **Write to file:**
   ```
   Write JSON to .claude/cache/modular_index.json
   Log: "Modular index regenerated: .claude/cache/modular_index.json"
   ```

## Phase 4: Invalidate Stale Caches

1. **Find context cache files:**
   ```
   STALE_CACHES = []
   For each file in .claude/cache/context_*.json:
     IF file.modified_time < modular_index.json.created:
       STALE_CACHES.append(file)
   ```

2. **Delete stale caches:**
   ```
   For each file in STALE_CACHES:
     Delete file
     Log: "Invalidated: {file}"
   ```

3. **Report invalidation:**
   ```
   IF STALE_CACHES.length > 0:
     Log: "Invalidated {STALE_CACHES.length} stale cache file(s)"
   ELSE:
     Log: "No stale caches found"
   ```

## Phase 5: Report Summary

```
=== MODULAR INDEX RELOAD COMPLETE ===

Files indexed:
  - Auto-loaded rules: {AUTO_LOADED.length}
  - Path-specific rules: {PATH_SPECIFIC.length}
  - On-demand docs: {ON_DEMAND.length}
  - Total: {total_files}

Checksums generated: {total_checksums}
Caches invalidated: {STALE_CACHES.length} file(s)

Index location: .claude/cache/modular_index.json
```

## Metrics Block (END)

# 1. Set END_TIME = current_timestamp
# 2. Set TASK_STATUS = "success"
# 3. Call `python3 .claude/scripts/log_metric.py` silently with:
#    - command: "flow-reload-rules"
#    - files_indexed: total_files
#    - checksums_generated: total_checksums
#    - caches_invalidated: STALE_CACHES.length
#    - status: TASK_STATUS
#    - start_time: START_TIME
#    - end_time: END_TIME

## Usage Examples

```bash
# After modifying a rule file
/flow-reload-rules

# Verify checksums updated
cat .claude/cache/modular_index.json | grep checksum
```

## Notes

- This command is faster than `flow-md-architect audit` as it only regenerates the index
- Does not validate CLAUDE.md structure or content
- Use `flow-md-architect audit` for full validation
- Checksums enable downstream commands to detect when rules have changed

## Command Metadata

- **Version:** 1.0
- **Created:** 2026-01-17
- **Last Updated:** 2026-01-17
- **Dependencies:** None
- **Related Commands:** flow-md-architect, flow-feature-build

## Changelog

### v1.0 (2026-01-17)
- Initial implementation
- Scans auto-loaded, path-specific, and on-demand files
- Generates SHA256 checksums (truncated to 16 chars)
- Invalidates stale context caches
