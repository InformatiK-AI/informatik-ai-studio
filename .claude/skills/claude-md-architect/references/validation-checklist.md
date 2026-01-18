# CLAUDE.md Validation Checklist

Use this checklist when auditing or generating CLAUDE.md files.

**Architecture:** All projects use **modular architecture**:
- **Core CLAUDE.md:** 100-300 lines (strategic context and index)
- **Auto-loaded rules:** `.claude/rules/` (50-150 lines each)
- **Path-specific rules:** `.claude/rules/domain/` (50-200 lines each)
- **On-demand docs:** `.claude/docs/` (reference material)

---

## Required Sections (Standard Projects)

### Strategic Layer

- [ ] `[project_metadata]` with name, description, version, objectives
- [ ] `[stack]` with technology choices and rationale
- [ ] `[core_team]` with defined agent roles
  - [ ] `security-architect` included
  - [ ] `acceptance-validator` included

### Technical Layer

- [ ] `[directory_structure]` showing key paths only
- [ ] `[environment_variables]` if applicable (can be "None" for static sites)
- [ ] `[commands]` with essential commands only

### Global Rules Layer

- [ ] `[workflow]` with git practices and development process
- [ ] `[code_standards]` with project-specific conventions
- [ ] `[testing_requirements]` with NO EXCEPTIONS policy
- [ ] `[deployment]` if applicable

### Quality Markers

- [ ] Quick Reference section (top or bottom)
- [ ] Core CLAUDE.md length: 100-300 lines
- [ ] `[modular_index]` section present and complete
- [ ] No redundant sections (commands/workflows duplicated)
- [ ] All referenced modular files exist

## Optional Sections (Add as Needed)

- [ ] `[security_requirements]` - Detailed security policies
- [ ] `[performance_requirements]` - Performance targets and metrics
- [ ] `[roadmap]` - Feature roadmap and technical debt
- [ ] `[glossary]` - Project-specific terminology
- [ ] `[change_log]` - Version history of CLAUDE.md itself

## Common Issues Checklist

### Length Issues

- [ ] Core CLAUDE.md is 100-300 lines
- [ ] Estimated tokens <5,000 for core (multiply lines × 15)
- [ ] Auto-loaded rules are 50-150 lines each
- [ ] No >50 line code examples (extract to `.claude/examples/`)

### Redundancy Issues

- [ ] Commands listed once only (not in multiple sections)
- [ ] Workflow described once only (reference elsewhere)
- [ ] No duplicate warnings or emphasis statements

### Clarity Issues

- [ ] Section headers use consistent format: `## [section_name]`
- [ ] Bullet points used over long paragraphs
- [ ] Code blocks have language tags
- [ ] Tables used for comparison data

### Completeness Issues

- [ ] All environment variables have descriptions
- [ ] Tech stack choices include rationale
- [ ] Agent roles specify when to invoke
- [ ] Testing requirements specify coverage expectations

## Scoring Rubric (Modular Architecture)

| Criterion | Points | How to Score |
|-----------|--------|--------------|
| **Core Length** | 20 | 20pts if 100-300 lines, -5pts per 50 lines over |
| **Rules Existence** | 20 | 4pts per required rule file (code-standards, testing, security, git-workflow, agent-coordination) |
| **Rules Quality** | 15 | 3pts per file that's 50-150 lines |
| **Reference Integrity** | 20 | 20pts if all refs valid, -4pts per broken ref |
| **Index Completeness** | 15 | 15pts if all files indexed in `[modular_index]` |
| **No Orphans** | 10 | 10pts if no orphan files, -2pts per orphan |

**Total**: 100 points

**Quality Bands**:

- 90-100: Excellent modular structure
- 75-89: Good, minor cleanup needed
- 60-74: Adequate, some references may be broken
- <60: Needs restructuring

---

## Modular Validation (Required for All Projects)

### Core CLAUDE.md Validation

- [ ] File exists at project root
- [ ] Length: 100-300 lines
- [ ] Contains `[modular_index]` section with all file references
- [ ] All required sections present: `[project_metadata]`, `[stack]`, `[core_team]`, `[commands]`
- [ ] Detailed rules extracted to `.claude/rules/`

