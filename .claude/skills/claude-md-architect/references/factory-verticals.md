# Factory Verticals - Standard Tech Stacks

This document defines the three standard "Factory Verticals" - proven, battle-tested technology stacks that should be prioritized for new projects unless there are specific reasons to deviate.

## Overview

Factory Verticals are pre-configured, opinionated tech stacks designed to:

- Accelerate project bootstrapping
- Ensure consistency across projects
- Leverage proven patterns and best practices
- Reduce decision fatigue and analysis paralysis
- Enable knowledge sharing across teams

**Default Behavior**: When creating a new project CLAUDE.md, always default to one of these verticals unless the user explicitly requests a different stack.

---

## Vertical A: Astro + React + Tailwind

**Best for**: Content-focused websites, marketing sites, documentation, blogs, landing pages, static/hybrid applications

### Tech Stack

- **Framework**: Astro (static site generator with partial hydration)
- **UI Library**: React (for interactive islands)
- **Styling**: Tailwind CSS (utility-first CSS)
- **Deployment**: Vercel, Netlify, or Cloudflare Pages

### Key Characteristics

- **Performance**: Excellent (ships zero JS by default, selective hydration)
- **SEO**: Excellent (static HTML, server-rendered)
- **Learning Curve**: Low (simple conventions)
- **Build Time**: Fast
- **Scalability**: High (static assets, CDN-friendly)

### When to Choose

- Content is mostly static with selective interactivity
- Performance and SEO are critical priorities
- Team prefers file-based routing
- Budget considerations (low hosting costs)
- Need for multi-framework support (can use React, Vue, Svelte together)

### When NOT to Choose

- Highly dynamic, real-time application
- Requires complex client-side state management
- Heavy focus on user authentication and personalization
- Real-time collaboration features

### Typical Project Structure

```
project/
├── src/
│   ├── pages/           # File-based routing
│   ├── components/      # Reusable components
│   ├── layouts/         # Page layouts
│   └── styles/          # Global styles
├── public/              # Static assets
├── astro.config.mjs     # Astro configuration
├── tailwind.config.cjs  # Tailwind configuration
└── package.json
```

### Essential Dependencies

```json
{
  "dependencies": {
    "astro": "^4.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@astrojs/react": "^3.0.0",
    "@astrojs/tailwind": "^5.0.0",
    "tailwindcss": "^3.0.0"
  }
}
```

### Core Commands

```bash
npm create astro@latest     # Initialize project
npm run dev                 # Development server
npm run build               # Production build
npm run preview             # Preview production build
```

### CLAUDE.md Considerations for Vertical A

**Typical CLAUDE.md Length:** 500-600 lines (Standard template)

**Essential Sections:**

- Project metadata (landing page, marketing site, docs)
- Tech stack (Astro + React + Tailwind)
- Directory structure (pages/, components/, layouts/)
- Environment variables (PUBLIC_SITE_URL, analytics keys)
- Commands (dev, build, preview)
- Code standards (Astro components + React islands)
- Testing (Vitest for components, Playwright for E2E)
- Deployment (Vercel/Netlify config)
- Performance requirements (Lighthouse 95+, Core Web Vitals)

**Usually Omit:**

- Database section (static/hybrid sites)
- Complex auth flows (unless using server-side auth)
- Real-time features

**Recommended Agents:**

- presentation-layer-architect (critical for UI/UX)
- ui-component-architect (React islands)
- performance-optimizer (static site optimization)
- seo-specialist (content-focused sites)

**Typical Length Breakdown:**

- Strategic: ~200 lines
- Technical: ~200 lines
- Global: ~150 lines
- Quick Reference: ~50 lines

**Modular Option for Vertical A:**

If choosing modular architecture:
- Core CLAUDE.md: 100-200 lines
- `.claude/rules/code-standards.md`: Astro + React conventions
- `.claude/rules/testing-policy.md`: Vitest + Playwright setup
- `.claude/rules/domain/ui-rules.md`: Component patterns (paths: `src/components/**`)

---

## Vertical B: Next.js + Supabase

**Best for**: Full-stack web applications, SaaS products, dashboards, authenticated apps, apps requiring databases

### Tech Stack

- **Framework**: Next.js (React framework with SSR/SSG)
- **Backend/Database**: Supabase (Postgres + Auth + Storage + Realtime)
- **Styling**: Tailwind CSS (typically) or styled-components
- **Deployment**: Vercel (Next.js) + Supabase Cloud

### Key Characteristics

