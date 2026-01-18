# Claude Code Hook Patterns Reference

## Purpose

Comprehensive guide to Claude Code hooks configuration, patterns, and troubleshooting. Use this reference for advanced customizations beyond the basic setup.

---

## Table of Contents

1. [Hook Types and Lifecycle](#hook-types-and-lifecycle)
2. [PostToolUse Hook Patterns](#posttooluse-hook-patterns)
3. [Matcher Patterns](#matcher-patterns)
4. [Multi-Language Configurations](#multi-language-configurations)
5. [Advanced Patterns](#advanced-patterns)
   - [Dependency Security Analysis](#dependency-security-analysis)
   - [Conditional Linting by Directory](#conditional-linting-by-directory)
   - [Skip Certain Directories](#skip-certain-directories)
   - [Chain Multiple Tools](#chain-multiple-tools)
   - [Package Manager Detection](#package-manager-detection)
   - [Multiple Hooks](#multiple-hooks)
6. [Performance Optimization](#performance-optimization)
7. [Troubleshooting](#troubleshooting)
8. [Integration with Git Hooks](#integration-with-git-hooks)
9. [Next.js Framework-Specific Patterns](#nextjs-framework-specific-patterns)
   - [App Router Convention Validation](#app-router-convention-validation)
   - [Server/Client Component Pattern Validation](#serverclient-component-pattern-validation)
   - [Next.js Import Pattern Validation](#nextjs-import-pattern-validation)
   - [Comprehensive Next.js Hook](#comprehensive-nextjs-hook-all-validations)
   - [TypeScript + Next.js Integration](#typescript--nextjs-integration)
   - [Next.js Metadata Validation](#nextjs-metadata-validation)

---

## Hook Types and Lifecycle

### Available Hook Types

Claude Code supports several hook types:

- **PostToolUse**: Runs after a tool is used (Edit, Write, Bash, etc.)
- **PreToolUse**: Runs before a tool is used (less common)
- **user-prompt-submit**: Runs when user submits a prompt

### PostToolUse Lifecycle

```
User/Claude → Tool Call → Tool Execution → PostToolUse Hook → Result
                          (Edit/Write)      (Lint/Format)
```

**Timing**: PostToolUse hooks run immediately after the tool completes, before control returns to Claude.

**Environment Variables Available**:

- `$CLAUDE_TOOL_FILE_PATH`: Path to the file that was modified (for Edit/Write tools)
- `$CLAUDE_TOOL_NAME`: Name of the tool that was used

---

## PostToolUse Hook Patterns

### Basic Auto-Linting (Single Language)

**JavaScript/TypeScript with ESLint:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.js || \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Python with Black:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then black \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Python with Ruff (modern alternative):**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then ruff check --fix \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Ruby with RuboCop:**

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.rb ]]; then rubocop \"$CLAUDE_TOOL_FILE_PATH\" --auto-correct 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

---

## Matcher Patterns

### Tool Matchers

Match specific tools that trigger the hook:

- `"Edit"` - Only Edit tool
- `"Write"` - Only Write tool
- `"Edit|Write"` - Either Edit or Write
- `"Bash"` - Bash command execution
- `".*"` - Any tool (use sparingly)

### Examples

**Run only on Edit (not Write):**

```json
{
  "matcher": "Edit",
  "hooks": [...]
}
```

**Run on Edit, Write, or NotebookEdit:**

```json
{
  "matcher": "Edit|Write|NotebookEdit",
  "hooks": [...]
}
```

---

## Multi-Language Configurations

### Full-Stack Project (TypeScript + Python)

```json
{
  "description": "Auto-lint TypeScript and Python files",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts || \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then black \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### Multi-Language with Prettier

```json
{
  "description": "Lint and format multiple languages",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.js || \"$CLAUDE_TOOL_FILE_PATH\" == *.ts || \"$CLAUDE_TOOL_FILE_PATH\" == *.jsx || \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix && npx prettier --write \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then black \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### Comprehensive Multi-Language Setup

```json
{
  "description": "Auto-lint for JS/TS/Python/Ruby/Go/Rust",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.js || \"$CLAUDE_TOOL_FILE_PATH\" == *.ts || \"$CLAUDE_TOOL_FILE_PATH\" == *.jsx || \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then black \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.rb ]]; then rubocop \"$CLAUDE_TOOL_FILE_PATH\" --auto-correct 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.go ]]; then gofmt -w \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.rs ]]; then rustfmt \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

---

## Advanced Patterns

### Dependency Security Analysis

Monitor dependency files for security vulnerabilities and outdated packages:

```json
{
  "description": "Advanced dependency analysis and security checking. Monitors for outdated packages, security vulnerabilities, and license compatibility.",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *package.json || \"$CLAUDE_TOOL_FILE_PATH\" == *requirements.txt || \"$CLAUDE_TOOL_FILE_PATH\" == *Cargo.toml || \"$CLAUDE_TOOL_FILE_PATH\" == *pom.xml || \"$CLAUDE_TOOL_FILE_PATH\" == *Gemfile ]]; then echo \"Dependency file modified: $CLAUDE_TOOL_FILE_PATH\"; if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *package.json ]] && command -v npm >/dev/null 2>&1; then npm audit 2>/dev/null || true; npx npm-check-updates 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *requirements.txt ]] && command -v safety >/dev/null 2>&1; then safety check -r \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; elif [[ \"$CLAUDE_TOOL_FILE_PATH\" == *Cargo.toml ]] && command -v cargo >/dev/null 2>&1; then cargo audit 2>/dev/null || true; fi; fi"
          }
        ]
      }
    ]
  }
}
```

**What this hook does:**

1. **Detects dependency file modifications**: Triggers when package.json, requirements.txt, Cargo.toml, pom.xml, or Gemfile is edited
2. **Runs security audits**:
   - `npm audit` for Node.js projects
   - `safety check` for Python projects
   - `cargo audit` for Rust projects
3. **Checks for updates**: `npm-check-updates` shows available package updates
4. **Graceful failure**: Uses `2>/dev/null || true` and checks if tools are installed

**Prerequisites:**

- Node.js: `npm audit` (built-in), `npm-check-updates` (install: `npm i -g npm-check-updates`)
- Python: `safety` (install: `pip install safety`)
- Rust: `cargo-audit` (install: `cargo install cargo-audit`)

**Use cases:**

- Immediate security feedback when dependencies change
- Proactive vulnerability detection
- Stay informed about outdated packages
- Compliance with security policies

### Conditional Linting by Directory

Only lint files in `src/` directory:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == */src/*.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### Skip Certain Directories

Exclude `node_modules` and `dist`:

```bash
if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts && \"$CLAUDE_TOOL_FILE_PATH\" != */node_modules/* && \"$CLAUDE_TOOL_FILE_PATH\" != */dist/* ]]; then
  npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true
fi
```

### Chain Multiple Tools

Run linter, then formatter:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix && npx prettier --write \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### Package Manager Detection

Automatically use the right package manager:

```bash
# Detect package manager and use appropriate command
if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then
  if [ -f pnpm-lock.yaml ]; then
    pnpm exec eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true
  elif [ -f yarn.lock ]; then
    yarn eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true
  else
    npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true
  fi
fi
```

### Multiple Hooks

Run different hooks for different tools:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Bash command executed' >> .claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```

---

## Performance Optimization

### Best Practices

1. **Use graceful failure**: Always end with `2>/dev/null || true`
   - Prevents hook failures from blocking Claude's work
   - Suppresses error output that clutters the console

2. **Check file extensions early**: Filter by extension before running expensive commands
   - Good: `if [[ "$FILE" == *.ts ]]; then eslint...`
   - Bad: Running eslint on all files and letting it fail

3. **Use --fix flags**: Auto-fix issues instead of just reporting
   - Reduces need for manual intervention
   - Claude's edits are automatically corrected

4. **Avoid running tests**: PostToolUse hooks should be fast
   - Don't run test suites in hooks
   - Use Git pre-push hooks for tests instead

5. **Cache when possible**: Some linters support caching
   - ESLint: `--cache` flag
   - Ruff: Built-in caching

### Example: Optimized Hook

```bash
# Fast: Early exit if not TypeScript
if [[ \"$CLAUDE_TOOL_FILE_PATH\" != *.ts && \"$CLAUDE_TOOL_FILE_PATH\" != *.tsx ]]; then
  exit 0
fi

# Use ESLint cache for faster linting
npx eslint --cache --fix \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true
```

---

## Troubleshooting

### Hook Not Running

**Symptom**: Files aren't being linted after edits

**Diagnosis**:

1. Check `.claude/settings.json` exists and is valid JSON
2. Verify matcher pattern matches the tool being used
3. Test hook command manually:
   ```bash
   CLAUDE_TOOL_FILE_PATH="test.ts" bash -c 'YOUR_HOOK_COMMAND_HERE'
   ```

**Common Issues**:

- Missing quotes around `$CLAUDE_TOOL_FILE_PATH`
- Incorrect file extension pattern (e.g., `*.ts` instead of `\*.ts`)
- Linter not installed or not in PATH

**Fix**:

```json
{
  "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
}
```

Note the escaped quotes and proper quoting of the variable.

### Hook Failing Silently

**Symptom**: Hook runs but doesn't fix issues

**Diagnosis**:

1. Remove `2>/dev/null || true` temporarily to see errors
2. Run linter manually on a test file
3. Check linter configuration files exist

**Common Issues**:

- Linter config missing (`.eslintrc`, `pyproject.toml`, etc.)
- Linter not installed in project dependencies
- File being edited is in ignore list

**Fix**: Ensure linter is properly configured and installed

### Performance Issues

**Symptom**: Claude Code becomes slow after enabling hooks

**Diagnosis**:

1. Check if hook is running on every file (should be selective)
2. Verify linter isn't doing full project scans
3. Look for missing caching flags

**Common Issues**:

- Hook running on all files instead of just edited file
- Linter not using cache
- Multiple hooks running redundantly

**Fix**: Optimize hook to only process relevant files and enable caching

### Wrong Linter Running

**Symptom**: Python linter runs on JS files, etc.

**Diagnosis**:

1. Check file extension pattern in hook command
2. Verify conditional logic (if/elif/else)

**Common Issues**:

- Missing `elif` between conditions
- Incorrect pattern matching syntax
- Multiple hooks with overlapping matchers

**Fix**: Use proper conditional chain with `elif`:

```bash
if [[ "$FILE" == *.ts ]]; then
  eslint...
elif [[ "$FILE" == *.py ]]; then
  black...
fi
```

---

## Integration with Git Hooks

### Complementary Roles

**Claude Code Hooks (PostToolUse)**:

- Real-time linting as Claude edits
- Immediate feedback and auto-fixing
- Only affects files Claude touches

**Git Hooks (pre-commit, pre-push)**:

- Validate before commit/push
- Catch issues from manual edits
- Comprehensive checks (tests, builds)

### Recommended Setup

Use both for complete coverage:

1. **PostToolUse hooks**: Auto-lint on every Claude edit
   - Fast feedback loop
   - Auto-fix minor issues
   - Only lints changed file

2. **Git pre-commit hooks**: Validate staged files before commit
   - Catches manual edits
   - Runs on all staged files
   - Uses lint-staged for speed

3. **Git pre-push hooks**: Full validation before push
   - Runs tests
   - Type checking
   - Production build validation

### Example: Consistent Configuration

**Claude Code (.claude/settings.json)**:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then pnpm exec eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Git Hooks (lint-staged.config.js)**:

```javascript
module.exports = {
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
};
```

Both use the same linters (ESLint, Prettier) for consistency.

---

## Best Practices Summary

1. ✅ **Always use graceful failure**: `2>/dev/null || true`
2. ✅ **Check file extensions early**: Filter before running linters
3. ✅ **Use --fix flags**: Auto-correct when possible
4. ✅ **Keep hooks fast**: Avoid expensive operations
5. ✅ **Quote variables**: Always quote `$CLAUDE_TOOL_FILE_PATH`
6. ✅ **Test manually**: Verify hook commands before deploying
7. ✅ **Use caching**: Enable linter caching for speed
8. ✅ **Combine with Git hooks**: Use both for comprehensive coverage
9. ✅ **Project-level configuration**: Use `.claude/settings.json` for team consistency
10. ✅ **Document customizations**: Add comments explaining hook logic

---

## Next.js Framework-Specific Patterns

### Purpose

Next.js projects require specialized validation beyond standard TypeScript/React linting. This section provides hook configurations for enforcing Next.js best practices, App Router conventions, Server/Client component patterns, and proper imports.

### Prerequisites

Install Next.js ESLint plugin and TypeScript support:

```bash
pnpm add -D eslint-config-next @next/eslint-plugin-next
```

Configure ESLint to use Next.js rules (`.eslintrc.json`):

```json
{
  "extends": ["next/core-web-vitals", "next/typescript"],
  "rules": {
    "@next/next/no-html-link-for-pages": "error",
    "@next/next/no-img-element": "error",
    "@next/next/no-sync-scripts": "error"
  }
}
```

### Basic Next.js Hook (ESLint + Next.js Rules)

```json
{
  "description": "Auto-lint Next.js TypeScript files with framework-specific rules",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts || \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix --config .eslintrc.json 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### App Router Convention Validation

Validates Next.js App Router file structure and naming conventions:

```json
{
  "description": "Validate Next.js App Router conventions and file structure",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == */app/* ]]; then if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *page.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *layout.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *loading.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *error.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *not-found.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *template.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *default.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *route.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; echo \"✓ App Router file validated: $(basename $CLAUDE_TOOL_FILE_PATH)\"; else echo \"⚠ Warning: File in app/ directory should follow App Router conventions (page.tsx, layout.tsx, etc.)\"; fi; fi"
          }
        ]
      }
    ]
  }
}
```

**What this validates:**

- Files in `app/` directory follow naming conventions:
  - `page.tsx` - Route pages
  - `layout.tsx` - Shared layouts
  - `loading.tsx` - Loading UI
  - `error.tsx` - Error boundaries
  - `not-found.tsx` - 404 pages
  - `template.tsx` - Templates
  - `default.tsx` - Parallel route fallbacks
  - `route.ts` - API route handlers

### Server/Client Component Pattern Validation

Enforces proper 'use client' and 'use server' directive usage:

```json
{
  "description": "Validate Next.js Server/Client component patterns and directives",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx && \"$CLAUDE_TOOL_FILE_PATH\" == */app/* ]]; then if grep -q \"'use client'\" \"$CLAUDE_TOOL_FILE_PATH\" || grep -q '\"use client\"' \"$CLAUDE_TOOL_FILE_PATH\"; then if grep -qE \"(useState|useEffect|useContext|useReducer|useRef|useCallback|useMemo|useLayoutEffect|useImperativeHandle|useDebugValue|useDeferredValue|useTransition|useId|useSyncExternalStore|useInsertionEffect|onClick|onChange|onSubmit)\" \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"✓ Client Component correctly uses 'use client' directive\"; else echo \"⚠ Warning: 'use client' directive present but no client-side hooks/event handlers found\"; fi; else if grep -qE \"(useState|useEffect|onClick|onChange)\" \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"❌ ERROR: Client-side hooks/events detected but missing 'use client' directive!\"; fi; fi; npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**What this validates:**

- Files with `'use client'` directive should have client-side features (hooks, event handlers)
- Files using client-side hooks/events must have `'use client'` directive
- Provides warnings for unnecessary directives
- Auto-lints with ESLint after validation

### Next.js Import Pattern Validation

Validates proper usage of Next.js built-in components and functions:

```json
{
  "description": "Validate Next.js import patterns and built-in component usage",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then if grep -q '<img' \"$CLAUDE_TOOL_FILE_PATH\" && ! grep -q \"'use client'\" \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"⚠ Warning: Use next/image instead of <img> for optimized images\"; fi; if grep -q '<a href=' \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"⚠ Warning: Use next/link instead of <a> for internal navigation\"; fi; if grep -q '<script src=' \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"⚠ Warning: Use next/script instead of <script> for better loading strategies\"; fi; npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**What this validates:**

- Warns when using `<img>` instead of `next/image`
- Warns when using `<a href>` instead of `next/link`
- Warns when using `<script src>` instead of `next/script`
- Auto-lints after validation

### Comprehensive Next.js Hook (All Validations)

Combines all Next.js validations into a single hook:

```json
{
  "description": "Comprehensive Next.js validation: App Router, Server/Client patterns, imports, and ESLint",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then echo \"🔍 Validating Next.js file: $(basename $CLAUDE_TOOL_FILE_PATH)\"; if [[ \"$CLAUDE_TOOL_FILE_PATH\" == */app/* ]]; then if ! [[ \"$CLAUDE_TOOL_FILE_PATH\" =~ (page|layout|loading|error|not-found|template|default|route|opengraph-image|twitter-image|icon|apple-icon|manifest|sitemap|robots)\\.(tsx?|jsx?)$ ]]; then echo \"⚠ Warning: File in app/ should follow App Router conventions\"; fi; if grep -q \"'use client'\" \"$CLAUDE_TOOL_FILE_PATH\" || grep -q '\"use client\"' \"$CLAUDE_TOOL_FILE_PATH\"; then if ! grep -qE \"(useState|useEffect|useContext|useReducer|useRef|useCallback|useMemo|onClick|onChange|onSubmit|useSearchParams|usePathname|useRouter|useParams)\" \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"⚠ Warning: 'use client' directive may be unnecessary\"; fi; else if grep -qE \"(useState|useEffect|onClick|onChange|useSearchParams|usePathname|useRouter|useParams)\" \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"❌ ERROR: Client-side features require 'use client' directive!\"; fi; fi; fi; if grep -q '<img' \"$CLAUDE_TOOL_FILE_PATH\" && ! grep -q 'next/image' \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"⚠ Use next/image instead of <img>\"; fi; if grep -q '<a href=' \"$CLAUDE_TOOL_FILE_PATH\" && ! grep -q 'next/link' \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"⚠ Use next/link instead of <a>\"; fi; npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix --config .eslintrc.json 2>/dev/null || true; echo \"✅ Next.js validation complete\"; fi"
          }
        ]
      }
    ]
  }
}
```

**Complete validation includes:**

1. **App Router conventions**: Validates file naming in `app/` directory
2. **Server/Client patterns**: Checks for proper `'use client'` usage
3. **Import validation**: Warns about non-optimal imports
4. **ESLint with Next.js rules**: Runs framework-specific linting
5. **Provides real-time feedback**: Immediate warnings and errors

### TypeScript + Next.js Integration

For strict TypeScript validation with Next.js:

```json
{
  "description": "Next.js with strict TypeScript type checking and validation",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; if [[ \"$CLAUDE_TOOL_FILE_PATH\" == */app/* ]]; then npx tsc --noEmit --skipLibCheck \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; fi"
          }
        ]
      }
    ]
  }
}
```

**What this does:**

1. Runs ESLint with Next.js rules
2. Performs TypeScript type checking on App Router files
3. Skips library type checking for speed
4. Auto-fixes issues when possible

### Performance Optimization for Next.js Hooks

**Best Practices:**

1. **Cache ESLint results**: Use `--cache` flag for faster repeat checks

   ```bash
   npx eslint --cache --fix "$CLAUDE_TOOL_FILE_PATH"
   ```

2. **Skip node_modules**: Always exclude dependency directories

   ```bash
   if [[ "$CLAUDE_TOOL_FILE_PATH" != */node_modules/* && "$CLAUDE_TOOL_FILE_PATH" != */.next/* ]]; then
     # Run validations
   fi
   ```

3. **Use fast grep checks**: Validate patterns before running expensive linters

   ```bash
   # Quick pattern check first
   if grep -q "useState" "$FILE"; then
     # Then run full validation
   fi
   ```

4. **Parallel execution**: For multiple independent checks, use background processes
   ```bash
   npx eslint "$FILE" --fix &
   grep -q "'use client'" "$FILE" &
   wait
   ```

### Integration with Git Hooks

**Recommended setup for Next.js projects:**

**Claude Code Hook** (.claude/settings.json) - Real-time validation:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *.ts ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix --cache 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Git Pre-commit Hook** (lint-staged.config.js) - Comprehensive validation:

```javascript
module.exports = {
  "*.{ts,tsx}": [
    "eslint --fix --config .eslintrc.json",
    "prettier --write",
    () => "tsc --noEmit",
  ],
  "app/**/*.{ts,tsx}": [
    // Additional App Router specific checks
    "eslint --fix",
  ],
};
```

**Git Pre-push Hook** (.husky/pre-push) - Full build validation:

```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Type check entire project
pnpm tsc --noEmit

# Run tests
pnpm test

# Validate Next.js build
pnpm build
```

### Troubleshooting Next.js Hooks

**Issue: False positives for 'use client' warnings**

**Cause**: Hook doesn't recognize all client-side patterns

**Fix**: Extend the regex pattern to include more client-side features:

```bash
grep -qE "(useState|useEffect|useContext|useReducer|useRef|useCallback|useMemo|useLayoutEffect|useSearchParams|usePathname|useRouter|useParams|useSelectedLayoutSegment|useServerInsertedHTML|onClick|onChange|onSubmit|onBlur|onFocus|onKeyDown|onKeyUp|onKeyPress|onMouseEnter|onMouseLeave)"
```

**Issue: Hook too slow on large files**

**Cause**: Running multiple validations sequentially

**Fix**: Use fast early exits and cache ESLint:

```bash
# Early exit if not in app directory
if [[ "$FILE" != */app/* ]]; then exit 0; fi

# Use ESLint cache
npx eslint --cache --fix "$FILE"
```

**Issue: Hook conflicts with existing ESLint config**

**Cause**: Project has custom ESLint rules that conflict

**Fix**: Explicitly specify Next.js config:

```bash
npx eslint "$FILE" --fix --config .eslintrc.json --resolve-plugins-relative-to .
```

### Next.js Metadata Validation

Validates metadata exports in App Router:

```json
{
  "description": "Validate Next.js metadata API usage in layouts and pages",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == */app/*layout.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == */app/*page.tsx ]]; then if ! grep -q \"export.*metadata\" \"$CLAUDE_TOOL_FILE_PATH\" && ! grep -q \"generateMetadata\" \"$CLAUDE_TOOL_FILE_PATH\"; then echo \"ℹ Info: Consider adding metadata export for SEO optimization\"; fi; npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**What this validates:**

- Layouts and pages should export `metadata` or `generateMetadata` for SEO
- Provides informational reminders (not errors)
- Helps maintain good SEO practices

## Security Scanning Patterns

### Purpose

Security scanning hooks automatically detect vulnerabilities and secrets in code as it's written. This section provides comprehensive patterns for integrating security tools into Claude Code PostToolUse hooks.

### Basic Security Scanning Hook

**Multi-tool security scanning:**

```json
{
  "description": "Scan code for security vulnerabilities and secrets after modifications",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v semgrep >/dev/null 2>&1; then semgrep --config=auto \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; if command -v bandit >/dev/null 2>&1 && [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then bandit \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; if command -v gitleaks >/dev/null 2>&1; then gitleaks detect --source=\"$CLAUDE_TOOL_FILE_PATH\" --no-git 2>/dev/null || true; fi; if grep -qE '(password|secret|key|token)\\s*=\\s*[\"\\'][^\"\\'\n]{8,}' \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null; then echo \"Warning: Potential hardcoded secrets detected in $CLAUDE_TOOL_FILE_PATH\" >&2; fi"
          }
        ]
      }
    ]
  }
}
```

**What this does:**

1. Runs semgrep for vulnerability detection (all languages)
2. Runs bandit for Python-specific security issues
3. Runs gitleaks for secrets detection
4. Uses regex to catch hardcoded secrets
5. All tools check for installation first
6. Gracefully skips missing tools

### Individual Tool Patterns

#### Semgrep (Multi-Language Vulnerability Scanning)

**Basic semgrep hook:**

```json
{
  "description": "Run semgrep security analysis on all code files",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v semgrep >/dev/null 2>&1; then semgrep --config=auto \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Semgrep with custom rulesets:**

```json
{
  "description": "Run semgrep with OWASP Top 10 rules",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v semgrep >/dev/null 2>&1; then semgrep --config=p/owasp-top-ten --config=p/security-audit \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Available semgrep configs:**

- `--config=auto` - Community rules (recommended default)
- `--config=p/owasp-top-ten` - OWASP Top 10 vulnerabilities
- `--config=p/security-audit` - Comprehensive security audit
- `--config=p/xss` - XSS detection
- `--config=p/sql-injection` - SQL injection detection
- `--config=p/ci` - CI-focused checks (faster)
- `--config=p/javascript` - JavaScript-specific rules
- `--config=p/python` - Python-specific rules

**Semgrep with JSON output (for parsing):**

```bash
if command -v semgrep >/dev/null 2>&1; then
  semgrep --config=auto --json "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null | jq '.results[] | "[\(.check_id)] \(.extra.message)"' || true
fi
```

#### Bandit (Python Security Scanner)

**Basic bandit hook:**

```json
{
  "description": "Run bandit security scanner on Python files",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v bandit >/dev/null 2>&1 && [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then bandit \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Bandit with severity filtering:**

```bash
# Only report high and medium severity issues
if command -v bandit >/dev/null 2>&1 && [[ "$CLAUDE_TOOL_FILE_PATH" == *.py ]]; then
  bandit -ll "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
fi
```

**Bandit with specific tests:**

```bash
# Only check for hardcoded passwords and SQL injection
if command -v bandit >/dev/null 2>&1 && [[ "$CLAUDE_TOOL_FILE_PATH" == *.py ]]; then
  bandit -t B105,B608 "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
fi
```

**Common bandit test IDs:**

- `B105` - Hardcoded password strings
- `B106` - Hardcoded password function arguments
- `B107` - Hardcoded password default arguments
- `B201` - Flask debug mode
- `B301` - Pickle usage
- `B303` - MD5/SHA1 usage
- `B320` - XML vulnerabilities
- `B608` - SQL injection

#### Gitleaks (Secrets Detection)

**Basic gitleaks hook:**

```json
{
  "description": "Detect secrets and credentials in code",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if command -v gitleaks >/dev/null 2>&1; then gitleaks detect --source=\"$CLAUDE_TOOL_FILE_PATH\" --no-git 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

**Gitleaks with verbose output:**

```bash
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --source="$CLAUDE_TOOL_FILE_PATH" --no-git --verbose 2>/dev/null || true
fi
```

**Gitleaks with custom config:**

```bash
# Use project-specific gitleaks config
if command -v gitleaks >/dev/null 2>&1 && [ -f .gitleaks.toml ]; then
  gitleaks detect --source="$CLAUDE_TOOL_FILE_PATH" --config=.gitleaks.toml --no-git 2>/dev/null || true
fi
```

#### Pattern-Based Secrets Detection

**Basic regex pattern matching:**

```bash
# Simple hardcoded secrets detection
if grep -qE '(password|secret|key|token)\s*=\s*["'][^"'\n]{8,}' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
  echo "Warning: Potential hardcoded secrets detected in $CLAUDE_TOOL_FILE_PATH" >&2
fi
```

**Advanced pattern matching with specific warnings:**

```bash
# Detect various secret patterns with specific messages
if grep -qE '(aws_access_key_id|aws_secret_access_key|AKIA[0-9A-Z]{16})' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
  echo "❌ AWS credentials detected in $CLAUDE_TOOL_FILE_PATH" >&2
fi

if grep -qE '(sk_live_|sk_test_)[0-9a-zA-Z]{24,}' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
  echo "❌ Stripe API key detected in $CLAUDE_TOOL_FILE_PATH" >&2
fi

if grep -qE '(gh[pousr]_[0-9a-zA-Z]{36})' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
  echo "❌ GitHub token detected in $CLAUDE_TOOL_FILE_PATH" >&2
fi

if grep -qE 'Bearer [0-9a-zA-Z\-._~+/]+=*' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
  echo "⚠ Bearer token detected in $CLAUDE_TOOL_FILE_PATH" >&2
fi
```

**Comprehensive secret patterns:**

```bash
# Combined pattern matching for multiple secret types
if grep -qE '(password|passwd|pwd|secret|api_key|apikey|token|auth|credential)\s*[:=]\s*["'"'"'][^"'"'"'\n]{8,}' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
  echo "⚠ Potential hardcoded secret detected" >&2
  grep -nE '(password|passwd|pwd|secret|api_key|apikey|token|auth|credential)\s*[:=]\s*["'"'"'][^"'"'"'\n]{8,}' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null | head -3
fi
```

### Combined Security + Linting Hooks

#### TypeScript/JavaScript with Security

```json
{
  "description": "Lint and security scan TypeScript files",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.ts || \"$CLAUDE_TOOL_FILE_PATH\" == *.tsx || \"$CLAUDE_TOOL_FILE_PATH\" == *.js || \"$CLAUDE_TOOL_FILE_PATH\" == *.jsx ]]; then npx eslint \"$CLAUDE_TOOL_FILE_PATH\" --fix 2>/dev/null || true; if command -v semgrep >/dev/null 2>&1; then semgrep --config=p/javascript --config=p/xss \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; fi; if command -v gitleaks >/dev/null 2>&1; then gitleaks detect --source=\"$CLAUDE_TOOL_FILE_PATH\" --no-git 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

#### Python with Comprehensive Security

```json
{
  "description": "Format, lint, and security scan Python files",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ \"$CLAUDE_TOOL_FILE_PATH\" == *.py ]]; then if command -v black >/dev/null 2>&1; then black \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; if command -v bandit >/dev/null 2>&1; then bandit -ll \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; if command -v semgrep >/dev/null 2>&1; then semgrep --config=p/python --config=p/sql-injection \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true; fi; fi; if command -v gitleaks >/dev/null 2>&1; then gitleaks detect --source=\"$CLAUDE_TOOL_FILE_PATH\" --no-git 2>/dev/null || true; fi"
          }
        ]
      }
    ]
  }
}
```

### Language-Specific Security Patterns

#### Go Security Scanning

```bash
# Go security with gosec
if [[ "$CLAUDE_TOOL_FILE_PATH" == *.go ]]; then
  if command -v gosec >/dev/null 2>&1; then
    gosec "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
  fi
  if command -v semgrep >/dev/null 2>&1; then
    semgrep --config=p/golang "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
  fi
fi
```

#### Ruby Security Scanning

```bash
# Ruby security with brakeman
if [[ "$CLAUDE_TOOL_FILE_PATH" == *.rb ]]; then
  if command -v brakeman >/dev/null 2>&1; then
    brakeman --quiet --no-pager "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
  fi
  if command -v semgrep >/dev/null 2>&1; then
    semgrep --config=p/ruby "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
  fi
fi
```

#### Java Security Scanning

```bash
# Java security with spotbugs/findsecbugs
if [[ "$CLAUDE_TOOL_FILE_PATH" == *.java ]]; then
  if command -v semgrep >/dev/null 2>&1; then
    semgrep --config=p/java --config=p/owasp-top-ten "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
  fi
fi
```

### Advanced Security Patterns

#### Context-Aware Security Scanning

```bash
# Only scan security-critical directories with strict rules
if [[ "$CLAUDE_TOOL_FILE_PATH" == */auth/* || "$CLAUDE_TOOL_FILE_PATH" == */api/* || "$CLAUDE_TOOL_FILE_PATH" == */security/* ]]; then
  echo "🔒 Security-critical file detected, running comprehensive scan..."
  if command -v semgrep >/dev/null 2>&1; then
    semgrep --config=p/owasp-top-ten --config=p/security-audit "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
  fi
  if command -v gitleaks >/dev/null 2>&1; then
    gitleaks detect --source="$CLAUDE_TOOL_FILE_PATH" --no-git --verbose 2>/dev/null || true
  fi
else
  # Standard security scan for other files
  if command -v semgrep >/dev/null 2>&1; then
    semgrep --config=auto "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
  fi
fi
```

#### Configuration File Security

```bash
# Special handling for config files
if [[ "$CLAUDE_TOOL_FILE_PATH" == *.env* || "$CLAUDE_TOOL_FILE_PATH" == *config* || "$CLAUDE_TOOL_FILE_PATH" == *secret* ]]; then
  echo "⚠️  Configuration file detected, scanning for secrets..."

  # Run gitleaks with verbose output
  if command -v gitleaks >/dev/null 2>&1; then
    gitleaks detect --source="$CLAUDE_TOOL_FILE_PATH" --no-git --verbose 2>/dev/null || true
  fi

  # Check for exposed secrets
  if grep -qE '(password|secret|key|token)\s*[:=]\s*[^${]' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
    echo "❌ ERROR: Hardcoded secrets in config file!" >&2
    echo "Use environment variables or secret management instead" >&2
  fi
fi
```

#### Dependency File Security

```bash
# Monitor dependency changes for vulnerabilities
if [[ "$CLAUDE_TOOL_FILE_PATH" == *package.json || "$CLAUDE_TOOL_FILE_PATH" == *requirements.txt || "$CLAUDE_TOOL_FILE_PATH" == *Gemfile || "$CLAUDE_TOOL_FILE_PATH" == *go.mod ]]; then
  echo "📦 Dependency file modified, running security audit..."

  if [[ "$CLAUDE_TOOL_FILE_PATH" == *package.json ]] && command -v npm >/dev/null 2>&1; then
    npm audit --json 2>/dev/null | jq '.vulnerabilities | to_entries[] | select(.value.severity == "high" or .value.severity == "critical") | "[\(.value.severity)] \(.key)"' || true
  elif [[ "$CLAUDE_TOOL_FILE_PATH" == *requirements.txt ]] && command -v safety >/dev/null 2>&1; then
    safety check -r "$CLAUDE_TOOL_FILE_PATH" --json 2>/dev/null || true
  elif [[ "$CLAUDE_TOOL_FILE_PATH" == *Gemfile ]] && command -v bundle-audit >/dev/null 2>&1; then
    bundle-audit check 2>/dev/null || true
  fi
fi
```

### Security Scanning Performance Optimization

#### Fast Security Scanning (Essential Only)

```bash
# Minimal security scan for speed
if command -v gitleaks >/dev/null 2>&1; then
  gitleaks detect --source="$CLAUDE_TOOL_FILE_PATH" --no-git 2>/dev/null || true
fi

if grep -qE '(password|secret|key|token)\s*=\s*["'"'"'][^"'"'"'\n]{8,}' "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null; then
  echo "⚠️  Potential secrets detected" >&2
fi
```

#### Cached Security Scanning

```bash
# Use semgrep with caching for faster repeat scans
SEMGREP_CACHE_DIR="${HOME}/.cache/semgrep"
mkdir -p "$SEMGREP_CACHE_DIR"

if command -v semgrep >/dev/null 2>&1; then
  SEMGREP_CACHE_DIR="$SEMGREP_CACHE_DIR" semgrep --config=auto "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
fi
```

#### Parallel Security Tool Execution

```bash
# Run multiple tools in parallel for speed
(
  if command -v semgrep >/dev/null 2>&1; then
    semgrep --config=auto "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
  fi
) &

(
  if command -v gitleaks >/dev/null 2>&1; then
    gitleaks detect --source="$CLAUDE_TOOL_FILE_PATH" --no-git 2>/dev/null || true
  fi
) &

wait
```

### Troubleshooting Security Hooks

#### Issue: Too Many False Positives

**Solution**: Configure ignore files

```bash
# .semgrepignore
tests/
*.test.ts
mock-data/

# .gitleaksignore
test-fixtures/
*.example.env
```

**Or use inline ignores:**

```python
# nosemgrep: python.lang.security.audit.dangerous-eval.dangerous-eval-use
eval(safe_expression)

# gitleaks:allow
TEST_API_KEY = "test_key_12345"
```

#### Issue: Security Tools Too Slow

**Solution**: Use faster configs or skip for certain files

```bash
# Skip security scanning for test files
if [[ "$CLAUDE_TOOL_FILE_PATH" == */tests/* || "$CLAUDE_TOOL_FILE_PATH" == *.test.* ]]; then
  exit 0
fi

# Use fast CI config for semgrep
if command -v semgrep >/dev/null 2>&1; then
  semgrep --config=p/ci "$CLAUDE_TOOL_FILE_PATH" 2>/dev/null || true
fi
```

#### Issue: Tools Not Installed

**Solution**: Provide helpful installation messages

```bash
if ! command -v semgrep >/dev/null 2>&1; then
  echo "ℹ️  Install semgrep for security scanning: pip install semgrep" >&2
fi

if ! command -v gitleaks >/dev/null 2>&1; then
  echo "ℹ️  Install gitleaks for secrets detection: brew install gitleaks" >&2
fi
```

### Security Scanning Best Practices

1. ✅ **Always use graceful failure**: `|| true` prevents blocking work
2. ✅ **Check tool installation**: Use `command -v tool` before running
3. ✅ **Run secrets detection on all files**: Gitleaks should scan everything
4. ✅ **Use appropriate rulesets**: Match semgrep config to project type
5. ✅ **Combine with Git pre-commit**: PostToolUse + pre-commit = comprehensive coverage
6. ✅ **Configure ignore files**: Reduce false positives with `.semgrepignore`, `.gitleaksignore`
7. ✅ **Provide context**: Echo warnings with file paths and severity
8. ✅ **Keep tools updated**: Security tools need regular updates for new vulnerabilities
9. ✅ **Test with known issues**: Verify hooks catch real vulnerabilities
10. ✅ **Document exceptions**: Comment why specific warnings are suppressed

### Integration with CI/CD

**PostToolUse Hook** (non-blocking warnings):

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "semgrep --config=auto \"$CLAUDE_TOOL_FILE_PATH\" 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

**Git Pre-commit** (blocking on critical issues):

```bash
#!/usr/bin/env sh
# .husky/pre-commit

# Block commit on critical security issues
semgrep --config=p/owasp-top-ten --error --strict .
gitleaks detect --source=. --verbose
```

**CI Pipeline** (comprehensive security audit):

```yaml
# .github/workflows/security.yml
- name: Security Scan
  run: |
    semgrep --config=p/security-audit --sarif > semgrep.sarif
    gitleaks detect --source=. --report-format=sarif --report-path=gitleaks.sarif
    npm audit --audit-level=moderate
```

## Additional Resources

- [Claude Code Documentation](https://claude.ai/docs)
- [ESLint CLI Options](https://eslint.org/docs/latest/use/command-line-interface)
- [Black Documentation](https://black.readthedocs.io/)
- [RuboCop Documentation](https://docs.rubocop.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Next.js ESLint Plugin](https://nextjs.org/docs/app/building-your-application/configuring/eslint)
- [Next.js App Router Documentation](https://nextjs.org/docs/app)
- [Next.js Server/Client Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Semgrep Documentation](https://semgrep.dev/docs/)
- [Semgrep Rules Registry](https://semgrep.dev/r)
- [Gitleaks Documentation](https://github.com/gitleaks/gitleaks)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Last Updated**: 2026-01-10
