# Project Plan: InformatiK-AI Studio

> **Generated**: 2026-01-17
> **Scope**: PROJECT
> **Flow**: flow-plan v3.3.0
> **Status**: Complete

---

## Executive Summary

**InformatiK-AI Studio** is a web application for AI-powered software generation, similar to Bolt.new and Lovable. Users can generate complete web applications using natural language prompts, edit code directly, see real-time previews, and deploy with one click to Vercel.

### Key Decisions (from Brainstorming)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Target Users | Developers AND non-technical | Dual-mode interface covers both |
| UI Approach | Chat Mode + Editor Mode | Flexibility for all skill levels |
| AI Strategy | Claude-only for MVP | Simplify, add GPT later |
| Deployment | One-click Vercel | Best DX, simple integration |
| Collaboration | Single-user MVP | Complexity reduction |
| Monetization | None for now | Focus on product first |
| Code Editor | Monaco Editor | VS Code experience, best autocompletado |
| Preview Sandbox | iframe + Blob URL | Simple, rapido de implementar |
| Templates | 2-3 basicos | React starter, Landing page, Dashboard |

---

## Technology Stack

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Framework | Next.js (App Router) | 15.0+ | SSR, Server Actions, Streaming |
| Language | TypeScript (strict) | 5.0+ | Type safety |
| Database | Supabase (PostgreSQL) | Latest | Auth + DB + Storage + Realtime |
| Auth | Supabase Auth | Latest | Email/password + OAuth |
| Styling | Tailwind CSS + shadcn/ui | 4.0+ | Modern, consistent UI |
| AI | Anthropic Claude | Latest | Code generation |
| Code Editor | Monaco Editor | Latest | VS Code experience |
| Preview | Sandboxed iframe | - | Security isolation |
| Testing | Vitest + Playwright | Latest | Unit + E2E |
| Deployment | Vercel | Latest | Serverless + Edge |
| Rate Limiting | Upstash Redis | Latest | API protection |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         VERCEL EDGE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │   Next.js    │    │   API Routes │    │   Server     │       │
│  │   Frontend   │───▶│   /api/*     │───▶│   Actions    │       │
│  │              │    │              │    │              │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
│         │                   │                   │                │
│         ▼                   ▼                   ▼                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    SUPABASE                               │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │   Auth   │  │ Database │  │ Storage  │  │ Realtime │  │   │
│  │  │          │  │ (Postgres│  │  (Files) │  │          │  │   │
│  │  │  OAuth   │  │  + RLS)  │  │          │  │          │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────┐    ┌──────────────┐                           │
│  │   Claude AI  │    │ Vercel API   │                           │
│  │   (Server)   │    │  (Deploy)    │                           │
│  └──────────────┘    └──────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Epic Breakdown (MVP)

### Epic 1: Foundation Setup
**Priority**: Critical (Must be first)

**Features**:
- Next.js 15 project with App Router
- TypeScript configuration (strict mode)
- Tailwind CSS 4.0 + shadcn/ui setup
- ESLint + Prettier configuration
- Supabase project setup
- Environment variables configuration
- App shell (layout, sidebar, header)

**Key Files**:
- `package.json`, `tsconfig.json`, `next.config.js`
- `tailwind.config.ts`, `app/globals.css`
- `lib/supabase/client.ts`, `lib/supabase/server.ts`
- `app/layout.tsx`, `components/shell/`

**Estimated Complexity**: Medium

---

### Epic 2: Authentication
**Priority**: Critical (Blocking for all user features)

**Features**:
- Login page (email/password)
- Signup page with email verification
- OAuth providers (GitHub, Google)
- Protected routes middleware
- User session management
- Password reset flow

**Database**:
- Uses Supabase Auth (auth.users)
- No custom tables needed

**Key Files**:
- `app/(auth)/login/page.tsx`
- `app/(auth)/signup/page.tsx`
- `app/(auth)/reset-password/page.tsx`
- `app/api/auth/callback/route.ts`
- `middleware.ts`

**Estimated Complexity**: Medium

---

### Epic 3: Project Management
**Priority**: High

**Features**:
- Dashboard with project list/grid view
- Create new project wizard
- Project settings page
- Delete project (with confirmation)
- Project file system (virtual files in DB)
- Recent projects widget

**Database Tables**:
```sql
-- Projects
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  template VARCHAR(50) DEFAULT 'blank',
  settings JSONB DEFAULT '{}',
  deployed_url VARCHAR(500),
  vercel_project_id VARCHAR(100),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Project Files
CREATE TABLE project_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  path VARCHAR(500) NOT NULL,
  content TEXT NOT NULL,
  language VARCHAR(50),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(project_id, path)
);
```

**Key Files**:
- `app/(dashboard)/page.tsx`
- `app/(dashboard)/projects/new/page.tsx`
- `app/(dashboard)/projects/[id]/page.tsx`
- `app/api/projects/route.ts`
- `app/api/projects/[id]/route.ts`
- `app/api/projects/[id]/files/route.ts`

**Estimated Complexity**: Medium

---

### Epic 4: Chat Mode (AI Generation)
**Priority**: High (Core differentiator)

**Features**:
- Chat interface with message history
- AI generation with Claude (streaming)
- Code blocks with syntax highlighting
- "Apply" button to save generated files
- Quick action suggestions
- Generation history per project

**Database Tables**:
```sql
-- AI Generations
CREATE TABLE generations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  prompt TEXT NOT NULL,
  response TEXT,
  model VARCHAR(50) NOT NULL,
  tokens_input INT DEFAULT 0,
  tokens_output INT DEFAULT 0,
  duration_ms INT,
  status VARCHAR(20) DEFAULT 'completed',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Key Files**:
- `components/workspace/chat/chat-interface.tsx`
- `components/workspace/chat/chat-input.tsx`
- `components/workspace/chat/chat-message.tsx`
- `components/workspace/chat/code-block.tsx`
- `app/api/generate/stream/route.ts`
- `lib/ai/providers/anthropic.ts`
- `lib/ai/prompts/system-prompts.ts`

**Estimated Complexity**: High

---

### Epic 5: Editor Mode
**Priority**: High (Developer experience)

**Features**:
- Monaco Editor integration (dynamic import)
- File tree navigation (collapsible)
- Multi-tab support with dirty indicators
- Auto-save (debounced 1s)
- Keyboard shortcuts (Cmd+S, etc.)
- AI assistant sidebar panel
- Syntax highlighting for common languages

**Key Files**:
- `components/workspace/editor/code-editor.tsx`
- `components/workspace/editor/file-tree.tsx`
- `components/workspace/editor/editor-tabs.tsx`
- `components/workspace/editor/ai-sidebar.tsx`
- `hooks/use-auto-save.ts`
- `hooks/use-keyboard-shortcuts.ts`
- `stores/editor-store.ts` (Zustand)

**Estimated Complexity**: High

---

### Epic 6: Preview System
**Priority**: High

**Features**:
- Sandboxed iframe preview
- Hot reload on code changes (throttled 500ms)
- Console output capture
- Runtime error overlay
- Responsive viewport controls (desktop/tablet/mobile)
- Preview URL for sharing

**Key Files**:
- `components/workspace/preview/preview-frame.tsx`
- `components/workspace/preview/console-panel.tsx`
- `components/workspace/preview/device-selector.tsx`
- `components/workspace/preview/error-overlay.tsx`
- `lib/preview/sandbox.ts`
- `lib/preview/console-capture.ts`

**Estimated Complexity**: High

---

### Epic 7: Vercel Deployment
**Priority**: Medium (Nice-to-have for MVP, but key feature)

**Features**:
- Deploy dialog with configuration options
- Environment variables input
- Deployment progress indicator
- Live URL display on success
- Deployment history page
- Redeploy functionality

**Database Tables**:
```sql
-- Deployments
CREATE TABLE deployments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  provider VARCHAR(20) DEFAULT 'vercel',
  status VARCHAR(20) DEFAULT 'queued',
  url VARCHAR(500),
  error_message TEXT,
  env_vars JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Key Files**:
- `components/deploy/deploy-button.tsx`
- `components/deploy/deploy-dialog.tsx`
- `components/deploy/env-vars-form.tsx`
- `app/api/deploy/vercel/route.ts`
- `app/api/deploy/[deployId]/status/route.ts`
- `lib/deploy/vercel.ts`

**Estimated Complexity**: High

---

## Epic Priorities

| Priority | Epic | Dependency |
|----------|------|------------|
| 1 | Epic 1: Foundation | None |
| 2 | Epic 2: Authentication | Epic 1 |
| 3 | Epic 3: Project Management | Epic 2 |
| 4 | Epic 4: Chat Mode | Epic 3 |
| 5 | Epic 5: Editor Mode | Epic 3 |
| 6 | Epic 6: Preview System | Epic 4 or Epic 5 |
| 7 | Epic 7: Deployment | Epic 6 |

---

## Implementation Phases

### Phase 1: Foundation (Epic 1 + Epic 2)
**Duration**: First implementation cycle

1. Initialize Next.js 15 project with TypeScript
2. Configure Tailwind CSS 4.0 + shadcn/ui
3. Set up Supabase project (auth + database)
4. Implement auth pages (login, signup, OAuth)
5. Create protected routes middleware
6. Build app shell (sidebar, header)

### Phase 2: Core Features (Epic 3 + Epic 4)
**Duration**: Second implementation cycle

1. Apply database migrations (projects, project_files, generations)
2. Implement project CRUD API routes
3. Build dashboard and project list UI
4. Create chat interface components
5. Implement Claude streaming generation API
6. Connect chat to AI and basic preview

### Phase 3: Developer Experience (Epic 5 + Epic 6)
**Duration**: Third implementation cycle

1. Integrate Monaco Editor (dynamic import for bundle size)
2. Build file tree component
3. Implement multi-tab support
4. Add auto-save with debouncing
5. Create preview sandbox with hot reload
6. Add console output capture

### Phase 4: Deployment (Epic 7)
**Duration**: Fourth implementation cycle

1. Implement Vercel API integration
2. Build deploy dialog UI
3. Add deployment status polling
4. Create deployment history page
5. Add environment variables support

### Phase 5: Polish
**Duration**: Final cycle

1. Responsive design refinement
2. Performance optimization (code splitting, lazy loading)
3. Error handling improvements
4. Accessibility audit (WCAG 2.1 AA)
5. E2E tests with Playwright

---

## API Routes Summary

| Route | Method | Purpose | Rate Limit |
|-------|--------|---------|------------|
| `/api/auth/callback` | GET | OAuth callback | 10/min |
| `/api/projects` | GET, POST | List/create projects | 60/min |
| `/api/projects/[id]` | GET, PATCH, DELETE | Project CRUD | 60/min |
| `/api/projects/[id]/files` | GET, POST | List/create files | 120/min |
| `/api/projects/[id]/files/[path]` | GET, PUT, DELETE | File CRUD | 120/min |
| `/api/generate/stream` | POST | Streaming AI generation | 20/min |
| `/api/generate/fix` | POST | Fix code errors | 30/min |
| `/api/deploy/vercel` | POST | Deploy to Vercel | 5/5min |
| `/api/deploy/[id]/status` | GET | Deployment status | 60/min |

---

## Security Considerations

| Area | Approach | Agent Review |
|------|----------|--------------|
| API Keys | Server-side only, never exposed to client | @security-architect |
| User Input | Sanitize before AI prompts | @security-architect |
| RLS | All tables have row-level security | @database-architect |
| Preview | Sandboxed iframe, no server execution | @security-architect |
| Rate Limiting | Upstash Redis on all endpoints | @security-architect |
| File Paths | Validate to prevent traversal | @security-architect |
| Auth | Supabase Auth with session management | @security-architect |

---

## Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| AI generation costs | Medium | Token limits, rate limiting, usage tracking |
| Preview security | High | Strict sandboxing, no server-side execution |
| Vercel API changes | Low | Abstract behind service layer |
| Monaco bundle size | Medium | Dynamic import, code splitting |
| Supabase limits (free tier) | Medium | Monitor usage, plan for scaling |

---

## Dependencies to Install

```bash
# Core
pnpm add next@15 react@19 react-dom@19 typescript

# UI
pnpm add tailwindcss@4 @tailwindcss/postcss postcss
pnpm add class-variance-authority clsx tailwind-merge lucide-react

# Supabase
pnpm add @supabase/supabase-js @supabase/ssr

# AI
pnpm add @anthropic-ai/sdk

# Editor
pnpm add @monaco-editor/react

# State & Forms
pnpm add zustand @tanstack/react-query zod react-hook-form @hookform/resolvers

# Rate Limiting
pnpm add @upstash/ratelimit @upstash/redis

# Utilities
pnpm add use-debounce framer-motion next-themes nanoid
```

---

## Environment Variables

```env
# Supabase (Required)
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_ROLE_KEY=xxx

# AI (Required)
ANTHROPIC_API_KEY=sk-ant-xxx

# Deployment (Optional for MVP)
VERCEL_TOKEN=xxx

# Rate Limiting (Required for production)
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=xxx
```

---

## Agent Team (for Implementation)

| Agent | Responsibility | Phase |
|-------|----------------|-------|
| @database-architect | Supabase schema, RLS policies | Epic 3, 4, 7 |
| @api-contract-designer | API route design, OpenAPI | Epic 3, 4, 7 |
| @domain-logic-architect | AI orchestration, business logic | Epic 4, 7 |
| @frontend-architect | UI components, state management | All Epics |
| @devops-architect | Vercel config, CI/CD | Epic 7 |
| @security-architect | Security review (MANDATORY) | All Epics |
| @test-strategy-planner | Test planning | All Epics |
| @experience-analyzer | UX/DX analysis | Epic 4, 5, 6 |

---

## Verification Plan

### Manual Testing Checklist
- [ ] Auth Flow: Sign up, log in, OAuth, log out
- [ ] Project CRUD: Create, view, edit, delete project
- [ ] Chat Mode: Send prompt, receive streaming response, apply code
- [ ] Editor Mode: Open files, edit, save, switch tabs
- [ ] Preview: See code changes reflected in preview
- [ ] Deploy: Deploy project, check status, visit live URL

### Automated Testing
- **Unit Tests**: AI providers, token estimation, output parsing
- **Integration Tests**: API routes with mock Supabase
- **E2E Tests**: Full user flows with Playwright

---

## Documentation Generated

- `.claude/docs/informatik_ai_studio/brainstorming.md` - Design decisions
- `.claude/sessions/context_session_project_informatik_ai_studio.md` - This plan

---

*Plan generated by flow-plan v3.3.0*
*Status: READY FOR IMPLEMENTATION*
