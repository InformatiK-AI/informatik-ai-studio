# Skill Dependency Graph

Visual representation of skill dependencies, prerequisites, and workflow phases.

## Workflow Phases

```
Phase 1: PROJECT SETUP
    claude-md-architect
           │
           ├──────────────────┐
           ▼                  ▼
      hooks-setup      env-configurator
           │
           ▼
Phase 2: IDEATION
      brainstorming (mandatory)
           │
           ▼
Phase 3: PLANNING
      writing-plans
           │
           ▼
Phase 4: PRE-IMPLEMENTATION
      preflight-check ─────────┐
           │                   │ (on failure)
           │                   ▼
           │           dependency-installer
           ▼
Phase 5: AGENT COORDINATION
  implementation-orchestrator
           │
           ▼
Phase 6: PRE-MERGE
      code-reviewer (mandatory)
           │
           ▼
Phase 7: QA VALIDATION
  acceptance-validator (mandatory, gate)
```

## Dependency Matrix

| Skill | Prerequisites | Triggers | Triggered By |
|-------|--------------|----------|--------------|
| claude-md-architect | - | hooks-setup, env-configurator | - |
| hooks-setup | - | - | claude-md-architect |
| env-configurator | - | - | claude-md-architect |
| brainstorming | - | writing-plans | - |
| writing-plans | brainstorming | - | - |
| preflight-check | - | dependency-installer (on failure) | flow-feature-build start |
| implementation-orchestrator | preflight-check | - | - |
| code-reviewer | implementation-orchestrator | - | - |
| acceptance-validator | code-reviewer | - | - |

## Auto-Triggers

### On CLAUDE.md Change
```
CLAUDE.md created/modified
         │
         ├── hooks-setup
         │
         └── env-configurator
```

### On Feature Build Start
```
flow-feature-build start
         │
         └── preflight-check
                   │
                   ├── (success) → implementation-orchestrator
                   │
                   └── (failure) → dependency-installer → retry
```

## Mandatory Gates

| Skill | Phase | Condition |
|-------|-------|-----------|
| brainstorming | Before implementation | Must run before any creative work |
| code-reviewer | Before merge | Must pass before PR can be merged |
| acceptance-validator | QA validation | Must validate all acceptance criteria |

## Execution Order (Feature Development)

```
1. brainstorming
         ↓
2. writing-plans
         ↓
3. preflight-check ──(fail)──→ dependency-installer
         ↓                              ↓
         ←─────────────────────────────┘
         ↓
4. implementation-orchestrator
         ↓
    ┌────┴────┐
    │ AGENTS  │ (coordinated by orchestrator)
    │ DAG     │
    └────┬────┘
         ↓
5. code-reviewer
         ↓
6. acceptance-validator
         ↓
    [READY FOR MERGE]
```

## Integration with Agent DAG

The skill dependency graph integrates with the agent execution DAG:

```
                        SKILLS                              AGENTS
                          │                                   │
              ┌───────────┼───────────┐                      │
              │           │           │                      │
              ▼           ▼           ▼                      │
         preflight   brainstorming  writing                  │
           check                    plans                    │
              │           │           │                      │
              └───────────┼───────────┘                      │
                          │                                  │
                          ▼                                  │
              implementation-orchestrator ←─────────────────→│
                          │                                  │
                          ▼                                  │
              ┌───────────────────────────────────────┐      │
              │         AGENT DAG EXECUTION           │      │
              │  database-architect → api-contract    │◄─────┘
              │  → domain-logic, frontend, devops     │
              │  → security-architect (gate)          │
              │  → test-strategy → impl-test-engineer │
              └───────────────────────────────────────┘
                          │
                          ▼
                    code-reviewer
                          │
                          ▼
                 acceptance-validator
```

## Skill Phase Reference

| Phase | Order | Skills | Type |
|-------|-------|--------|------|
| project-setup | 1 | claude-md-architect, hooks-setup, env-configurator | Auto-triggered |
| ideation | 2 | brainstorming | Mandatory |
| planning | 3 | writing-plans | Recommended |
| pre-implementation | 4 | preflight-check | Auto-triggered |
| agent-coordination | 5 | implementation-orchestrator | Workflow |
| pre-merge | 6 | code-reviewer | Mandatory |
| qa-validation | 7 | acceptance-validator | Gate |

## Version

**Last Updated:** 2026-01-17
**Version:** 1.0.0
