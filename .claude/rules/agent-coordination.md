# Agent Coordination - InformatiK-AI Studio

## Agent Invocation Protocol

### When to Invoke Specialists

| Condition | Agent | Priority |
|-----------|-------|----------|
| Database schema changes | @database-architect | Required |
| New API endpoints | @api-contract-designer | Required |
| AI integration work | @domain-logic-architect | Required |
| UI/Component work | @frontend-architect | Required |
| Security-sensitive changes | @security-architect | **MANDATORY** |
| Before feature completion | @acceptance-validator | **MANDATORY** |
| CI/CD or deploy changes | @devops-architect | Required |

### Invocation Order (DAG)

For full-stack features, invoke in this order:

```
1. @database-architect (if DB changes)
   |
2. @api-contract-designer (if API changes)
   |
3. @domain-logic-architect + @frontend-architect (parallel)
   |
4. @security-architect (MANDATORY gate)
   |
5. @implementation-test-engineer
   |
6. @acceptance-validator (MANDATORY gate)
```

## Project-Specific Agent Guidelines

### @database-architect

Focus areas for InformatiK-AI Studio:
- Supabase schema design
- RLS policies for multi-tenant data isolation
- Project storage structure
- AI generation history tables

### @api-contract-designer

Focus areas:
- `/api/generate/*` - AI generation endpoints
- `/api/projects/*` - Project CRUD
- `/api/deploy/*` - Deploy to Vercel/Netlify
- Rate limiting specifications

### @domain-logic-architect

Focus areas:
- AI provider orchestration (Claude/GPT fallback)
- Token management and optimization
- Code generation pipeline
- Prompt engineering patterns

### @frontend-architect

Focus areas:
- Monaco Editor integration
- Real-time preview system
- Project file explorer
- Dashboard and project management UI

### @security-architect

**MANDATORY** review triggers:
- Any API key handling
- Auth flow modifications
- Code execution in preview
- Deploy functionality
- User data storage

## Output Artifacts

Each agent produces specific output files:

| Agent | Output File | Location |
|-------|-------------|----------|
| @database-architect | `database.md` | `.claude/docs/{feature}/` |
| @api-contract-designer | `api_contract.md` | `.claude/docs/{feature}/` |
| @domain-logic-architect | `backend.md` | `.claude/docs/{feature}/` |
| @frontend-architect | `frontend.md` | `.claude/docs/{feature}/` |
| @security-architect | `security_plan.md` | `.claude/docs/{feature}/` |

## Cross-Agent Validation

The `implementation-orchestrator` validates coherence:

- Database <-> API contract (types, naming)
- API contract <-> Backend (endpoints, handlers)
- Backend <-> Frontend (API calls, state)
- All <-> Security (no key exposure, proper auth)

## Missing Agent Protocol

If a required agent is unavailable:

1. Invoke `@agent-librarian "scout: {agent-name}"`
2. Review and approve the draft
3. Continue with the recruited agent