### Auto-Loaded Rules (.claude/rules/)

**File Existence:**
- [ ] `.claude/rules/code-standards.md` exists
- [ ] `.claude/rules/testing-policy.md` exists
- [ ] `.claude/rules/security-policy.md` exists
- [ ] `.claude/rules/git-workflow.md` exists
- [ ] `.claude/rules/agent-coordination.md` exists

**File Quality:**
- [ ] Each file is 50-150 lines (concise)
- [ ] Each file has clear structure and headers
- [ ] No duplicate content across files
- [ ] Actionable rules (not vague guidance)

### Path-Specific Rules (.claude/rules/domain/)

**If path-specific rules exist:**
- [ ] Each file has valid YAML frontmatter
- [ ] `paths` array contains valid glob patterns
- [ ] Patterns match intended file paths
- [ ] No overlapping/conflicting paths between files
- [ ] Each file is 50-200 lines

**Frontmatter Validation:**
```yaml
---
description: [Required - one line]
paths:
  - "src/api/**"    # Valid glob pattern
  - "**/*.api.ts"   # Valid glob pattern
---
```

### On-Demand Docs (.claude/docs/)

**Reference Integrity:**
- [ ] All files in `[modular_index]` exist
- [ ] No orphan files (exist but not referenced)
- [ ] Load triggers are accurate

**Architecture Docs:**
- [ ] `architecture/tech-stack.md` - if referenced
- [ ] `architecture/database-schema.md` - if DB project
- [ ] `architecture/api-contracts.md` - if API project

**Patterns/Guides:**
- [ ] Files are comprehensive but focused
- [ ] Each file covers ONE topic

### Modular Index Validation

The `[modular_index]` section must be complete and accurate:

```markdown
## [modular_index]

### Auto-Loaded Rules (.claude/rules/)
| File | Purpose |
|------|---------|
| code-standards.md | ✓ Must exist |
| testing-policy.md | ✓ Must exist |
| ... | ... |

### Path-Specific Rules (.claude/rules/domain/)
| File | Paths | Purpose |
|------|-------|---------|
| api-rules.md | src/api/** | ✓ Paths must be valid |
| ... | ... | ... |

### On-Demand Documentation (.claude/docs/)
| File | Load When | Content |
|------|-----------|---------|
| architecture/database-schema.md | DB changes | ✓ Must exist |
| ... | ... | ... |
```

### Common Issues

**Reference Errors:**
- [ ] File referenced in index but doesn't exist
- [ ] File exists but not in index (orphan)
- [ ] Path pattern syntax errors in frontmatter

**Size Violations:**
- [ ] Core CLAUDE.md >300 lines (should extract more)
- [ ] Rule files >150 lines (should split)
- [ ] Single doc file >500 lines (should split)

**Structure Issues:**
- [ ] Missing required rule files
- [ ] Domain rules without frontmatter
- [ ] Duplicate content across files

### Migration Checklist (Legacy Projects)

When migrating existing monolithic CLAUDE.md to modular architecture:

**Pre-Migration:**
- [ ] Backup original CLAUDE.md
- [ ] Count lines in each section
- [ ] Identify sections >50 lines for extraction

**During Migration:**
- [ ] Extract code standards → `.claude/rules/code-standards.md`
- [ ] Extract testing policy → `.claude/rules/testing-policy.md`
- [ ] Extract security policy → `.claude/rules/security-policy.md`
- [ ] Extract git workflow → `.claude/rules/git-workflow.md`
- [ ] Extract agent guidelines → `.claude/rules/agent-coordination.md`
- [ ] Extract DB schema → `.claude/docs/architecture/database-schema.md`
- [ ] Extract API contracts → `.claude/docs/architecture/api-contracts.md`
- [ ] Update CLAUDE.md with `[modular_index]` section

**Post-Migration:**
- [ ] Core CLAUDE.md is 100-300 lines
- [ ] All extracted files exist
- [ ] All references in index are valid
- [ ] Run validation checklist above
- [ ] Token count reduced (verify with estimation)