- **Performance**: Good (server components, streaming)
- **Full-Stack**: Yes (API routes, server actions)
- **Authentication**: Built-in via Supabase
- **Database**: Postgres with real-time subscriptions
- **Learning Curve**: Medium (React + Next.js patterns + Supabase API)
- **Scalability**: High (edge functions, horizontal scaling)

### When to Choose

- Need user authentication and authorization
- Require a relational database
- Want real-time features (chat, notifications, live updates)
- Building a SaaS or B2B application
- Need file storage and CDN
- Want type-safe API with TypeScript

### When NOT to Choose

- Simple static site (overkill)
- No database requirements
- Team lacks React/TypeScript experience
- Requires specific database (MongoDB, etc.)

### Typical Project Structure

```
project/
├── app/                 # Next.js app directory
│   ├── (auth)/         # Route groups
│   ├── api/            # API routes
│   ├── dashboard/      # Protected pages
│   └── layout.tsx      # Root layout
├── components/          # React components
├── lib/
│   ├── supabase/       # Supabase client & utilities
│   └── utils/          # Helper functions
├── supabase/
│   ├── migrations/     # Database migrations
│   └── seed.sql        # Seed data
├── public/             # Static assets
├── next.config.js      # Next.js configuration
└── package.json
```

### Essential Dependencies

```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "@supabase/supabase-js": "^2.0.0",
    "@supabase/auth-helpers-nextjs": "^0.8.0",
    "tailwindcss": "^3.0.0"
  }
}
```

### Core Commands

```bash
npx create-next-app@latest  # Initialize project
npm run dev                 # Development server
npm run build               # Production build
npm start                   # Production server
supabase init               # Initialize Supabase
supabase start              # Local Supabase
supabase db push            # Push migrations
```

### Environment Variables

