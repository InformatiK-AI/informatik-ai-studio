---
name: claude-md-architect
description: This skill should be used when creating a new CLAUDE.md file for a project (whether it exists or not), recreating/replacing an existing CLAUDE.md from scratch, or when auditing, improving, or modernizing an existing CLAUDE.md file. It provides strategic guidance for designing future-proof project documentation that serves as the "Constitution" for all development work.
---

# Claude.md Architect

This skill provides expert guidance for designing, creating, recreating, and maintaining future-proof CLAUDE.md files that serve as comprehensive project documentation and strategic foundations.

## Purpose

CLAUDE.md files are the foundational "Constitution" for projects, providing:

- Strategic context (objectives, tech stack, team structure)
- Technical context (paths, environment variables, commands)
- Global rules (workflow, code standards, testing requirements)
- Agent coordination (defining specialized agent roles and responsibilities)

This skill ensures CLAUDE.md files are:

- **Comprehensive**: Cover all necessary project aspects
- **Future-proof**: Designed to evolve with the project
- **Actionable**: Provide clear guidance for agents and developers
- **Consistent**: Follow best practices and organizational standards

## When to Use This Skill

Use this skill when:

- In plan mode (EnterPlanMode) and in build mode (alt+b to cycle)
- Bootstrapping a new project and need to create an initial CLAUDE.md
- **Recreating or replacing an existing CLAUDE.md from scratch** (e.g., "create a new CLAUDE.md", "rebuild the CLAUDE.md", "start fresh with CLAUDE.md")
- Auditing an existing CLAUDE.md for completeness and best practices
- Modernizing legacy project documentation into CLAUDE.md format
- Updating CLAUDE.md to reflect major architectural changes
- Ensuring consistency across multiple projects in an organization

---

## Quick Decision Tree

**What do you need to do?**

