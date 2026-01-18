# Technology Stack Details - InformatiK-AI Studio

> Referenced from: CLAUDE.md [stack] section
> Load when: Making technology decisions, onboarding, architecture review

## Core Stack

### Framework: Next.js v15

**Why Chosen**:
- App Router with Server Components for optimal performance
- Built-in API routes and Server Actions
- Streaming support for AI responses
- Excellent Vercel deployment integration
- Large ecosystem and community support

**Key Features Used**:
- **Server Components**: Default for pages, reduces client JS
- **Server Actions**: Form handling, mutations
- **Route Handlers**: API endpoints for AI generation
- **Streaming**: Real-time AI response rendering
- **Middleware**: Auth checks, rate limiting

**Configuration** (`next.config.js`):
```javascript
/** @type {import('next').NextConfig} */
module.exports = {
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  images: {
    domains: ['avatars.githubusercontent.com'],
  },
};
```

**Important Caveats**:
- Server Components cannot use hooks or browser APIs
- Client Components must be explicitly marked with `'use client'`
- File-based routing requires specific naming conventions

---

### Database: Supabase (PostgreSQL)

**Why Chosen**:
- Managed PostgreSQL with excellent DX
- Built-in auth with multiple providers
- Real-time subscriptions for collaboration
- Row Level Security for multi-tenant isolation
- Storage for project assets

**Key Features Used**:
- **Auth**: Email/password, OAuth (GitHub, Google)
- **Database**: PostgreSQL with full SQL support
- **RLS**: Per-user data isolation
- **Storage**: Project files, generated assets
- **Realtime**: Live preview updates (future)

**Client Setup**:
```typescript
// lib/supabase/client.ts (browser)
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}

// lib/supabase/server.ts (server)
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createClient() {
  const cookieStore = cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    { cookies: { /* cookie handling */ } }
  );
}
```

---

### AI Providers: Anthropic Claude + OpenAI GPT

**Why Multi-Model**:
- Redundancy: Fallback if one provider is down
- Specialization: Different models for different tasks
- Cost optimization: Route to cheaper models when appropriate
- User preference: Let users choose their preferred model

**Provider Configuration**:
```typescript
// lib/ai/providers/index.ts
export type AIProvider = 'anthropic' | 'openai';
export type AIModel =
  | 'claude-3-5-sonnet-20241022'
  | 'claude-3-5-haiku-20241022'
  | 'gpt-4o'
  | 'gpt-4o-mini';

export const DEFAULT_MODEL = 'claude-3-5-sonnet-20241022';

export const MODEL_CONFIG: Record<AIModel, ModelConfig> = {
  'claude-3-5-sonnet-20241022': {
    provider: 'anthropic',
    maxTokens: 8192,
    contextWindow: 200000,
    costPer1kInput: 0.003,
    costPer1kOutput: 0.015,
  },
  // ... other models
};
```

---

### Editor: Monaco Editor

**Why Chosen**:
- Same editor engine as VS Code
- Excellent TypeScript/JavaScript support
- Syntax highlighting, IntelliSense, error markers
- Highly customizable

**Integration**:
```typescript
// Using @monaco-editor/react wrapper
import Editor from '@monaco-editor/react';

<Editor
  height="100%"
  defaultLanguage="typescript"
  theme={isDarkMode ? 'vs-dark' : 'light'}
  options={{
    minimap: { enabled: false },
    fontSize: 14,
    automaticLayout: true,
  }}
/>
```

---

### Styling: Tailwind CSS v4 + shadcn/ui

**Why Chosen**:
- Utility-first CSS for rapid development
- shadcn/ui provides accessible, customizable components
- Dark mode support built-in
- Excellent performance (CSS at build time)

**Theme Configuration**:
```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    /* ... semantic tokens */
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}
```

---

## Supporting Libraries

| Library | Version | Purpose | Notes |
|---------|---------|---------|-------|
| `@supabase/supabase-js` | ^2.45 | Supabase client | Auth, DB, Storage |
| `@supabase/ssr` | ^0.5 | SSR helpers | Server/browser clients |
| `anthropic` | ^0.30 | Claude API | AI generation |
| `openai` | ^4.60 | GPT API | AI fallback |
| `@monaco-editor/react` | ^4.6 | Code editor | Monaco wrapper |
| `zod` | ^3.23 | Validation | Schema validation |
| `lucide-react` | ^0.450 | Icons | Icon library |
| `framer-motion` | ^11 | Animations | UI animations |

## Development Tools

| Tool | Purpose | Configuration |
|------|---------|---------------|
| ESLint | Linting | `eslint.config.js` |
| Prettier | Formatting | `.prettierrc` |
| TypeScript | Type checking | `tsconfig.json` |
| Vitest | Unit testing | `vitest.config.ts` |
| Playwright | E2E testing | `playwright.config.ts` |

## Infrastructure

| Service | Provider | Purpose |
|---------|----------|---------|
| Hosting | Vercel | Next.js hosting, Edge functions |
| Database | Supabase | PostgreSQL, Auth, Storage |
| AI | Anthropic/OpenAI | Code generation |
| Analytics | Vercel Analytics | Usage tracking |
| Error Tracking | Sentry | Error monitoring |