```env
NEXT_PUBLIC_SUPABASE_URL=your-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### CLAUDE.md Considerations for Vertical B

**Typical CLAUDE.md Length:** 700-900 lines (Comprehensive template)

**Essential Sections:**

- Project metadata (SaaS, dashboard, full-stack app)
- Tech stack (Next.js + Supabase + Tailwind)
- Directory structure (app/, components/, lib/supabase/)
- Environment variables (Supabase URLs, keys, feature flags)
- Commands (dev, build, start, db migrations)
- Code standards (Next.js App Router, Server Components, TypeScript)
- Testing (Jest/Vitest, Playwright, Supabase integration tests)
- Deployment (Vercel + Supabase Cloud)
- Security requirements (RLS policies, auth flows, API security)
- Database schema (migrations, seed data)

**Additional Sections Often Needed:**

- Authentication flows (Supabase Auth patterns)
- Real-time features (Supabase Realtime subscriptions)
- File storage (Supabase Storage patterns)
- API routes and server actions
- Row-Level Security (RLS) policies

**Recommended Agents:**

- domain-logic-architect (business logic planning)
- data-architect (database schema design)
- security-architect (auth, RLS, API security)
- api-architect (API routes, server actions)
- integration-specialist (Supabase integration)

**Typical Length Breakdown:**

- Strategic: ~250 lines
- Technical: ~350 lines
- Global: ~250 lines
- Quick Reference: ~50 lines

**Modularization Tips:**

- Extract database schema to `.claude/docs/architecture/database-schema.md`
- Extract RLS policies to `.claude/docs/patterns/rls-patterns.md`
- Extract auth flows to `.claude/docs/patterns/auth-flows.md`

**Modular Option for Vertical B (Recommended):**

Vertical B projects often exceed 700 lines - modular is recommended:
- Core CLAUDE.md: 150-250 lines
- `.claude/rules/code-standards.md`: Next.js + TypeScript conventions
- `.claude/rules/testing-policy.md`: Jest/Vitest + Playwright setup
- `.claude/rules/security-policy.md`: Auth, RLS, API security rules
- `.claude/rules/domain/api-rules.md`: API route patterns (paths: `app/api/**`)
- `.claude/rules/domain/ui-rules.md`: React component patterns (paths: `components/**`)
- `.claude/docs/architecture/database-schema.md`: Full Supabase schema
- `.claude/docs/architecture/api-contracts.md`: API specifications
- `.claude/docs/patterns/auth-flows.md`: Supabase Auth patterns

---

## Vertical C: Python + AI SDK

**Best for**: AI/ML applications, data processing, automation, backend APIs, LLM-powered tools

### Tech Stack

- **Language**: Python 3.11+
- **AI Framework**: Anthropic SDK, OpenAI SDK, or LangChain
- **Web Framework**: FastAPI (for APIs) or Streamlit (for dashboards)
- **Environment**: Poetry or venv for dependency management
- **Deployment**: Modal, Railway, or traditional cloud (AWS, GCP)

### Key Characteristics

- **AI-First**: Built for LLM integration and AI workflows
- **Performance**: Good (async support with FastAPI)
- **Ecosystem**: Rich (extensive AI/ML libraries)
- **Learning Curve**: Low to Medium (Python is accessible)
- **Type Safety**: Optional (type hints available)

### When to Choose

- Building AI-powered applications
- LLM integration is core to the product
- Need for data science/ML workflows
- Backend API for AI features
- RAG (Retrieval Augmented Generation) systems
- AI agents and autonomous systems

### When NOT to Choose

- Simple CRUD web application (use Vertical B)
- Static content site (use Vertical A)
- No AI/ML requirements
- Team lacks Python experience

### Typical Project Structure

```
project/
├── src/
│   ├── agents/          # AI agents and workflows
│   ├── api/             # FastAPI routes
│   ├── models/          # Data models
│   ├── prompts/         # LLM prompts and templates
│   └── utils/           # Helper functions
├── tests/               # Unit and integration tests
├── .env.example         # Example environment variables
├── pyproject.toml       # Poetry dependencies
├── main.py              # Application entry point
└── README.md
```

### Essential Dependencies (Poetry)

```toml
[tool.poetry.dependencies]
python = "^3.11"
anthropic = "^0.18.0"          # Anthropic Claude API
fastapi = "^0.109.0"           # Web framework
uvicorn = "^0.27.0"            # ASGI server
pydantic = "^2.6.0"            # Data validation
python-dotenv = "^1.0.0"       # Environment variables
httpx = "^0.26.0"              # Async HTTP client

[tool.poetry.dev-dependencies]
pytest = "^8.0.0"              # Testing
black = "^24.0.0"              # Code formatting
ruff = "^0.2.0"                # Linting
```

### Core Commands

```bash
poetry install              # Install dependencies
poetry run uvicorn main:app --reload   # Development server
poetry run pytest           # Run tests
poetry run black .          # Format code
poetry run ruff check .     # Lint code
```

### Environment Variables

```env
ANTHROPIC_API_KEY=your-api-key
OPENAI_API_KEY=your-api-key
DATABASE_URL=postgresql://...
LOG_LEVEL=INFO
```

### CLAUDE.md Considerations for Vertical C

**Typical CLAUDE.md Length:** 600-800 lines (Standard to Comprehensive template)

**Essential Sections:**

- Project metadata (AI app, automation, backend API)
- Tech stack (Python + Anthropic/OpenAI + FastAPI/Streamlit)
- Directory structure (src/agents/, src/prompts/, src/api/)
- Environment variables (API keys, database URLs, log levels)
- Commands (poetry install, run server, run tests, linting)
- Code standards (Python style guide, type hints, async patterns)
- Testing (pytest, coverage, integration tests)
- Deployment (Modal, Railway, Docker)
- AI/LLM patterns (prompt management, token optimization, error handling)

**Additional Sections Often Needed:**

- Prompt templates and management
- Token usage and cost optimization
- Rate limiting and retry strategies
- AI agent workflows
- RAG (Retrieval Augmented Generation) architecture
- Vector database integration (if applicable)

**Usually Omit:**

- Frontend-specific patterns (unless using Streamlit)
- Complex CSS/styling (unless using Streamlit)

**Recommended Agents:**

- ai-architect (LLM integration design)
- prompt-engineer (prompt template optimization)
- domain-logic-architect (business logic)
- api-architect (FastAPI routes)
- performance-optimizer (token efficiency, caching)

**Typical Length Breakdown:**

- Strategic: ~200 lines
- Technical: ~300 lines
- Global: ~200 lines
- Quick Reference: ~50 lines

**Modularization Tips:**

- Extract prompt templates to `src/prompts/` or `.claude/docs/patterns/prompts.md`
- Extract AI agent workflows to `.claude/docs/architecture/agent-workflows.md`
- Extract API patterns to `.claude/docs/patterns/api-patterns.md`
- Keep token optimization guide in `.claude/docs/guides/token-optimization.md`

**Modular Option for Vertical C:**

If project grows complex:
- Core CLAUDE.md: 120-200 lines
- `.claude/rules/code-standards.md`: Python style, type hints, async patterns
- `.claude/rules/testing-policy.md`: Pytest setup and coverage
- `.claude/rules/security-policy.md`: API key handling, rate limiting
- `.claude/rules/domain/api-rules.md`: FastAPI conventions (paths: `src/api/**`)
- `.claude/docs/patterns/prompts.md`: LLM prompt templates and best practices
- `.claude/docs/architecture/agent-workflows.md`: AI agent design patterns

### Common Patterns

**1. FastAPI + Anthropic Claude**

```python
from fastapi import FastAPI
from anthropic import Anthropic

app = FastAPI()
client = Anthropic()

@app.post("/chat")
async def chat(message: str):
    response = client.messages.create(
        model="claude-sonnet-4.5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": message}]
    )
    return {"response": response.content[0].text}
```

**2. Streamlit Dashboard**

```python
import streamlit as st
from anthropic import Anthropic

st.title("AI Assistant")
client = Anthropic()

if prompt := st.chat_input("Ask me anything"):
    response = client.messages.create(
        model="claude-sonnet-4.5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    st.write(response.content[0].text)
```

---

## Decision Matrix

Use this quick reference to choose the right vertical:

| Requirement         | Vertical A          | Vertical B        | Vertical C     |
| ------------------- | ------------------- | ----------------- | -------------- |
| Static content      | ✅ Best             | ❌ Overkill       | ❌ Wrong tool  |
| User authentication | ⚠️ Possible         | ✅ Best           | ⚠️ Possible    |
| Database            | ❌ Not built-in     | ✅ Best           | ✅ Good        |
| Real-time features  | ❌ Limited          | ✅ Best           | ⚠️ Possible    |
| AI/LLM integration  | ⚠️ Client-side only | ⚠️ Via API routes | ✅ Best        |
| SEO critical        | ✅ Excellent        | ✅ Good           | ❌ Not a focus |
| Fast build times    | ✅ Very fast        | ⚠️ Moderate       | ✅ Fast        |
| Low hosting cost    | ✅ Very low         | ⚠️ Moderate       | ⚠️ Varies      |
| Learning curve      | ✅ Low              | ⚠️ Medium         | ✅ Low-Medium  |

---

## Mixing Verticals

In some cases, combining verticals makes sense:

- **A + C**: Astro frontend with Python AI backend (marketing site + AI features)
- **B + C**: Next.js app with dedicated Python microservices for heavy AI workloads
- **A + B**: Astro for public site, Next.js for authenticated dashboard

When proposing mixed architectures, clearly justify why a single vertical is insufficient.

---

## CLAUDE.md Length Quick Reference

Use this table to estimate CLAUDE.md length when choosing a vertical:

| Vertical                  | Monolithic Length | Modular Core | Template               |
| ------------------------- | ----------------- | ------------ | ---------------------- |
| **A: Astro + React**      | 500-600 lines     | 100-200      | Standard / Modular     |
| **B: Next.js + Supabase** | 700-900 lines     | 150-250      | Comprehensive / Modular |
| **C: Python + AI SDK**    | 600-800 lines     | 120-200      | Standard / Modular     |

### Template Selection Guide

- **Minimal (300-400 lines)**: New projects, POCs, simple stacks
- **Standard (500-700 lines)**: Most production projects (Vertical A, C)
- **Comprehensive (800-1000 lines)**: Complex projects (Vertical B, enterprise)
- **Modular (100-300 lines)**: Scalable projects, team collaboration, large codebases

### Modular Architecture Option (NEW)

Each vertical can use either **monolithic** or **modular** architecture:

**Modular Architecture Benefits:**
- 73% reduction in initial context tokens
- Better maintainability for large projects
- Team-friendly: domain experts can own their rules
- Path-specific rules for different areas of codebase

**When to Choose Modular:**
- Project will exceed 700 lines in CLAUDE.md
- Multiple distinct domains (API, UI, data, etc.)
- Team wants separation of concerns
- Need domain-specific rules for different file paths

**Modular Structure by Vertical:**

| Vertical | Auto-Loaded Rules | Path-Specific | On-Demand Docs |
|----------|-------------------|---------------|----------------|
| **A** | code-standards, testing, git | ui-rules | - |
| **B** | code-standards, testing, security, git, agent-coord | api-rules, ui-rules | database-schema, api-contracts, auth-flows |
| **C** | code-standards, testing, security, git | api-rules | prompts, agent-workflows |

---

## Updating This Document

This document should be reviewed quarterly to:

- Add new proven patterns
- Update dependencies to latest stable versions
- Incorporate lessons learned from production projects
- Add emerging best practices
- Update CLAUDE.md length estimates based on real projects
- Refine modular architecture recommendations

Last updated: 2026-01-17

### Changelog

- **2026-01-17**: Added modular architecture option for all verticals
- **2026-01-11**: Initial version with three factory verticals
