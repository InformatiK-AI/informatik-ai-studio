# CLAUDE.md Core Template (Modular Architecture)

This template is for modular CLAUDE.md files that use the `.claude/rules/` and `.claude/docs/` structure for separation of concerns.

**Target Length**: 100-300 lines (core only, details in modular files)
**Use When**: Projects exceeding 500 lines in monolithic CLAUDE.md, or new projects wanting scalable documentation

---

## Template

```markdown
# [Project Name]

> Version: 1.0.0 | Status: Development | Architecture: Modular

## [project_metadata]

| Field | Value |
|-------|-------|
| Name | [Project Name] |
| Description | [1-2 sentence description] |
| Repository | [URL] |
| Created | [Date] |
| Last Updated | [Date] |

### Objectives

1. [Primary objective]
2. [Secondary objective]
3. [Tertiary objective]

---

## [stack]

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Vertical | [A/B/C] | - | Astro/Next.js/Python |
| Framework | [Name] | [Version] | [Brief note] |
| Language | [Name] | [Version] | - |
| Database | [Name] | [Version] | If applicable |
| Styling | [Name] | [Version] | - |
| Testing | [Name] | [Version] | - |

### Stack Rationale

[2-3 sentences explaining why this stack was chosen]

---

## [core_team]

### Mandatory Agents

#### @security-architect
- **Invoke When**: Before merging auth, data, or security features
- **Output**: `security_plan.md`

#### @acceptance-validator
- **Invoke When**: Before marking features complete
- **Output**: Validation report

### Specialist Agents (As Needed)

| Agent | Trigger | Responsibility |
|-------|---------|----------------|
| @database-architect | Schema changes | Database design |
| @api-contract-designer | API work | Contract design |
| @domain-logic-architect | Backend logic | Business logic |
| @frontend-architect | UI/Components | Frontend architecture |

---

## [quick_reference]

### Commands

```bash
[package_manager] dev        # Start development server
[package_manager] build      # Production build
[package_manager] test       # Run test suite
[package_manager] lint       # Run linter
```

### Key Files

| Purpose | Path |
|---------|------|
| Entry Point | `[path]` |
| Main Config | `[path]` |
| Environment | `.env.local` |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `[VAR_NAME]` | Yes/No | [Brief description] |

---

## [workflow]

### Development Process

1. **Plan** → `flow-plan "[task]"`
2. **Contract** → `flow-issue-create "[task]"`
3. **Build** → `flow-feature-build "[issue]"`
4. **Validate** → `flow-qa-validate "[PR]"`
5. **Fix** (if needed) → `flow-feedback-fix "[PR]"`

### Git Workflow

- **Branching**: `feature/{issue-number}-{short-description}`
- **Commits**: Conventional Commits format
- **PRs**: Require 1 approval + passing CI

---

## [modular_index]

### Auto-Loaded Rules (.claude/rules/)

These files are automatically loaded by Claude Code for every task:

| File | Purpose | Priority |
|------|---------|----------|
| `code-standards.md` | Coding conventions and style | High |
| `testing-policy.md` | Test requirements and coverage | High |
| `security-policy.md` | Security guidelines | Critical |
| `git-workflow.md` | Git/commit practices | Medium |
| `agent-coordination.md` | Agent collaboration rules | Medium |

### Path-Specific Rules (.claude/rules/domain/)

Auto-loaded only for matching file paths:

| File | Paths | Purpose |
|------|-------|---------|
| `api-rules.md` | `src/api/**`, `src/routes/**` | API-specific rules |
| `ui-rules.md` | `src/components/**`, `src/pages/**` | UI-specific rules |
| `test-rules.md` | `tests/**`, `**/*.test.*` | Test-specific rules |

### On-Demand Documentation (.claude/docs/)

Load these when working on specific features:

| File | Load When | Content |
|------|-----------|---------|
| `architecture/tech-stack.md` | Stack decisions | Full stack details |
| `architecture/database-schema.md` | DB changes | Schema documentation |
| `architecture/api-contracts.md` | API work | OpenAPI/contract specs |
| `patterns/auth-flows.md` | Auth features | Authentication patterns |
| `patterns/error-handling.md` | Error work | Error handling guide |
| `guides/deployment.md` | Deploy tasks | Deployment procedures |

---

## [change_log]

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | [Date] | Initial modular architecture |

```

---

## Directory Structure

When using this template, ensure the following directory structure exists:

```
project/
├── CLAUDE.md                          # This file (100-300 lines)
├── .claude/
│   ├── rules/                         # Auto-loaded (every task)
│   │   ├── code-standards.md          # Coding conventions
│   │   ├── testing-policy.md          # Test requirements
│   │   ├── security-policy.md         # Security guidelines
│   │   ├── git-workflow.md            # Git practices
│   │   ├── agent-coordination.md      # Agent collaboration
│   │   └── domain/                    # Path-specific rules
│   │       ├── api-rules.md           # paths: src/api/**
│   │       ├── ui-rules.md            # paths: src/components/**
│   │       └── test-rules.md          # paths: tests/**
│   │
│   ├── docs/                          # On-demand loading
│   │   ├── architecture/
│   │   │   ├── tech-stack.md
│   │   │   ├── database-schema.md
│   │   │   └── api-contracts.md
│   │   ├── patterns/
│   │   │   ├── auth-flows.md
│   │   │   └── error-handling.md
│   │   └── guides/
│   │       └── deployment.md
│   │
│   └── examples/                      # Code examples
│       └── [component-template.tsx]
```

---

## Migration Guide

To migrate from monolithic CLAUDE.md to modular:

1. **Identify extractable sections** (>50 lines each):
   - Code standards → `.claude/rules/code-standards.md`
   - Testing requirements → `.claude/rules/testing-policy.md`
   - Security requirements → `.claude/rules/security-policy.md`
   - Git workflow → `.claude/rules/git-workflow.md`
   - Database schema → `.claude/docs/architecture/database-schema.md`
   - API contracts → `.claude/docs/architecture/api-contracts.md`

2. **Extract and reference**:
   - Move content to appropriate modular file
   - Replace section in CLAUDE.md with brief summary + reference to modular file
   - Update `[modular_index]` section

3. **Validate**:
   - CLAUDE.md should be 100-300 lines
   - All critical rules in `.claude/rules/` (auto-loaded)
   - Detailed docs in `.claude/docs/` (on-demand)

---

## Token Efficiency

| Architecture | Lines | Est. Tokens | Context % |
|--------------|-------|-------------|-----------|
| Monolithic | 800-1000 | ~15,000 | ~7.5% |
| **Modular** | 100-300 | ~4,000 | ~2% |
| Rules (auto) | ~200 | ~3,000 | ~1.5% |
| **Total Initial** | - | ~7,000 | **~3.5%** |

**Savings**: 53% reduction in initial context load
