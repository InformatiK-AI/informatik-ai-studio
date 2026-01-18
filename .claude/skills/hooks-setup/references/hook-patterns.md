# Git Hook Patterns and Customization

This reference provides detailed information on Git hook patterns, customization strategies, and merge approaches for the hooks-setup skill.

## Hook Lifecycle and Timing

### Pre-commit Hook

**When it runs**: Before commit is created, after `git commit` is executed
**Purpose**: Validate code quality on staged files only
**Typical checks**:

- Linting (ESLint, stylelint)
- Formatting (Prettier)
- Type checking (TypeScript)
- Unit tests for changed files (optional)

**Best practices**:

- Keep it fast (< 10 seconds) to not disrupt developer flow
- Only check staged files using lint-staged
- Auto-fix when possible (--fix flags)
- Provide clear error messages

### Commit-msg Hook

**When it runs**: After commit message is entered, before commit is created
**Purpose**: Validate commit message format
**Typical checks**:

- Conventional Commits format validation
- Message length requirements
- Issue/ticket reference validation
- Prohibited words/patterns

**Best practices**:

- Use commitlint for standardized validation
- Provide helpful error messages with examples
- Support commit message templates
- Allow bypass for emergency fixes (with warning)

### Pre-push Hook

**When it runs**: Before push to remote, after local commits
**Purpose**: Run comprehensive checks before code reaches remote
**Typical checks**:

- Full test suite
- Type checking across entire codebase
- Build verification
- Integration tests
- Security scans (optional)

**Best practices**:

- Can be slower than pre-commit (< 2 minutes ideal)
- Prevent broken code from reaching remote
- Cache test results when possible
- Allow bypass with warning for urgent fixes

## Lint-staged Patterns

### Basic Configuration

```javascript
module.exports = {
  "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.css": ["stylelint --fix", "prettier --write"],
  "*.md": ["prettier --write"],
};
```

### Advanced Patterns

#### Running Different Commands by File Type

```javascript
module.exports = {
  // Frontend files
  "src/components/**/*.{ts,tsx}": [
    "eslint --fix",
    "prettier --write",
    () => "tsc --noEmit", // Type check entire project
  ],

  // Backend files
  "src/api/**/*.ts": [
    "eslint --fix",
    "prettier --write",
    "jest --findRelatedTests", // Run related tests
  ],

  // Astro components
  "*.astro": [
    "eslint --fix",
    "prettier --write --plugin=prettier-plugin-astro",
  ],
};
```

#### Conditional Execution

```javascript
module.exports = {
  "*.{ts,tsx}": (files) => {
    const testFiles = files.filter((f) => f.includes(".test."));
    const srcFiles = files.filter((f) => !f.includes(".test."));

    const commands = [];

    if (srcFiles.length > 0) {
      commands.push(`eslint --fix ${srcFiles.join(" ")}`);
      commands.push("tsc --noEmit");
    }

    if (testFiles.length > 0) {
      commands.push(`jest ${testFiles.join(" ")}`);
    }

    return commands;
  },
};
```

#### Project-Specific Paths

```javascript
module.exports = {
  // Only lint source files, ignore build output
  "src/**/*.{js,ts}": ["eslint --fix"],

  // Validate JSON schemas
  "schemas/**/*.json": ["ajv validate"],

  // Check markdown links
  "docs/**/*.md": ["markdown-link-check"],
};
```

## Commitlint Configuration Patterns

### Custom Scopes

```javascript
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "scope-enum": [
      2,
      "always",
      ["hero", "features", "animations", "ui", "api", "deps", "config"],
    ],
  },
};
```

### Custom Types

```javascript
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "test",
        "chore",
        "wip", // Work in progress
        "hotfix", // Emergency fix
      ],
    ],
  },
};
```

### Project-Specific Rules

```javascript
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "header-max-length": [2, "always", 72],
    "body-max-line-length": [2, "always", 100],
    "subject-case": [2, "always", "sentence-case"],

    // Require ticket reference in footer
    "footer-max-line-length": [0],
    "references-empty": [2, "never"],
  },
  parserPreset: {
    parserOpts: {
      referenceActions: null,
      issuePrefixes: ["JIRA-", "GH-"],
    },
  },
};
```

