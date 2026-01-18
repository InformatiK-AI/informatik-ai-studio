# Shared Skill Mixins

This directory contains reusable components (mixins) for skills to reduce duplication and ensure consistency across the framework.

## Purpose

Instead of duplicating common sections across multiple skills, skills can reference these shared mixins. This provides:

1. **Single Source of Truth** - Update once, apply everywhere
2. **Consistency** - All skills use the same standards
3. **Maintainability** - Easier to update tech stacks, best practices, etc.
4. **Reduced File Size** - Skills become more focused on their unique value

## Available Mixins

| Mixin | Description | Used By |
|-------|-------------|---------|
| `tech-stack-fullstack.md` | Full-stack tech stack (TS, React, Node, etc.) | senior-frontend, senior-backend, senior-devops, senior-security, senior-architect, senior-fullstack |
| `tech-stack-data.md` | Data/ML tech stack (Python, Spark, etc.) | senior-data-engineer, senior-data-scientist |
| `best-practices-general.md` | General best practices (Code Quality, Performance, Security, Maintainability) | All senior-* skills |
| `best-practices-senior.md` | Senior-level responsibilities | senior-data-engineer, senior-data-scientist |
| `development-workflow.md` | Standard development workflow | All senior-* skills |
| `common-commands.md` | Common CLI commands | All senior-* skills |
| `troubleshooting.md` | Troubleshooting template | All senior-* skills |
| `performance-targets.md` | Performance SLOs template | Data/ML skills |
| `security-compliance.md` | Security & compliance checklist | All skills |

## How to Use Mixins

### Method 1: Include Directive (Recommended)

In your SKILL.md, use the include directive:

```markdown
{{include:tech-stack-fullstack}}
```

Then run the build script to process:

```bash
python .claude/skills/_shared/build_mixins.py skill-name
```

### Method 2: Pre-built Content

Skills can also have pre-built content with mixin-source markers:

```markdown
<!-- mixin-source: tech-stack-fullstack v1.0.0 -->
## Tech Stack
...content...
```

## Build Script

The `build_mixins.py` script automates mixin processing:

```bash
# Build all skills with mixin configurations
python .claude/skills/_shared/build_mixins.py

# Build a specific skill
python .claude/skills/_shared/build_mixins.py senior-frontend

# Check for outdated mixins
python .claude/skills/_shared/build_mixins.py --check

# Dry run (show what would change)
python .claude/skills/_shared/build_mixins.py --dry-run
```

**Features:**
- Processes `{{include:mixin-name}}` directives
- Replaces placeholders like `{{ANALYZER_SCRIPT}}`
- Updates existing mixin-source sections
- Checks for version mismatches

## Updating Mixins

When updating a mixin:

1. Edit the mixin file in this directory
2. Update the version in the mixin header
3. Update the version in `MIXINS.json`
4. Run `python build_mixins.py` to propagate changes
5. Run validation: `python ../_tests/test_skill_mixins.py`

## Mixin Versioning

Each mixin includes a version comment at the top:

```markdown
<!-- mixin-version: 1.0.0 -->
```

This helps track which version of a mixin a skill is using.

## Creating New Mixins

1. Identify repeated content across 3+ skills
2. Extract to a new `.md` file in this directory
3. Add entry to this README
4. Update MANIFEST.json with mixin reference
5. Update dependent skills to use the mixin
