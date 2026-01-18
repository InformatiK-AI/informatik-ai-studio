# Brainstorming: InformatiK-AI Studio

> Generated: 2026-01-17
> Scope: PROJECT
> Status: Complete

## Requirements Summary

### Target Users
- **Primary**: Developers AND non-technical users
- **Approach**: Dual-mode interface (Chat Mode + Editor Mode)

### Core Features
- **AI Generation**: Claude-only for MVP (multi-model later)
- **Code Editor**: Monaco Editor with VS Code experience
- **Preview**: Real-time sandboxed preview
- **Deployment**: One-click Vercel deployment

### Scope Decisions
- **App Types**: Multi-platform (MVP: Web-only, mobile/desktop later)
- **Monetization**: None for now (build first)
- **Collaboration**: Single-user only for MVP
- **Templates**: Not in MVP (future enhancement)
- **Version History**: Not in MVP (future enhancement)

---

## Architecture Design

### User Flow (Happy Path)

```
1. User lands on homepage → Signs up/logs in (Supabase Auth)
2. Dashboard shows their projects (or "Create New" if empty)
3. User clicks "New Project" → Chooses template or starts blank
4. Prompt Interface: User describes what they want to build
5. AI generates initial code → Shows in Monaco Editor + Live Preview
6. User iterates: edits code directly OR gives AI more instructions
7. When satisfied → One-click deploy to Vercel
8. User gets live URL for their app
```

### Dual-Mode Interface

| Mode | For | Features |
|------|-----|----------|
| **Chat Mode** | Non-technical users | Natural language prompts, AI does everything |
| **Editor Mode** | Developers | Full Monaco editor, direct code editing, AI as assistant |

Users can switch between modes at any time.

### Component Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                        APP SHELL                              │
├────────────┬─────────────────────────────────────────────────┤
│  SIDEBAR   │              MAIN WORKSPACE                      │
│            │                                                  │
│  - Logo    │  ┌─────────────────────────────────────────────┐│
│  - Nav     │  │ CHAT MODE          OR    EDITOR MODE        ││
│  - Projects│  │                                             ││
│  - Settings│  │ ┌─────────────┐    │  ┌────────┬──────────┐││
│            │  │ │ Chat Panel  │    │  │Monaco  │ Preview  │││
│            │  │ │             │    │  │Editor  │ Frame    │││
│            │  │ │ + Preview   │    │  │        │          │││
│            │  │ │   below     │    │  │+ File  │+ Console │││
│            │  │ └─────────────┘    │  │ Tree   │          │││
│            │  │                    │  └────────┴──────────┘││
│            │  └─────────────────────────────────────────────┘│
└────────────┴─────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Complexity |
|-----------|---------|------------|
| **AuthProvider** | Supabase auth context | Low |
| **ProjectProvider** | Current project state | Medium |
| **ChatInterface** | Natural language prompts | Medium |
| **CodeEditor** | Monaco wrapper | High |
| **FileTree** | Project file navigation | Medium |
| **PreviewFrame** | Sandboxed iframe | Medium |
| **DeployButton** | One-click Vercel deploy | High |

---

## Data Model (Supabase)

### Core Tables

```sql
-- Users: Managed by Supabase Auth (auth.users)

-- Projects
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  template TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  deployed_url TEXT,
  vercel_project_id TEXT
);

-- Project Files (virtual file system)
CREATE TABLE project_files (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  path TEXT NOT NULL,
  content TEXT NOT NULL,
  language TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(project_id, path)
);

-- AI Generations (history/undo)
CREATE TABLE generations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  user_prompt TEXT NOT NULL,
  ai_response TEXT NOT NULL,
  model TEXT NOT NULL,
  tokens_input INT,
  tokens_output INT,
  duration_ms INT,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

### RLS Policies
All tables use Row Level Security ensuring users only access their own data.

---

## API Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/api/auth/callback` | GET | Supabase OAuth callback |
| `/api/projects` | GET/POST | List/create projects |
| `/api/projects/[id]` | GET/PATCH/DELETE | CRUD single project |
| `/api/projects/[id]/files` | GET/POST | List/create files |
| `/api/projects/[id]/files/[path]` | GET/PUT/DELETE | CRUD single file |
| `/api/generate` | POST | Non-streaming AI generation |
| `/api/generate/stream` | POST | Streaming AI generation |
| `/api/deploy` | POST | Deploy project to Vercel |

---

## Epic Breakdown (MVP)

### Epic 1: Foundation Setup
- Next.js 15 project initialization
- Supabase integration (auth + database)
- Tailwind CSS + shadcn/ui setup
- Basic app shell and routing

### Epic 2: Authentication
- Supabase Auth integration
- Login/signup pages
- OAuth (GitHub, Google)
- Protected routes middleware

### Epic 3: Project Management
- Projects CRUD (dashboard, create, delete)
- File system abstraction (project_files table)
- Project state management

### Epic 4: Chat Mode (Non-technical users)
- Chat interface component
- AI generation integration (Claude)
- Streaming response display
- Code-to-preview parsing

### Epic 5: Editor Mode (Developers)
- Monaco Editor integration
- File tree navigation
- Multi-tab support
- Auto-save functionality

### Epic 6: Preview System
- Sandboxed iframe preview
- Hot reload on code changes
- Console output capture
- Error overlay

### Epic 7: Vercel Deployment
- Vercel API integration
- One-click deploy flow
- Deploy status tracking
- Live URL display

---

## Implementation Order

```
Phase 1: Foundation (Epic 1 + Epic 2)
├── Next.js + Supabase setup
├── Auth (login/signup/OAuth)
└── App shell with protected routing

Phase 2: Core Features (Epic 3 + Epic 4)
├── Project management (CRUD, dashboard)
├── Chat Mode with AI generation
└── Basic preview (parse AI output → show result)

Phase 3: Developer Experience (Epic 5 + Epic 6)
├── Monaco Editor integration
├── File tree + multi-tab
├── Enhanced preview with hot reload
└── Console output

Phase 4: Deployment (Epic 7)
├── Vercel API integration
├── One-click deploy
└── Live URL display
```

### Critical Path
`Auth → Projects → AI Generation → Preview → Editor → Deploy`

---

## Future Enhancements (Post-MVP)

- Multi-model support (GPT, other providers)
- Template gallery
- Version history / snapshots
- Project sharing (view/edit links)
- Real-time collaboration
- Mobile app generation (React Native)
- Desktop app generation (Electron/Tauri)
- Usage analytics and monetization
