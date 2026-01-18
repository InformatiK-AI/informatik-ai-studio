# Skills vs Agents: Quick Reference Guide

## Overview

This project uses two types of specialized components:
- **Skills** (34 total) - User-directed tools with specific workflows
- **Agents** (10 total) - Autonomous specialists for planning and design

## Cross-References: Agent ↔ Skill Relationships

Agents produce plans, skills help implement and validate them:

| Agent | Related Skills | Integration |
|-------|----------------|-------------|
| `database-architect` | `senior-backend`, `senior-data-engineer` | Schema plans → backend implements migrations |
| `api-contract-designer` | `senior-backend`, `api-integration-specialist` | API specs → backend implements endpoints |
| `domain-logic-architect` | `senior-backend`, `senior-fullstack` | Business logic plans → backend implements |
| `frontend-architect` | `senior-frontend`, `frontend-design`, `react-best-practices`, `ui-design-system` | UI plans → frontend implements components |
| `security-architect` | `senior-security`, `code-reviewer` | Security plans → security reviews code |
| `devops-architect` | `senior-devops`, `ci-cd-architect` | Infra plans → devops implements pipelines |
| `test-strategy-planner` | `acceptance-validator`, `code-reviewer` | Test plans → validator defines AC |
| `implementation-test-engineer` | `code-reviewer` | Writes tests → reviewer validates |
| `experience-analyzer` | `ux-researcher-designer`, `ui-design-system` | UX analysis → design implements |
| `n8n-architect` | `senior-fullstack`, `api-integration-specialist` | Workflow plans → fullstack implements |

## Workflow Integration

### Full Feature Build Flow

```
Phase 0: preflight-check skill (validation gate)
    ↓
Phase 1: Agents plan in sequence:
    database-architect → api-contract-designer → domain-logic-architect
                                               → frontend-architect
                                               → devops-architect
    ↓
Phase 1.5: implementation-orchestrator skill (validates coherence)
    ↓
Phase 2: Mandatory gates:
    security-architect (blocks if issues)
    test-strategy-planner → implementation-test-engineer
    ↓
Phase 3: code-reviewer skill (pre-PR review)
    ↓
Phase 4: acceptance-validator skill (QA validation)
```

### Common Agent → Skill Handoffs

1. **Database Design**
   - `@database-architect` creates schema plan
   - `/senior-backend` guides migration implementation

2. **API Development**
   - `@api-contract-designer` creates OpenAPI spec
   - `/api-integration-specialist` guides client integration

3. **Frontend Development**
   - `@frontend-architect` plans components and state
   - `/frontend-design` ensures high-quality UI
   - `/react-best-practices` optimizes performance

4. **Security Review**
   - `@security-architect` identifies vulnerabilities
   - `/senior-security` provides implementation guidance
   - `/code-reviewer` validates fixes

## Key Differences

| Aspect | Skills | Agents |
|--------|--------|--------|
| **Location** | `.claude/skills/{name}/SKILL.md` | `.claude/agents/{name}.md` |
| **Structure** | Directory with SKILL.md + README + references/ | Single markdown file |
| **Invocation** | `/skill-name command args` | `@agent-name` |
| **Scope** | Specific tool/task with defined workflows | Autonomous specialist for planning |
| **Output** | Tools, checklists, templates, reports | Plans, architectural documents |
| **Autonomy** | User-directed execution | Autonomous with given context |

## Invocation Syntax

### Skills (use slash command)
```
/acceptance-validator define {feature}    # Define acceptance criteria
/acceptance-validator validate {feature}  # Validate implementation
/preflight-check                          # Run pre-flight validation
/code-reviewer analyze {file}             # Review code
```

### Agents (use @ mention)
```
@security-architect                       # Security planning
@database-architect                       # Database schema design
@domain-logic-architect                   # Backend architecture
@implementation-test-engineer             # Write tests
```

## Common Mistakes

### Wrong: Using @ for skills
```
@acceptance-validator  # WRONG - this is a skill, not an agent
```

### Correct: Using / for skills
```
/acceptance-validator validate {feature}  # CORRECT
```

## Skills Categorization

### Command-Invoked Skills (10 skills)
These skills are automatically invoked by workflow commands:

