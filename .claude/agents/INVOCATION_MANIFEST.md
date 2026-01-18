# Agent Invocation Manifest

This document defines the invocation order, dependencies, and triggers for all agents in the `.claude/agents/` directory.

## Agent Invocation Order (DAG)

```
                    ┌─────────────────────┐
                    │  database-architect │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ api-contract-designer│
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│domain-logic-architect│ │frontend-architect│ │   devops-architect  │
└──────────┬──────────┘ └────────┬────────┘ └─────────────────────┘
           │                     │
           └──────────┬──────────┘
                      │
                      ▼
           ┌─────────────────────┐
           │  security-architect │  ◄─── MANDATORY GATE
           └──────────┬──────────┘
                      │
                      ▼
         ┌───────────────────────┐
         │implementation-test-   │
         │     engineer          │
         └───────────────────────┘
```

## Agent Triggers & Dependencies

| Agent | Triggers When | Requires First | Produces | Feeds Into |
|-------|---------------|----------------|----------|------------|
| `database-architect` | Database schema changes | CLAUDE.md | `database.md` | api-contract-designer |
| `api-contract-designer` | API endpoints needed | database.md (if applicable) | `api_contract.md` | domain-logic, frontend |
| `domain-logic-architect` | Backend logic needed | api_contract.md (if applicable) | `backend.md` | security-architect |
| `frontend-architect` | UI/frontend needed | api_contract.md (if applicable) | `frontend.md` | security-architect |
| `devops-architect` | Deployment/CI-CD needed | CLAUDE.md | `devops.md` | - |
| `security-architect` | **ALWAYS (mandatory)** | All architecture plans | `security_plan.md` | implementation |
| `test-strategy-planner` | Tests needed | All architecture plans | `test_cases.md` | implementation-test-engineer |
| `implementation-test-engineer` | Writing tests | test_cases.md | Test files | - |
| `experience-analyzer` | UX/DX analysis needed | Implementation | `experience_analysis.md` | - |
| `n8n-architect` | Workflow automation | CLAUDE.md | `n8n-workflow-plan.md` | - |

## Feature Type → Agent Combinations

### Backend-Only Feature
```
database-architect → api-contract-designer → domain-logic-architect → security-architect
```

### Frontend-Only Feature
```
frontend-architect → security-architect
```

### Full-Stack Feature
```
database-architect → api-contract-designer → domain-logic-architect
                                          → frontend-architect
                                          ↓
                                    security-architect (reviews ALL plans)
```

### Infrastructure Feature
```
devops-architect → security-architect
```

### Workflow Automation Feature
```
n8n-architect → security-architect
```

## Mandatory Agents

The following agents **MUST** be invoked regardless of feature type:

1. **`security-architect`** - Reviews all plans for security vulnerabilities (OWASP Top 10)
2. **`implementation-test-engineer`** - Ensures tests are written (TDD/RAD workflows)

## Conditional Invocation Rules

```
IF feature involves database changes:
    INVOKE database-architect FIRST
    WAIT for database.md

IF feature involves API:
    INVOKE api-contract-designer
    WAIT for api_contract.md

IF feature involves backend logic:
    INVOKE domain-logic-architect
    INPUT: api_contract.md (if exists)

IF feature involves frontend:
    INVOKE frontend-architect
    INPUT: api_contract.md (if exists)

IF feature involves deployment:
    INVOKE devops-architect

ALWAYS:
    INVOKE security-architect LAST (before implementation)
    INPUT: ALL generated plan files
```

## Plan Coherence Validation

Before proceeding to implementation, validate that all plans are coherent:

| Check | Plans Involved | Validation |
|-------|----------------|------------|
| Database ↔ API | database.md, api_contract.md | Schema types match API DTOs |
| API ↔ Backend | api_contract.md, backend.md | Endpoints have handlers |
| API ↔ Frontend | api_contract.md, frontend.md | Frontend calls correct endpoints |
| All ↔ Security | All plans, security_plan.md | No security gaps identified |

## Invocation in Commands

### flow-feature-build
- **Phase 0**: Pre-flight check (validates agent availability)
- **Phase 1.5**: Plan validation (ensures all plans exist and are coherent)
- **Phase 2**: Dynamic agent invocation based on feature type
- **Phase 3**: Validation with security-architect

### flow-qa-validate
- Invokes `security-architect` for security review
- Invokes `acceptance-validator` skill for AC validation

## Agent Status Indicators

When invoking agents, use these status indicators:

| Status | Meaning |
|--------|---------|
| `PENDING` | Agent not yet invoked |
| `IN_PROGRESS` | Agent is working on plan |
| `COMPLETED` | Plan generated successfully |
| `BLOCKED` | Waiting for dependency |
| `FAILED` | Agent encountered error |

## Version

**Last Updated:** 2026-01-17
**Version:** 1.0
