# Migration Guide: Legacy Docs → CLAUDE.md

## Purpose

Convert unstructured project documentation (README, ARCHITECTURE.md, scattered wikis) into a comprehensive CLAUDE.md file.

## Migration Workflow

### Step 1: Discovery

Identify existing documentation:

- [ ] README.md - Project overview, setup instructions
- [ ] ARCHITECTURE.md / docs/architecture/ - System design
- [ ] CONTRIBUTING.md - Development workflow, code standards
- [ ] package.json / pyproject.toml - Dependencies, scripts
- [ ] .env.example - Environment variables
- [ ] CI/CD configs (.github/workflows/, .gitlab-ci.yml)
- [ ] Wiki / Confluence pages - Business rules, patterns

### Step 2: Content Mapping

Map legacy docs to CLAUDE.md sections:

| Legacy Source        | CLAUDE.md Section                       | Extraction Strategy                |
| -------------------- | --------------------------------------- | ---------------------------------- |
| README "About"       | `[project_metadata]`                    | Copy description, add objectives   |
| README "Setup"       | `[commands]`, `[environment_variables]` | Extract commands, env vars         |
| package.json scripts | `[commands]`                            | List with brief descriptions       |
| ARCHITECTURE.md      | `[stack]`, `[directory_structure]`      | Summarize tech stack + key paths   |
| CONTRIBUTING.md      | `[workflow]`, `[code_standards]`        | Extract git practices, conventions |
| .env.example         | `[environment_variables]`               | Document each variable's purpose   |
| CI/CD configs        | `[deployment]`, `[testing]`             | Describe deployment process        |

### Step 3: Transformation Rules

**Consolidate**:

- Multiple README sections → Single `[project_metadata]`
- Scattered env vars → Organized `[environment_variables]`

**Enrich**:

- Add rationale to tech choices (`[stack]`)
- Define agent roles (`[core_team]`)
- Add Quick Reference section

**Prune**:

- Remove outdated information
- Cut verbose explanations (keep essentials)
- Move detailed guides to `.claude/docs/`

### Step 4: Validation

- Run quality checks (see Validation Framework in SKILL.md)
- Ensure all required sections present
- Target 500-700 lines (standard project)

### Step 5: Parallel Maintenance

During transition:

- Keep legacy docs for 1-2 sprints
- Add notice: "See CLAUDE.md for authoritative documentation"
- Gradually deprecate old docs

## Example Migration

**Before (README.md - 200 lines)**:

```markdown
# MyApp

MyApp is a task management tool...

## Installation

Run `npm install`...

## Development

Run `npm run dev`...

## Tech Stack

- React
- Node.js
- PostgreSQL
```

**After (CLAUDE.md - 600 lines)**:

```markdown
# CLAUDE.md - MyApp

## [project_metadata]

name: MyApp
description: Task management SaaS with team collaboration
objectives:

- Enable teams to track tasks efficiently
- Provide real-time collaboration features

## [stack]

**Framework**: Next.js 14
**Database**: PostgreSQL (Supabase)
**Rationale**: Next.js provides SSR + API routes, Supabase handles auth + real-time

## [commands]

pnpm dev # Development server
pnpm build # Production build
pnpm test # Run tests

## [core_team]

### @security-architect

- Role: Review auth flows, data handling
  ...
```

**Outcome**: Comprehensive, agent-optimized documentation in standardized format.

---

## Common Challenges

**Challenge**: Too much legacy content (5+ docs, 2000+ total lines)
**Solution**: Prioritize essentials, extract details to `.claude/docs/`, link from CLAUDE.md

**Challenge**: Conflicting information across docs
**Solution**: Verify with codebase (package.json, actual file structure), use most recent

**Challenge**: Missing context (why certain tech choices?)
**Solution**: Interview team members, document assumptions, note TODOs for future clarification
