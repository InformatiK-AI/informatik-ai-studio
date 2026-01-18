# InformatiK-AI Studio

> Version: 1.0.0 | Status: Development | Architecture: Modular

## [project_metadata]

| Field | Value |
|-------|-------|
| Name | InformatiK-AI Studio |
| Description | Web app de generacion de software con IA, similar a Bolt.new/Lovable, usando la metodologia InformatiK-AI |
| Repository | [TBD] |
| Created | 2026-01-17 |
| Last Updated | 2026-01-17 |

### Objectives

1. Crear una plataforma web para generacion de aplicaciones completas usando IA
2. Implementar editor de codigo con preview en tiempo real y deploy integrado
3. Soportar multiples modelos de IA (Claude, GPT) para generacion de codigo
4. Aplicar la metodologia InformatiK-AI para desarrollo estructurado

---

## [stack]

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Vertical | B | - | Next.js + Supabase |
| Framework | Next.js | ^15.0 | App Router, Server Components |
| Language | TypeScript | ^5.0 | Strict mode |
| Database | Supabase (PostgreSQL) | Latest | Auth + DB + Storage + Realtime |
| Styling | Tailwind CSS | ^4.0 | + shadcn/ui components |
| AI SDK | Anthropic + OpenAI | Latest | Multi-modelo |
| Editor | Monaco Editor | Latest | VS Code experience |
| Testing | Vitest + Playwright | Latest | Unit + E2E |
| Deploy | Vercel | Latest | Serverless + Edge |

### Stack Rationale

Next.js 15 con App Router proporciona SSR/SSG, Server Actions y streaming para UX optima. Supabase maneja auth, database y storage con tiempo real. Monaco Editor ofrece experiencia tipo VS Code. Arquitectura multi-modelo permite flexibilidad con Claude y GPT.

---

## [core_team]

### Mandatory Agents

#### @security-architect
- **Invoke When**: Auth flows, API keys handling, data storage, deploy configs
- **Output**: `security_plan.md`

#### @acceptance-validator
- **Invoke When**: Before marking features complete
- **Output**: Validation report with Gherkin AC

### Specialist Agents (As Needed)

| Agent | Trigger | Responsibility |
|-------|---------|----------------|
| @database-architect | Schema changes | Supabase schema, RLS policies |
| @api-contract-designer | API endpoints | OpenAPI specs, tRPC routes |
| @domain-logic-architect | Business logic | AI orchestration, code generation |
| @frontend-architect | UI/Components | Editor, Preview, Dashboard |
| @devops-architect | Deploy/CI/CD | Vercel config, GitHub Actions |

---

## [quick_reference]

### Commands

```bash
pnpm dev          # Development server (localhost:3000)
pnpm build        # Production build
pnpm test         # Run unit tests (Vitest)
pnpm test:e2e     # Run E2E tests (Playwright)
pnpm lint         # ESLint + Prettier check
pnpm db:push      # Push Supabase migrations
pnpm db:generate  # Generate types from schema
```

### Key Files

| Purpose | Path |
|---------|------|
| App Entry | `app/layout.tsx` |
| API Routes | `app/api/` |
| Supabase Client | `lib/supabase/client.ts` |
| AI Providers | `lib/ai/providers/` |
| Editor Component | `components/editor/` |
| Environment | `.env.local` |

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Yes | Supabase project URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Yes | Supabase public key |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Supabase admin key (server only) |
| `ANTHROPIC_API_KEY` | Yes | Claude API key |
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `VERCEL_TOKEN` | No | For programmatic deploys |

---

## [workflow]

### Development Process

1. **Plan** → `/flow-plan "[task]"`
2. **Contract** → `/flow-issue-create "[task]"`
3. **Build** → `/flow-feature-build "[issue]"`
4. **Validate** → `/flow-qa-validate "[PR]"`
5. **Fix** (if needed) → `/flow-feedback-fix "[PR]"`

### Git Workflow

- **Branching**: `feature/{issue-number}-{short-description}`
- **Commits**: Conventional Commits format
- **PRs**: Require 1 approval + passing CI

---

## [modular_index]

### Auto-Loaded Rules (.claude/rules/)

| File | Purpose | Priority |
|------|---------|----------|
| `code-standards.md` | TypeScript/React conventions | High |
| `testing-policy.md` | Test requirements, NO EXCEPTIONS | High |
| `security-policy.md` | API keys, auth, data security | Critical |
| `git-workflow.md` | Git/commit practices | Medium |
| `agent-coordination.md` | Agent collaboration rules | Medium |

### Path-Specific Rules (.claude/rules/domain/)

| File | Paths | Purpose |
|------|-------|---------|
| `api-rules.md` | `app/api/**`, `lib/api/**` | API endpoint patterns |
| `ui-rules.md` | `components/**`, `app/**/page.tsx` | UI component rules |

### On-Demand Documentation (.claude/docs/)

| File | Load When | Content |
|------|-----------|---------|
| `architecture/tech-stack.md` | Stack decisions | Full stack details |
| `architecture/database-schema.md` | DB changes | Supabase schema, RLS |
| `architecture/api-contracts.md` | API work | OpenAPI specs |
| `patterns/ai-integration.md` | AI features | Multi-model patterns |
| `patterns/editor-preview.md` | Editor work | Monaco + Preview setup |
| `guides/deployment.md` | Deploy tasks | Vercel + Supabase deploy |

---

## [change_log]

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial modular architecture |