- 📝 **Creating new CLAUDE.md from scratch?** → [New Project Workflow](#workflow)
- 🔄 **Recreating/replacing existing CLAUDE.md?** → [New Project Workflow](#workflow) (review existing first)
- 🔍 **Auditing/improving existing CLAUDE.md?** → [Audit & Improve Workflow](#for-existing-projects-audit--improve)
- 📦 **Migrating from legacy docs (README, wiki)?** → [Migration Guide](./references/migration-guide.md)
- ✅ **Validating CLAUDE.md quality?** → [Validation Checklist](./references/validation-checklist.md)

---

## CLAUDE.md Sizing Guidelines

### Length Targets (Modular Architecture)

All projects use **modular architecture** with a lightweight core CLAUDE.md:

- **Core CLAUDE.md:** 100-300 lines (strategic context and index only)
- **Auto-loaded rules:** 50-150 lines each (in `.claude/rules/`)
- **Path-specific rules:** 50-200 lines each (in `.claude/rules/domain/`)
- **On-demand docs:** No limit (in `.claude/docs/`)

### Conciseness Principles

1. **Essential First:** Include only what agents need to start working effectively
2. **Link, Don't Duplicate:** Reference external docs instead of copying content
3. **Examples Externalize:** Move lengthy code blocks (>20 lines) to `.claude/examples/`
4. **Avoid Redundancy:** Don't repeat commands/workflows across multiple sections
5. **Progressive Detail:** Start simple, add complexity as the project evolves

### Modular Structure (Standard)

All projects use modular architecture. Content is organized as follows:

- **Core CLAUDE.md:** Strategic context, tech stack, core team, and modular index
- **Auto-loaded rules:** Code standards, testing, security, git workflow
- **Path-specific rules:** Domain rules triggered by file paths
- **On-demand docs:** Reference material loaded when needed

**Standard Modular Structure:**

```
.claude/
├── docs/
│   ├── patterns/           # Detailed implementation patterns
│   │   ├── animations.md
│   │   ├── testing-strategies.md
│   │   └── security-checklist.md
│   ├── architecture/       # System design documents
│   │   ├── database-schema.md
│   │   └── api-design.md
│   └── guides/             # Step-by-step guides
│       └── deployment-guide.md
└── examples/               # Code examples and templates
    ├── component-template.tsx
    └── ci-cd-pipeline.yml
```

**In CLAUDE.md, reference these files:**

```markdown
### Animation Standards

- Use Framer Motion for interactive animations
- Follow performance best practices (will-change, transform/opacity only)
- See [Animation Patterns](./.claude/docs/patterns/animations.md) for detailed examples
- See [Animation Performance](./.claude/docs/patterns/animation-performance.md) for optimization guide
```

---

## Optimizing for Agent Consumption

CLAUDE.md is **primarily consumed by AI agents**. Optimize for efficient parsing and context usage:

### 1. Scannability

- **Use clear section headers** with consistent formatting: `## [section_name]`
- **Bullet points over paragraphs** for rules and lists
- **Tables for comparison/reference** (tech stacks, environments, metrics)
- **Code blocks with language tags** for proper syntax highlighting

### 2. Quick Reference Section

**Always include a "Quick Reference" section** near the top or bottom with:

- Key file paths
- Essential commands
- Critical rules
- Emergency contacts

Agents should find essentials in <100 tokens for rapid orientation.

### 3. Context Efficiency

- **Agents have limited context windows** (typically 200K tokens)
- **Concise CLAUDE.md = more room for actual code context**
- **Target:** Agent can load CLAUDE.md + 5-10 relevant files without overflow
- **Rule of thumb:** CLAUDE.md should consume <5% of available context

### 4. Progressive Detail

- **Core rules in main file** (CLAUDE.md)
- **Detailed patterns in separate files** (`.claude/docs/patterns/`)
- **Agents load detail only when needed** (on-demand retrieval)

### 5. Avoid Over-Documentation

Don't document what's already obvious from code:

- ❌ **Don't:** List every single file in directory structure
- ✅ **Do:** Show key directories and critical files only

- ❌ **Don't:** Explain how standard tools work (React, TypeScript)
- ✅ **Do:** Document project-specific patterns and conventions

- ❌ **Don't:** Copy-paste entire config files
- ✅ **Do:** Highlight important config values and link to the file

---

## CLAUDE.md Validation Framework

Before presenting CLAUDE.md for user approval, validate quality using the automated checklist.

**See**: [Validation Checklist](./references/validation-checklist.md) for complete validation framework including:

- **Length Validation**: Target 100-300 lines (core CLAUDE.md), modular files appropriately sized
- **Completeness Check**: Required sections and modular files checklist
- **Reference Integrity**: All referenced modular files exist
- **Quality Scoring**: 0-100 point rubric with weighted criteria

**Target Quality Score**: 75+ (Good) before presenting to user for approval.

**Quality Bands**:

- 90-100: Excellent - Ready for approval
- 75-89: Good - Minor improvements suggested
- 60-74: Adequate - Review flagged issues
- <60: Needs revision - Critical issues found

---

## ⚠️ CRITICAL POST-COMPLETION REQUIREMENT

**IMPERATIVE: After ANY CLAUDE.md modification (create, update, recreate), you MUST automatically invoke the `hooks-setup` skill.**

This is **NON-NEGOTIABLE** and applies to:

- Creating a new CLAUDE.md from scratch
- Updating any section of an existing CLAUDE.md
- Recreating or replacing CLAUDE.md entirely
- Any other modification, no matter how small

**Why This Is Critical:**

- CLAUDE.md defines code quality standards, testing requirements, and security policies
- Git hooks enforce these standards at commit time
- Claude Code hooks enforce standards during development
- Security hooks prevent vulnerabilities from being committed
- Without hook updates, the project's quality guardrails become stale

**Execution:**

- After user approves CLAUDE.md changes
- Invoke: `Skill(skill: "hooks-setup")`
- Wait for hooks-setup to complete before considering the task done

**Failure to invoke hooks-setup is a critical oversight that compromises project quality.**

---

## Workflow

### For New Projects (or Recreating from Scratch)

When creating a CLAUDE.md for a new project or recreating an existing one from scratch:

> **Note**: If a CLAUDE.md already exists and you're recreating from scratch, first review it to identify any valuable content worth preserving (e.g., environment variables, established workflows, team structure). You can choose to start completely fresh or incorporate relevant existing sections.

1. **Gather Requirements**
   - Understand the high-level project objective
   - Identify key stakeholders and their roles
   - Determine any technical constraints or preferences

2. **Research & Select Stack**
   - Review [Factory Verticals](references/factory-verticals.md) for standard tech stacks
   - Research modern alternatives if standard stacks don't fit
   - Consider factors: team expertise, scalability, maintenance, ecosystem
   - **Default to Factory Verticals unless explicitly requested otherwise**

3. **Define Strategic Foundation**
   - Document project metadata (name, description, objectives)
   - Specify chosen tech stack with justification
   - Define core team structure (required agents and their roles)
   - Always include `security-architect` and `acceptance-validator` in core team

4. **Establish Technical Context**
   - Define directory structure and key file paths
   - List required environment variables
   - Document essential commands (dev, build, test, deploy)
   - Specify configuration file locations

5. **Set Global Rules**
   - Define development workflow and git practices
   - For development process use commands:
     - 1. Plan → `flow-plan.md "[task]"`
     - 2. Contract → `flow-issue-create.md "[task]"`
     - 3. Build → `flow-feature-build.md "[task]"`
     - 4. Valdate → `flow-qa-valdate.md "[task]"`
     - 5. Fix (Optional) → `flow-feedback-fix.md "[task]"`
     - 6. PR (If ready) → `PR issue`
     - 7. Bug (Optional) → `flow-analyze-bug.md "[task]"`
     - 8. Hooks (Optional) → `config-enforce.md "[task]"`
   - Establish code standards and conventions
   - Specify testing requirements and coverage expectations
   - Document deployment and release processes

6. **Present for Approval**
   - Generate complete CLAUDE.md draft
   - Highlight key strategic decisions
   - Request explicit approval before proceeding

7. **CRITICAL: Invoke hooks-setup Skill**
   - ⚠️ **Remember**: Invoke `hooks-setup` after user approval (see [CRITICAL POST-COMPLETION REQUIREMENT](#️-critical-post-completion-requirement))

8. **Create Session Artifacts**
   - Create session file and modular index JSON (see [SESSION ARTIFACTS](#️-session-artifacts-mandatory---all-modes))

### For Legacy Documentation Migration

When converting existing README, ARCHITECTURE.md, or wiki pages to CLAUDE.md format:

**See**: [Migration Guide](./references/migration-guide.md) for comprehensive migration workflow including:

- **Discovery Checklist**: Finding all existing documentation sources
- **Content Mapping**: Legacy docs → CLAUDE.md sections transformation table
- **Transformation Rules**: Consolidate, enrich, and prune strategies
- **Parallel Maintenance**: Transition approach during migration period

**Key Steps**:

1. Identify all existing documentation sources
2. Map content to CLAUDE.md sections using transformation table
3. Consolidate and enrich information
4. Validate using quality checklist
5. Maintain both old and new docs during transition (1-2 sprints)

### For Existing Projects (Audit & Improve)

When auditing or improving an existing CLAUDE.md:

#### Step 1: Read & Analyze Current State

**Completeness Checklist**:

```markdown
## Section-by-Section Audit

### Strategic Layer

- [ ] `[project_metadata]` - Name, version, objectives present?
- [ ] `[stack]` - Tech choices documented with rationale?
- [ ] `[core_team]` - Agents defined with clear roles?
  - [ ] security-architect included?
  - [ ] acceptance-validator included?

### Technical Layer

- [ ] `[directory_structure]` - Key paths only (not exhaustive)?
- [ ] `[environment_variables]` - All required vars documented?
- [ ] `[commands]` - Essential commands (no duplicates)?
- [ ] `[configuration]` - Config locations specified?

### Global Rules Layer

- [ ] `[workflow]` - Git practices & development process clear?
- [ ] `[code_standards]` - Project-specific conventions?
- [ ] `[testing_requirements]` - NO EXCEPTIONS policy present?
- [ ] `[deployment]` - Release process documented?

### Quality Indicators

- [ ] Quick Reference section exists?
- [ ] ABOUTME headers mentioned in code standards?
- [ ] Length appropriate (500-700 lines standard)?
- [ ] No obvious redundancy (commands/workflows duplicated)?
```

#### Step 2: Prioritization Matrix

Categorize findings by impact:

| Priority        | Category              | Examples                                   | Fix Urgency  |
| --------------- | --------------------- | ------------------------------------------ | ------------ |
| **P0 Critical** | Blocks agent work     | Missing core_team, no testing requirements | Immediate    |
| **P1 High**     | Reduces effectiveness | No Quick Reference, outdated stack         | This session |
| **P2 Medium**   | Quality improvement   | Redundant sections, >1000 lines            | Next update  |
| **P3 Low**      | Nice-to-have          | Additional examples, style consistency     | Future       |

#### Step 3: Compare Against Best Practices

**Good vs Bad Examples**:

✅ **GOOD - Concise Command Section**:

```markdown
## [commands]

pnpm dev # Development server
pnpm build # Production build
pnpm test # Run test suite
```

❌ **BAD - Verbose with Explanations**:

```markdown
## [commands]

Run `pnpm dev` to start the development server on localhost:3000. This will enable hot reloading...
Run `pnpm build` to create an optimized production bundle...
```

✅ **GOOD - Referenced Detail**:

```markdown
### Animation Standards

- Use Framer Motion for interactive animations
- See [Animation Patterns](./.claude/docs/patterns/animations.md) for examples
```

❌ **BAD - Inline 50-line Example**:

```markdown
### Animation Standards

Here's how to create a fade animation:
[50 lines of code example]
```

#### Step 4: Generate Improvement Recommendations

**Output Format**:

```markdown
## CLAUDE.md Audit Report

**Current Score**: 65/100 (Adequate)

### Critical Issues (P0)

1. Missing `security-architect` in `[core_team]` - BLOCKS security validation
2. No `[testing_requirements]` section - NO EXCEPTIONS policy not enforced

### High Priority (P1)

3. Length: 1,250 lines (Target: 500-700) - Extract to separate files
4. Redundancy: Workflow appears in 3 sections - Consolidate

### Recommended Actions

- [ ] Add security-architect and acceptance-validator to core team
- [ ] Create `[testing_requirements]` with NO EXCEPTIONS policy
- [ ] Extract detailed patterns to `.claude/docs/patterns/`
- [ ] Consolidate workflow to single section
- [ ] Add Quick Reference section

**Estimated Post-Fix Score**: 88/100 (Good)
```

#### Step 5: Implement Fixes

- Fix P0 issues automatically (missing required agents)
- Present P1+ recommendations to user with before/after examples
- Generate updated CLAUDE.md with quality report

#### Step 6: Validate Improvements

- Re-run validation framework
- Confirm score improved by at least 20 points
- Ensure no new issues introduced

#### Step 7: Present with Quality Report

- Present updated CLAUDE.md with before/after comparison
- Include validation report showing improvements
- Request approval before overwriting

#### Step 8: Invoke hooks-setup Skill

- ⚠️ **Remember**: Invoke `hooks-setup` after user approval (see [CRITICAL POST-COMPLETION REQUIREMENT](#️-critical-post-completion-requirement))

#### Step 9: Create Session Artifacts

- Create session file and modular index JSON (see [SESSION ARTIFACTS](#️-session-artifacts-mandatory---all-modes))

---

## ⚠️ SESSION ARTIFACTS (MANDATORY - ALL MODES)

**IMPERATIVE: After ANY claude-md-architect execution, you MUST create session tracking artifacts.**

This is **NON-NEGOTIABLE** and applies to ALL modes:
- `create` - New CLAUDE.md
- `audit` - Audit existing
- `improve` - Improve existing
- `recreate` - Replace existing
- `migrate-modular` - Convert to modular

### 1. Create Session File

**Location:** `.claude/sessions/context_session_md_architect_{YYYYMMDD_HHmmss}.md`

**Steps:**
1. Ensure directory exists: `mkdir -p .claude/sessions`
2. Generate timestamp: `YYYYMMDD_HHmmss` format
3. Create file with this template:

```markdown
# MD-Architect Session

## Metadata
- Mode: {MODE}
- Architecture: modular
- Timestamp: {ISO_TIMESTAMP}
- Status: {success|fail}

## Files Created/Verified

### Core File
- CLAUDE.md (lines: {LINE_COUNT})

### Auto-Loaded Rules
{List each file in .claude/rules/*.md}

### Path-Specific Rules
{List each file in .claude/rules/domain/*.md with paths from frontmatter}

### On-Demand Docs
{List each file in .claude/docs/**/*.md}

## Modular Index
{Copy of [modular_index] section from CLAUDE.md}

## Session Log
- {timestamp}: Session started with mode={MODE}
- {timestamp}: Files processed: {count}
- {timestamp}: Session completed with status={STATUS}
```

### 2. Create Modular Index JSON

**Location:** `.claude/cache/modular_index.json`

**Steps:**
1. Ensure directory exists: `mkdir -p .claude/cache`
2. Generate JSON with structure:

```json
{
  "version": "1.0",
  "created": "{ISO_TIMESTAMP}",
  "architecture_mode": "modular",
  "source_claude_md": "CLAUDE.md",
  "session_file": ".claude/sessions/context_session_md_architect_{timestamp}.md",
  "auto_loaded": [
    {"file": ".claude/rules/code-standards.md", "priority": "high"},
    {"file": ".claude/rules/testing-policy.md", "priority": "high"}
  ],
  "path_specific": [
    {"file": ".claude/rules/domain/api-rules.md", "paths": ["app/api/**"]}
  ],
  "on_demand": [
    {"file": ".claude/docs/architecture/tech-stack.md", "load_when": "Stack decisions"}
  ]
}
```

### 3. Validate Session Artifacts

Before completing the task, verify:
- [ ] Session file exists at `.claude/sessions/context_session_md_architect_*.md`
- [ ] Modular index exists at `.claude/cache/modular_index.json`
- [ ] Both files contain valid content

**If validation fails:** Set task status to "fail" and report the error.

---

## CLAUDE.md Structure

A comprehensive CLAUDE.md should include these sections:

### Strategic Section

- **[project_metadata]**: Name, description, version, objectives
- **[stack]**: Technology choices with justification
- **[core_team]**: Required agents and their responsibilities
  - Must include: `security-architect`, `acceptance-validator`
  - Add specialized agents based on project needs

### Technical Context Section

- **[directory_structure]**: Key paths and organization
- **[environment_variables]**: Required env vars and their purpose
- **[commands]**: Essential commands (dev, build, test, deploy)
- **[configuration]**: Config file locations and settings

### Global Rules Section

- **[workflow]**: Development process, git practices, branching
- **[code_standards]**: Conventions, linting, formatting
- **[testing]**: Test requirements, coverage, CI/CD
- **[deployment]**: Release process, environments

### Agent Coordination Section

- **[agent_guidelines]**: How agents should collaborate
- **[communication_patterns]**: When to delegate, escalate, or coordinate

Refer to [references/claude-md-template.md](references/claude-md-template.md) for a complete template with examples.

## Factory Verticals (Default Tech Stacks)

Unless explicitly requested otherwise, prioritize these proven tech stacks:

- **Vertical A**: Astro + React + Tailwind (static/hybrid sites)
- **Vertical B**: Next.js + Supabase (full-stack apps)
- **Vertical C**: Python + AI SDK (AI/ML projects)

See [references/factory-verticals.md](references/factory-verticals.md) for detailed descriptions, use cases, and configuration guidance for each vertical.

## Best Practices

**See**: [Best Practices Examples](./references/best-practices-examples.md) for detailed examples of good vs. bad practices.

### Writing Style

- Use clear, imperative language (be specific and actionable)
- Avoid vague terms like "should consider" - be definitive
- Prefer bullet points over paragraphs for scannability

### Maintainability

- Keep sections modular and clearly separated
- Link to external docs rather than duplicating them
- **Aim for conciseness:** Target 100-300 lines for core CLAUDE.md
- **Use modular architecture:** Auto-loaded rules, path-specific rules, and on-demand docs

### Evolution & Progressive Disclosure

- Version the CLAUDE.md file using semantic versioning
- Review and update quarterly or after major changes
- **Start minimal, grow as needed:** Begin with essential sections only
- **Don't over-document upfront:** Avoid documenting features that don't exist yet

### Team Collaboration

- Get stakeholder buy-in before finalizing
- Share with entire team for feedback
- Make it easily discoverable (repository root)

### Version Control

Treat CLAUDE.md as a versioned contract using semantic versioning:

- **Major (2.0.0)**: Stack change, architecture overhaul, team restructure
- **Minor (1.1.0)**: New sections, significant workflow changes, new agents
- **Patch (1.0.1)**: Corrections, clarifications, minor updates

Maintain version header and `[change_log]` section. See [Best Practices Examples](./references/best-practices-examples.md) for formatting.

## Common Mistakes to Avoid

- **Too generic**: "Build a user authentication system" vs. "Implement JWT-based auth with refresh tokens using Auth0"
- **Outdated**: Listing old dependencies or deprecated patterns
- **Incomplete**: Missing critical sections like environment variables
- **Inconsistent**: Different formatting or detail levels across sections
- **Inflexible**: Not accounting for project evolution and changes
- **Too long core**: Core CLAUDE.md >300 lines (extract to modular files)
- **Redundant**: Repeating the same commands, workflows, or warnings across multiple sections
- **Missing modular files**: Not creating required `.claude/rules/` files
- **Broken references**: `[modular_index]` referencing non-existent files
- **Missing Quick Reference**: No summary section for rapid agent orientation

## Output Format

Always generate a complete modular CLAUDE.md structure that:

- Is properly formatted with markdown
- Includes all required sections (see templates)
- Contains specific, actionable content
- Is tailored to the specific project
- Follows organizational standards (Factory Verticals when applicable)
- **Core CLAUDE.md:** 100-300 lines with `[modular_index]` section
- **Auto-loaded rules:** Code standards, testing, security, git workflow
- **Avoids redundancy:** Each piece of information appears once only
- **Includes Quick Reference:** Summary section for rapid orientation

**Template (Modular - All Projects):**

| Component | Template | Target Lines |
|-----------|----------|--------------|
| Core CLAUDE.md | [claude-md-core.md](references/claude-md-core.md) | 100-300 |
| Global rules | [template-global.md](references/rules/template-global.md) | 50-150 each |
| Path-specific rules | [template-path-specific.md](references/rules/template-path-specific.md) | 50-200 each |
| Architecture docs | [template-architecture.md](references/docs/template-architecture.md) | As needed |

After generating, always request explicit approval before committing to the repository.

⚠️ **Remember**: Invoke `hooks-setup` after user approval (see [CRITICAL POST-COMPLETION REQUIREMENT](#️-critical-post-completion-requirement))

---

## Modular Generation Mode

### Overview

All projects use modular architecture, which provides a lightweight core CLAUDE.md (100-300 lines) with intelligent references to specialized documents.

**Benefits of Modular Architecture:**

| Metric | Benefit |
|--------|---------|
| Initial tokens | ~4,000 (73% reduction from monolithic) |
| CLAUDE.md lines | 100-300 (focused core) |
| Parse time | Low (efficient agent context) |
| Maintainability | High (separation of concerns) |
| Scalability | Excellent (add rules/docs as needed) |

### Modular Architecture

```
project/
├── CLAUDE.md                          # Core: 100-300 lines
├── .claude/
│   ├── rules/                         # AUTO-LOADED (every task)
│   │   ├── code-standards.md          # Coding conventions
│   │   ├── testing-policy.md          # Test requirements
│   │   ├── security-policy.md         # Security guidelines
│   │   ├── git-workflow.md            # Git practices
│   │   ├── agent-coordination.md      # Agent collaboration
│   │   └── domain/                    # PATH-SPECIFIC rules
│   │       ├── api-rules.md           # paths: src/api/**
│   │       ├── ui-rules.md            # paths: src/components/**
│   │       └── test-rules.md          # paths: tests/**
│   │
│   ├── docs/                          # ON-DEMAND loading
│   │   ├── architecture/
│   │   │   ├── tech-stack.md          # Full stack details
│   │   │   ├── database-schema.md     # DB documentation
│   │   │   └── api-contracts.md       # API specifications
│   │   ├── patterns/
│   │   │   ├── auth-flows.md          # Auth implementation
│   │   │   └── error-handling.md      # Error patterns
│   │   └── guides/
│   │       └── deployment.md          # Deploy procedures
│   │
│   └── examples/                      # Code examples
│       └── [templates]
```

### Loading Protocol

**1. Auto-Loaded (Every Task):**
- Files in `.claude/rules/` (without `domain/`)
- Loaded automatically by Claude Code
- Keep concise: 50-150 lines per file

**2. Path-Specific (Matching Tasks):**
- Files in `.claude/rules/domain/`
- YAML frontmatter specifies paths
- Loaded only when working on matching files

```yaml
---
description: API-specific rules
paths:
  - "src/api/**"
  - "src/routes/**"
---
```

**3. On-Demand (Referenced):**
- Files in `.claude/docs/`
- Referenced in CLAUDE.md `[modular_index]`
- Load manually when needed for specific work

### Modular Generation Workflow

When generating in modular mode:

**Step 1: Generate Core CLAUDE.md**
- Use [claude-md-core.md](references/claude-md-core.md) template
- Include only essential sections
- Target 100-300 lines
- Add `[modular_index]` section

**Step 2: Generate Global Rules**
- Create files in `.claude/rules/`:
  - `code-standards.md` - From `[code_standards]` section
  - `testing-policy.md` - From `[testing_requirements]` section
  - `security-policy.md` - From `[security_requirements]` section
  - `git-workflow.md` - From workflow section
  - `agent-coordination.md` - From `[agent_guidelines]` section
- Use [template-global.md](references/rules/template-global.md) as reference

**Step 3: Generate Path-Specific Rules (if needed)**
- Create files in `.claude/rules/domain/`:
  - `api-rules.md` - For API-specific conventions
  - `ui-rules.md` - For UI component rules
  - `test-rules.md` - For testing conventions
- Use [template-path-specific.md](references/rules/template-path-specific.md) as reference

**Step 4: Generate Architecture Docs (if needed)**
- Create files in `.claude/docs/architecture/`:
  - `tech-stack.md` - Detailed stack documentation
  - `database-schema.md` - Full schema docs
  - `api-contracts.md` - API specifications
- Use [template-architecture.md](references/docs/template-architecture.md) as reference

**Step 5: Update modular_index**
- List all auto-loaded rules
- List all path-specific rules with their paths
- List all on-demand docs with load triggers

### Migration Mapping

Use this table when migrating from monolithic to modular:

| Original Section | Destination | Load Type |
|-----------------|-------------|-----------|
| `[code_standards]` >50 lines | `.claude/rules/code-standards.md` | Auto |
| `[testing_requirements]` | `.claude/rules/testing-policy.md` | Auto |
| `[security_requirements]` | `.claude/rules/security-policy.md` | Auto |
| Git workflow content | `.claude/rules/git-workflow.md` | Auto |
| `[agent_guidelines]` | `.claude/rules/agent-coordination.md` | Auto |
| API-specific rules | `.claude/rules/domain/api-rules.md` | Path-specific |
| UI-specific rules | `.claude/rules/domain/ui-rules.md` | Path-specific |
| Database schema | `.claude/docs/architecture/database-schema.md` | On-demand |
| API contracts | `.claude/docs/architecture/api-contracts.md` | On-demand |
| Deployment guide | `.claude/docs/guides/deployment.md` | On-demand |
| Code examples >20 lines | `.claude/examples/` | On-demand |

### Mode Handling

All projects use modular architecture:

```
IF .claude/rules/ has files:
  MODE: "modular" (already modular)
  ACTION: Validate reference integrity

ELSE IF CLAUDE.md exists AND lines > 300:
  MODE: "migrate-modular"
  ACTION: Automatically migrate to modular structure

ELSE:
  MODE: "modular" (create new)
  ACTION: Generate full modular structure
```

### Modular Validation

After generating modular structure, validate:

1. **File Existence**
   - All referenced files in `[modular_index]` exist
   - No orphan files (unreferenced docs)

2. **Reference Integrity**
   - All paths in path-specific rules are valid
   - No circular references

3. **Completeness**
   - Core CLAUDE.md has all required sections
   - Global rules cover essential policies
   - `[modular_index]` is up-to-date

4. **Size Compliance**
   - Core CLAUDE.md: 100-300 lines
   - Global rules: 50-150 lines each
   - Path-specific rules: 50-200 lines each

See [Validation Checklist](./references/validation-checklist.md) for complete validation framework.

### Templates Reference

| Template | Purpose | Location |
|----------|---------|----------|
| Core CLAUDE.md | Modular core document | [claude-md-core.md](references/claude-md-core.md) |
| Global Rules | Auto-loaded rules | [template-global.md](references/rules/template-global.md) |
| Path-Specific Rules | Domain rules with frontmatter | [template-path-specific.md](references/rules/template-path-specific.md) |
| Architecture Docs | On-demand technical docs | [template-architecture.md](references/docs/template-architecture.md) |