| Skill | Invoked By | Purpose |
|-------|------------|---------|
| `acceptance-validator` | `flow-qa-validate` | QA gatekeeper, define/validate AC |
| `preflight-check` | `flow-feature-build` Phase 0 | Pre-implementation validation |
| `implementation-orchestrator` | `flow-feature-build` Phase 1.5 | Coordinate agent plans |
| `code-reviewer` | `flow-feature-build` Phase 3 | Pre-PR code review |
| `dependency-installer` | `preflight-check` (auto-fix) | Install missing dependencies |
| `claude-md-architect` | `flow-md-architect` | Create/audit CLAUDE.md |
| `hooks-setup` | After CLAUDE.md creation | Configure Git/Claude hooks |
| `ci-cd-architect` | `flow-feature-build` (DevOps) | Generate CI/CD configs |
| `env-configurator` | After CLAUDE.md creation | Generate .env templates |
| `skill-creator` | Manual | Create new skills |

### Manual-Only Skills (25 skills)
These skills are invoked directly by users for expert guidance:

**Architecture & Design:**
- `senior-architect` - System architecture guidance
- `senior-frontend` - Frontend best practices
- `senior-backend` - Backend best practices
- `senior-fullstack` - Full-stack guidance
- `senior-devops` - DevOps guidance
- `senior-security` - Security guidance
- `senior-data-engineer` - Data engineering guidance
- `senior-data-scientist` - Data science guidance

**Content & UX:**
- `content-creator` - Marketing content
- `content-research-writer` - Research-backed content
- `ux-researcher-designer` - UX research tools
- `ui-design-system` - Design system toolkit
- `seo-optimizer` - SEO optimization

**Development Tools:**
- `react-best-practices` - React performance rules
- `frontend-design` - High-quality frontend interfaces
- `mcp-builder` - Build MCP servers
- `api-integration-specialist` - API integration guidance
- `artifacts-builder` - Complex HTML artifacts
- `theme-factory` - Styling artifacts with themes

**Specialized:**
- `brainstorming` - Creative exploration before implementation
- `writing-plans` - Multi-step task planning
- `agent-librarian` - Find/draft specialist agents
- `cto-advisor` - Technical leadership guidance

## Skills Registry (Key Skills)

| Skill | Purpose | Invocation |
|-------|---------|------------|
| `acceptance-validator` | QA gatekeeper, define/validate AC | `/acceptance-validator define/validate {feature}` |
| `preflight-check` | Pre-implementation validation | Run before `flow-feature-build` |
| `implementation-orchestrator` | Coordinate agent plans | Used in Phase 1.5 of flow-feature-build |
| `code-reviewer` | Automated code review | `/code-reviewer analyze {file}` |
| `claude-md-architect` | Create/audit CLAUDE.md | `/claude-md-architect create/audit` |

## Agents Registry (All Agents - 10 total)

| Agent | Purpose | Output |
|-------|---------|--------|
| `database-architect` | Schema design, migrations | `database.md` |
| `domain-logic-architect` | Backend business logic | `backend.md` |
| `api-contract-designer` | API contracts (REST/GraphQL/gRPC) | `api_contract.md` |
| `frontend-architect` | Frontend architecture, state, routing, UI components | `frontend.md` |
| `security-architect` | Security validation | `security_plan.md` |
| `devops-architect` | CI/CD, infrastructure | `devops.md` |
| `test-strategy-planner` | Test planning (Gherkin) | `test_cases.md` |
| `implementation-test-engineer` | Write actual test code | Test files |
| `experience-analyzer` | UX/DX analysis | `experience_analysis.md` |
| `n8n-architect` | Workflow automation | `n8n-workflow-plan.md` |

## Decision Tree: Skill or Agent?

```
Is the task about...

Planning/Architecture?
  └─> Use AGENT (@agent-name)
      Examples: database design, API contracts, security planning

Quality Validation?
  └─> Use SKILL (/skill-name)
      Examples: acceptance criteria, code review, pre-flight checks

Specific Tool/Workflow?
  └─> Use SKILL (/skill-name)
      Examples: dependency installation, CI/CD configuration
```

## Integration in Commands

Commands should reference skills and agents correctly:

```markdown
# Correct usage in commands

## Using a skill
Invoke `/acceptance-validator validate {feature}` skill...

## Using an agent
Invoke `@security-architect` agent...
```

## Version

**Last Updated:** 2026-01-17
**Version:** 1.2

### Changelog
- v1.2: Added Cross-References section mapping agents to related skills
- v1.2: Added Workflow Integration section showing agent/skill handoffs
- v1.2: Fixed skill count (34, not 35)
- v1.1: Added Skills Categorization (Command-Invoked vs Manual-Only)
- v1.1: Removed non-existent agents (presentation-layer-architect, ui-component-architect)
- v1.1: Consolidated UI functionality into frontend-architect
- v1.0: Initial release