## Hook Merge Strategies

### Strategy 1: Append New Commands

**Use when**: Adding new checks without modifying existing behavior

```bash
# Existing pre-commit
pnpm lint

# After merge
pnpm lint
pnpm test:unit  # New command appended
```

**Implementation**:

- Read existing hook file
- Check if new commands already exist
- Append new commands with comment marker
- Preserve existing commands

### Strategy 2: Replace Entire Hook

**Use when**: Completely redefining hook behavior

**Considerations**:

- Backup existing hook before replacing
- Notify user of replacement
- Provide option to restore backup

### Strategy 3: Smart Merge with Sections

**Use when**: Managing complex hooks with multiple responsibilities

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# ===== Linting =====
pnpm lint

# ===== Testing =====
pnpm test:unit

# ===== Custom User Commands =====
# User commands below this line
```

**Implementation**:

- Define sections with comment markers
- Allow users to add custom commands in designated section
- Update managed sections during merges
- Preserve user section

### Strategy 4: Hook Composition

**Use when**: Multiple tools want to manage hooks

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run all hook scripts in .husky/pre-commit.d/
for script in .husky/pre-commit.d/*; do
  if [ -f "$script" ] && [ -x "$script" ]; then
    "$script" || exit 1
  fi
done
```

**Benefits**:

- Each tool manages its own script file
- No conflicts between tools
- Easy to add/remove checks
- Clear ownership

## Common Customizations

### Skip Hooks for Emergency Fixes

```bash
# Skip pre-commit and commit-msg hooks
git commit --no-verify -m "hotfix: critical bug"

# Skip pre-push hook
git push --no-verify
```

**Recommendation**: Log bypass events and require justification

### Conditional Hook Execution

```bash
# In pre-commit hook
#!/usr/bin/env sh

# Skip if WIP commit
if git log -1 --pretty=%B | grep -q "^wip:"; then
  echo "WIP commit detected, skipping lint checks"
  exit 0
fi

# Run normal checks
pnpm lint-staged
```

### Performance Optimization

```bash
# Cache test results
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Only run tests if test files or source files changed
if git diff --cached --name-only | grep -qE '\.(test|spec)\.(ts|tsx)$|^src/'; then
  pnpm test
else
  echo "No relevant changes, skipping tests"
fi
```

### CI/CD Integration

Ensure hooks run the same checks as CI:

```yaml
# .github/workflows/ci.yml
- name: Lint
  run: pnpm lint-staged

- name: Validate commits
  run: pnpm commitlint --from=HEAD~1

- name: Tests
  run: pnpm test
```

## Troubleshooting

### Hook Not Executing

1. Check hook file has execute permissions: `chmod +x .husky/pre-commit`
2. Verify Husky is initialized: `.husky/_/husky.sh` exists
3. Check package.json has `"prepare": "husky"` script
4. Reinstall hooks: `pnpm exec husky install`

### Hook Failing Incorrectly

1. Test commands manually: `pnpm lint-staged`
2. Check file patterns in lint-staged config
3. Verify all tools are installed: `pnpm install`
4. Review error messages for specific failures

### Slow Hook Execution

1. Profile each command: Add `time` before commands
2. Reduce scope: Lint only staged files
3. Parallelize checks: Use `concurrently` or `npm-run-all`
4. Cache results: Use tool-specific caching (Jest, ESLint)

### Bypass Hooks (Development Only)

```bash
# Disable Husky temporarily
export HUSKY=0
git commit -m "message"

# Re-enable
unset HUSKY
```

## Best Practices Summary

1. **Keep pre-commit fast**: Use lint-staged for incremental checks
2. **Provide clear feedback**: Show which check failed and how to fix
3. **Allow bypass with warning**: Don't completely block developers
4. **Document customizations**: Add comments in hook files
5. **Test hooks locally**: Before pushing changes
6. **Sync with CI**: Hooks should mirror CI checks
7. **Version control**: Commit hook configurations to repo
8. **Educate team**: Ensure everyone understands hook purpose
9. **Monitor performance**: Track hook execution time
10. **Iterate based on feedback**: Adjust rules as team learns
