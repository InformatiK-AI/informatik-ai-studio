# InformatiK-AI Studio - GitHub Issues

> Generated: 2026-01-17
> Total Issues: 42
> Epics: 7 + Cross-Cutting

---

## Epic 1: Foundation Setup (6 Issues)

### Issue #1: Initialize Next.js 15 Project with TypeScript

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-1`, `foundation`, `setup`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want the project initialized with Next.js 15 and TypeScript strict mode, so that we have a solid foundation for building the application.

#### Description
Set up the Next.js 15 project with App Router, Server Components, and TypeScript in strict mode. This is the foundational issue that all other work depends on.

#### Technical Requirements
- Next.js 15.x with App Router
- TypeScript 5.x with `strict: true` in tsconfig.json
- pnpm as package manager
- ESLint + Prettier configuration
- Basic folder structure following conventions

#### Folder Structure
```
app/
├── layout.tsx          # Root layout with providers
├── page.tsx            # Landing page
├── (auth)/             # Auth route group
│   ├── login/page.tsx
│   └── signup/page.tsx
├── (dashboard)/        # Dashboard route group
│   └── dashboard/page.tsx
└── api/                # API routes
    └── health/route.ts

components/
├── ui/                 # shadcn/ui components
└── shared/             # Shared components

lib/
├── supabase/           # Supabase client
├── ai/                 # AI providers
└── utils.ts            # Utility functions

types/
└── index.ts            # TypeScript types
```

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Project starts in development mode
  Given all dependencies are installed with "pnpm install"
  When I run "pnpm dev"
  Then the server should start on port 3000
  And I should see "Ready" message in console
  And visiting http://localhost:3000 shows the landing page

@critical
Scenario: Production build succeeds
  When I run "pnpm build"
  Then the build should complete with exit code 0
  And no TypeScript errors should be present
  And no ESLint warnings should be present
```

#### Definition of Done
- [ ] Next.js 15 project created with `create-next-app`
- [ ] TypeScript strict mode enabled
- [ ] ESLint + Prettier configured
- [ ] Basic folder structure created
- [ ] `pnpm dev` runs without errors
- [ ] `pnpm build` succeeds
- [ ] Unit tests pass

---

### Issue #2: Configure Supabase Integration

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-1`, `foundation`, `supabase`, `database`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want Supabase configured for authentication and database, so that we can store user data and manage sessions.

#### Description
Set up Supabase client for both server and client-side usage. Configure environment variables and create the base database schema.

#### Technical Requirements
- @supabase/supabase-js and @supabase/ssr packages
- Server-side client (service role key)
- Client-side client (anon key)
- Environment variable validation
- TypeScript types generation from schema

#### Environment Variables
```bash
NEXT_PUBLIC_SUPABASE_URL=       # Public
NEXT_PUBLIC_SUPABASE_ANON_KEY=  # Public
SUPABASE_SERVICE_ROLE_KEY=      # Server only - NEVER expose
```

#### Files to Create
- `lib/supabase/client.ts` - Browser client
- `lib/supabase/server.ts` - Server client with cookies
- `lib/supabase/middleware.ts` - Session refresh middleware
- `lib/database.types.ts` - Generated types

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Supabase clients are properly configured
  Given environment variables are set
  When I import the Supabase client
  Then it should connect to the Supabase project
  And queries should execute successfully

@critical @security
Scenario: Service role key is not exposed
  When I inspect client-side bundle
  Then SUPABASE_SERVICE_ROLE_KEY should NOT be present
```

#### Definition of Done
- [ ] Supabase packages installed
- [ ] Browser client configured
- [ ] Server client configured with cookie handling
- [ ] Middleware for session refresh
- [ ] Types generated from schema
- [ ] Environment variable validation
- [ ] Unit tests for client initialization

---

### Issue #3: Set Up Tailwind CSS 4.0 and shadcn/ui

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-1`, `foundation`, `styling`, `ui`
**Estimated Complexity:** Low

#### User Story
As a developer, I want Tailwind CSS and shadcn/ui configured, so that we can build consistent, accessible UI components quickly.

#### Description
Configure Tailwind CSS 4.0 with the new CSS-first configuration and install core shadcn/ui components.

#### Technical Requirements
- Tailwind CSS 4.0 with new @theme directive
- CSS variables for theming
- Dark mode support (class strategy)
- shadcn/ui core components

#### shadcn/ui Components to Install
```bash
pnpm dlx shadcn@latest init
pnpm dlx shadcn@latest add button card input label form toast dialog dropdown-menu avatar skeleton
```

#### Theme Configuration
```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.7 0.15 250);
  --color-background: oklch(0.98 0 0);
  --color-foreground: oklch(0.1 0 0);
  /* ... more variables */
}

.dark {
  --color-background: oklch(0.1 0 0);
  --color-foreground: oklch(0.98 0 0);
}
```

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Tailwind styles are applied
  Given the application is running
  When I add a Tailwind class like "bg-primary"
  Then the style should be applied correctly
  And the color should match the theme variable

@standard
Scenario: Dark mode works
  When I toggle dark mode
  Then the theme should switch to dark colors
  And the preference should be persisted
```

#### Definition of Done
- [ ] Tailwind CSS 4.0 configured
- [ ] CSS variables for theming
- [ ] Dark mode toggle working
- [ ] shadcn/ui initialized
- [ ] Core components installed
- [ ] Components render correctly in light/dark mode

---

### Issue #4: Create App Shell Layout

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-1`, `foundation`, `layout`, `ui`
**Estimated Complexity:** Medium

#### User Story
As a user, I want a consistent app shell with navigation, so that I can easily navigate between different sections of the application.

#### Description
Create the main application layout with sidebar navigation, header, and content area. This layout will be used for authenticated pages.

#### Component Architecture
```
┌──────────────────────────────────────────────────────┐
│                    APP SHELL                          │
├──────────┬───────────────────────────────────────────┤
│ SIDEBAR  │         MAIN CONTENT                      │
│          │                                            │
│ - Logo   │  ┌────────────────────────────────────┐  │
│ - Nav    │  │ Header (breadcrumbs, user menu)    │  │
│ - Projects│ ├────────────────────────────────────┤  │
│ - Settings│ │                                    │  │
│          │  │         Page Content               │  │
│          │  │                                    │  │
│          │  └────────────────────────────────────┘  │
└──────────┴───────────────────────────────────────────┘
```

#### Files to Create
- `components/layout/app-shell.tsx`
- `components/layout/sidebar.tsx`
- `components/layout/header.tsx`
- `components/layout/nav-item.tsx`
- `app/(dashboard)/layout.tsx`

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: App shell renders correctly
  Given I am logged in
  When I navigate to /dashboard
  Then I should see the sidebar on the left
  And I should see the header at the top
  And the main content area should be visible

@standard
Scenario: Sidebar collapses on mobile
  Given I am on a mobile device (< 768px)
  When the page loads
  Then the sidebar should be collapsed
  And a hamburger menu should be visible
```

#### Definition of Done
- [ ] AppShell component created
- [ ] Sidebar with navigation
- [ ] Header with user menu
- [ ] Responsive design (mobile collapse)
- [ ] Dark mode support
- [ ] Component tests passing

---

### Issue #5: Implement Environment Variable Validation

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-1`, `foundation`, `security`, `config`
**Estimated Complexity:** Low

#### User Story
As a developer, I want environment variables validated at startup, so that the app fails fast with clear error messages if configuration is missing.

#### Description
Create a validation layer using Zod to ensure all required environment variables are present and correctly formatted before the application starts.

#### Technical Requirements
- Zod schema for environment validation
- Fail fast on missing required variables
- Type-safe environment access
- Clear error messages

#### Implementation
```typescript
// lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NEXT_PUBLIC_SUPABASE_URL: z.string().url(),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1),
  ANTHROPIC_API_KEY: z.string().startsWith('sk-ant-'),
  OPENAI_API_KEY: z.string().startsWith('sk-'),
});

export const env = envSchema.parse(process.env);
```

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: App fails with missing env vars
  Given NEXT_PUBLIC_SUPABASE_URL is not set
  When I run "pnpm dev"
  Then the app should fail immediately
  And I should see error "Missing required: NEXT_PUBLIC_SUPABASE_URL"

@critical @security
Scenario: Invalid API key format is rejected
  Given ANTHROPIC_API_KEY is "invalid-key"
  When I run "pnpm dev"
  Then the app should fail with validation error
```

#### Definition of Done
- [ ] Zod schema defined
- [ ] Validation runs on app start
- [ ] Clear error messages for missing vars
- [ ] Type-safe env access exported
- [ ] Unit tests for validation

---

### Issue #6: Configure ESLint, Prettier, and Husky

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-1`, `foundation`, `dx`, `tooling`
**Estimated Complexity:** Low

#### User Story
As a developer, I want automated code quality enforcement, so that the codebase maintains consistent standards.

#### Description
Set up ESLint with TypeScript rules, Prettier for formatting, and Husky with lint-staged for pre-commit hooks.

#### Configuration Files
- `.eslintrc.json` - ESLint config
- `.prettierrc` - Prettier config
- `.husky/pre-commit` - Pre-commit hook
- `lint-staged.config.js` - Lint-staged config

#### Rules
- Zero ESLint warnings policy
- Prettier formatting enforced
- TypeScript strict checks
- Import sorting

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Pre-commit hook runs linting
  Given I have unstaged changes with lint errors
  When I run "git commit"
  Then the commit should be blocked
  And I should see ESLint errors

@standard
Scenario: Code is auto-formatted on commit
  Given I have unformatted code
  When I run "git commit"
  Then Prettier should format the files
  And the formatted files should be committed
```

#### Definition of Done
- [ ] ESLint configured with TypeScript plugin
- [ ] Prettier configured
- [ ] Husky installed and configured
- [ ] lint-staged configured
- [ ] Pre-commit hook blocks on errors
- [ ] CI runs same checks

---

## Epic 2: Authentication (6 Issues)

### Issue #7: Implement Email/Password Registration

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-2`, `auth`, `supabase`
**Estimated Complexity:** Medium

#### User Story
As a new user, I want to register with my email and password, so that I can create an account and use the application.

#### Description
Create the registration flow using Supabase Auth with email verification. Include form validation, password strength requirements, and proper error handling.

#### Technical Requirements
- Supabase Auth signUp
- Password validation (8+ chars, uppercase, lowercase, number, special)
- Email verification required
- Form validation with Zod + React Hook Form
- Rate limiting awareness

#### UI Components
- `/signup` page
- Registration form with validation
- Password strength indicator
- Success/error feedback

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User registers successfully
  Given I am on the /signup page
  When I enter "newuser@example.com" as email
  And I enter "SecureP@ss123!" as password
  And I click "Sign Up"
  Then I should see "Check your email for verification"
  And a user should be created in Supabase

@error-handling
Scenario: Weak password is rejected
  When I enter "weak" as password
  And I click "Sign Up"
  Then I should see password requirements error
```

#### Definition of Done
- [ ] Signup page created
- [ ] Form validation implemented
- [ ] Supabase Auth integration
- [ ] Email verification flow
- [ ] Error handling for all cases
- [ ] Unit tests for validation
- [ ] E2E test for happy path

---

### Issue #8: Implement Email/Password Login

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-2`, `auth`, `supabase`
**Estimated Complexity:** Medium

#### User Story
As a registered user, I want to log in with my email and password, so that I can access my projects.

#### Description
Create the login flow with session management, secure cookie handling, and proper redirect after authentication.

#### Technical Requirements
- Supabase Auth signInWithPassword
- Session stored in secure HttpOnly cookie
- Return URL preservation
- Rate limiting (5 attempts, then 15 min lockout)

#### UI Components
- `/login` page
- Login form
- "Forgot Password" link
- OAuth buttons (GitHub, Google)

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User logs in successfully
  Given I have a verified account
  When I enter correct credentials
  And I click "Sign In"
  Then I should be redirected to /dashboard
  And a session cookie should be set

@security
Scenario: Session cookie is secure
  Given I am logged in
  When I inspect cookies
  Then the session cookie should have HttpOnly flag
  And it should have Secure flag
```

#### Definition of Done
- [ ] Login page created
- [ ] Supabase Auth integration
- [ ] Session cookie handling
- [ ] Return URL redirect
- [ ] Error handling
- [ ] Rate limiting UI feedback
- [ ] E2E test for login flow

---

### Issue #9: Implement OAuth Login (GitHub, Google)

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-2`, `auth`, `oauth`, `supabase`
**Estimated Complexity:** Medium

#### User Story
As a user, I want to log in with my GitHub or Google account, so that I can quickly access the application without creating a new password.

#### Description
Implement OAuth authentication with GitHub and Google using Supabase Auth. Handle the OAuth callback and user profile import.

#### Technical Requirements
- Supabase OAuth providers (GitHub, Google)
- OAuth callback handler at `/api/auth/callback`
- Profile picture import
- State parameter for CSRF protection

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User logs in with GitHub
  Given I am on the /login page
  When I click "Continue with GitHub"
  Then I should be redirected to GitHub authorization
  When I authorize the app
  Then I should be redirected back and logged in
  And my GitHub profile picture should be displayed

@security
Scenario: OAuth state prevents CSRF
  When I initiate OAuth flow
  Then the redirect URL should contain a state parameter
  And the state should be validated on callback
```

#### Definition of Done
- [ ] GitHub OAuth configured in Supabase
- [ ] Google OAuth configured in Supabase
- [ ] OAuth callback route implemented
- [ ] CSRF protection with state parameter
- [ ] Profile import (avatar, name)
- [ ] E2E test for OAuth flow

---

### Issue #10: Implement Protected Routes Middleware

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-2`, `auth`, `middleware`, `security`
**Estimated Complexity:** Medium

#### User Story
As the system, I want to protect routes that require authentication, so that only logged-in users can access sensitive pages.

#### Description
Create Next.js middleware to check authentication status and redirect unauthenticated users to the login page.

#### Technical Requirements
- Next.js middleware.ts
- Supabase session verification
- Public routes whitelist
- Return URL preservation

#### Route Protection Matrix
| Route Pattern | Protection |
|--------------|------------|
| `/` | Public |
| `/login`, `/signup` | Public (redirect if logged in) |
| `/dashboard/**` | Protected |
| `/projects/**` | Protected |
| `/api/auth/**` | Public |
| `/api/**` | Protected (session required) |

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Unauthenticated user is redirected
  Given I am not logged in
  When I navigate to /dashboard
  Then I should be redirected to /login?returnTo=/dashboard

@critical
Scenario: Authenticated user accesses protected route
  Given I am logged in
  When I navigate to /dashboard
  Then the page should load successfully
```

#### Definition of Done
- [ ] Middleware created
- [ ] Public routes whitelist
- [ ] Session verification
- [ ] Return URL handling
- [ ] Refresh session on request
- [ ] E2E tests for protection

---

### Issue #11: Implement User Logout

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-2`, `auth`, `supabase`
**Estimated Complexity:** Low

#### User Story
As a logged-in user, I want to log out, so that I can securely end my session.

#### Description
Implement logout functionality that clears the session from both server and client.

#### Technical Requirements
- Supabase Auth signOut
- Clear session cookie
- Redirect to login page
- Clear any client-side cached data

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: User logs out successfully
  Given I am logged in
  When I click "Log Out" in the user menu
  Then my session should be terminated
  And I should be redirected to /login
  And the session cookie should be cleared
```

#### Definition of Done
- [ ] Logout button in header
- [ ] signOut implementation
- [ ] Cookie cleared
- [ ] Redirect to login
- [ ] E2E test

---

### Issue #12: Create Database Schema with RLS Policies

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-2`, `database`, `security`, `supabase`
**Estimated Complexity:** High

#### User Story
As the system, I want Row Level Security policies on all tables, so that users can only access their own data.

#### Description
Create the complete database schema with projects, project_files, generations, and deployments tables. Implement RLS policies for user data isolation.

#### Schema
```sql
-- Projects table
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) NOT NULL,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  template VARCHAR(50) DEFAULT 'blank',
  settings JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policy
CREATE POLICY "Users can CRUD own projects" ON projects
  FOR ALL USING (auth.uid() = user_id);
```

#### Tables
1. `projects` - User projects
2. `project_files` - Virtual file system
3. `generations` - AI generation history
4. `deployments` - Deployment records

#### Acceptance Criteria (Gherkin)
```gherkin
@critical @security
Scenario: RLS isolates user data
  Given User A has a project
  When User B queries the projects table
  Then User B should NOT see User A's project

@critical
Scenario: User can CRUD their own projects
  Given I am logged in
  When I create/read/update/delete my project
  Then the operation should succeed
```

#### Definition of Done
- [ ] All tables created
- [ ] RLS policies on all tables
- [ ] Indexes for performance
- [ ] TypeScript types generated
- [ ] Migration files created
- [ ] Integration tests for RLS

---

## Epic 3: Project Management (5 Issues)

### Issue #13: Implement Project Creation

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-3`, `projects`, `crud`
**Estimated Complexity:** Medium

#### User Story
As a user, I want to create a new project, so that I can start building an application.

#### Description
Implement the project creation flow with a modal dialog for entering project details and initial file setup.

#### Technical Requirements
- Server Action for project creation
- Zod validation for project data
- Create default files on project creation
- Redirect to project editor after creation

#### Default Files
```typescript
const DEFAULT_FILES = [
  { path: 'index.html', content: '<!DOCTYPE html>...' },
  { path: 'src/App.tsx', content: 'export default function App()...' },
  { path: 'src/styles.css', content: '/* styles */' },
];
```

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User creates a new project
  Given I am on the dashboard
  When I click "New Project"
  And I enter "My App" as the name
  And I click "Create"
  Then a project should be created
  And I should be redirected to /projects/{id}
  And default files should exist
```

#### Definition of Done
- [ ] New Project dialog
- [ ] Server Action for creation
- [ ] Default files created
- [ ] Redirect to project
- [ ] Error handling
- [ ] Unit tests
- [ ] E2E test

---

### Issue #14: Implement Project Dashboard

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-3`, `projects`, `ui`, `dashboard`
**Estimated Complexity:** Medium

#### User Story
As a user, I want to see all my projects on a dashboard, so that I can quickly access and manage them.

#### Description
Create the project dashboard with a grid/list view of projects, search, and filtering.

#### UI Components
- Project card (thumbnail, name, last modified)
- Empty state for new users
- Search input
- Framework filter

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User sees their projects
  Given I have 3 projects
  When I navigate to /dashboard
  Then I should see all 3 projects
  And each should show name and last modified

@standard
Scenario: Empty state for new users
  Given I have no projects
  When I navigate to /dashboard
  Then I should see "No projects yet"
  And a "Create Project" button
```

#### Definition of Done
- [ ] Dashboard page
- [ ] Project card component
- [ ] Empty state
- [ ] Search functionality
- [ ] Loading skeleton
- [ ] E2E test

---

### Issue #15: Implement Project Update and Delete

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-3`, `projects`, `crud`
**Estimated Complexity:** Medium

#### User Story
As a user, I want to rename and delete my projects, so that I can keep my workspace organized.

#### Description
Implement project update (rename) and delete functionality with confirmation dialogs.

#### Technical Requirements
- Server Actions for update/delete
- Confirmation dialog for delete
- Cascade delete files and generations
- Optimistic UI updates

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User renames a project
  Given I have a project named "Old Name"
  When I click the project name
  And I change it to "New Name"
  And I press Enter
  Then the project should be renamed

@critical
Scenario: User deletes a project
  When I click delete on a project
  And I confirm the deletion
  Then the project should be removed
  And all associated files should be deleted
```

#### Definition of Done
- [ ] Rename functionality
- [ ] Delete with confirmation
- [ ] Cascade delete
- [ ] Error handling
- [ ] E2E tests

---

### Issue #16: Implement File System Operations

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-3`, `projects`, `files`, `crud`
**Estimated Complexity:** High

#### User Story
As a user, I want to create, read, update, and delete files in my project, so that I can organize my code.

#### Description
Implement the virtual file system using the project_files table with full CRUD operations.

#### API Endpoints
- `GET /api/projects/:id/files` - List files
- `POST /api/projects/:id/files` - Create file
- `PUT /api/projects/:id/files` - Update file
- `DELETE /api/projects/:id/files?path=...` - Delete file

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User creates a new file
  Given I am in a project
  When I right-click and select "New File"
  And I enter "Button.tsx"
  Then the file should be created
  And it should appear in the file tree

@security
Scenario: Path traversal is prevented
  When I try to create "../../../etc/passwd"
  Then I should see "Invalid file path" error
```

#### Definition of Done
- [ ] All CRUD endpoints
- [ ] Path validation
- [ ] Authorization checks
- [ ] Error handling
- [ ] Unit tests
- [ ] Integration tests

---

### Issue #17: Implement Real-time Project Updates

**Type:** Feature
**Priority:** P2 - Medium
**Labels:** `epic-3`, `projects`, `realtime`, `supabase`
**Estimated Complexity:** Medium

#### User Story
As a user, I want to see project changes in real-time, so that I can see updates without refreshing.

#### Description
Implement Supabase Realtime subscriptions for project and file updates.

#### Technical Requirements
- Supabase Realtime subscription
- Update dashboard on project changes
- Update file tree on file changes
- Clean up subscriptions on unmount

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Dashboard updates in real-time
  Given I have the dashboard open
  When I create a project in another tab
  Then the new project should appear automatically
  And no page refresh should be needed
```

#### Definition of Done
- [ ] Realtime subscription setup
- [ ] Dashboard auto-update
- [ ] File tree auto-update
- [ ] Subscription cleanup
- [ ] Connection error handling

---

## Epic 4: Chat Mode (6 Issues)

### Issue #18: Create Chat Interface Component

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-4`, `chat`, `ui`
**Estimated Complexity:** Medium

#### User Story
As a user, I want a chat interface to interact with AI, so that I can describe what I want to build in natural language.

#### Description
Create the chat interface component with message history, input area, and AI response display.

#### UI Components
- Chat container
- Message bubbles (user/AI)
- Input textarea with send button
- Loading indicator
- Code block renderer with syntax highlighting

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User sends a message
  Given I am in Chat Mode
  When I type a message and press Enter
  Then my message should appear in the chat
  And a loading indicator should show
  And the AI response should stream in

@standard
Scenario: Code blocks are syntax highlighted
  When AI responds with code
  Then code should be in a code block
  And syntax highlighting should be applied
```

#### Definition of Done
- [ ] Chat container component
- [ ] Message rendering
- [ ] Input with send
- [ ] Loading states
- [ ] Code block styling
- [ ] Component tests

---

### Issue #19: Implement Claude AI Integration

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-4`, `ai`, `claude`, `backend`
**Estimated Complexity:** High

#### User Story
As a user, I want to generate code using Claude AI, so that I can quickly build features.

#### Description
Implement the Anthropic Claude API integration with proper error handling, token management, and response streaming.

#### Technical Requirements
- Anthropic SDK integration
- Streaming API response
- Token counting and limits
- System prompt for code generation
- Rate limiting (20 requests/minute)

#### Files to Create
- `lib/ai/providers/anthropic.ts`
- `lib/ai/prompts/code-generation.ts`
- `lib/ai/tokens.ts`
- `app/api/generate/code/route.ts`

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Claude generates code
  Given I send a code generation request
  When the API processes the request
  Then Claude should generate TypeScript/React code
  And the response should stream back progressively

@security
Scenario: API key is never exposed
  When I inspect network requests
  Then ANTHROPIC_API_KEY should NOT be visible
  And requests should go through server route only
```

#### Definition of Done
- [ ] Anthropic provider implemented
- [ ] Streaming response handler
- [ ] System prompt defined
- [ ] Token counting
- [ ] Rate limiting
- [ ] Error handling
- [ ] Unit tests with mocks
- [ ] Integration test

---

### Issue #20: Implement Response Streaming

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-4`, `ai`, `streaming`
**Estimated Complexity:** High

#### User Story
As a user, I want to see AI responses as they're generated, so that I don't have to wait for the complete response.

#### Description
Implement Server-Sent Events (SSE) streaming for AI responses with proper error handling and cancellation.

#### Technical Requirements
- SSE endpoint at `/api/generate/stream`
- Client-side EventSource consumer
- AbortController for cancellation
- Progress indication

#### Implementation
```typescript
// Server: app/api/generate/stream/route.ts
export async function POST(req: Request) {
  const encoder = new TextEncoder();
  return new Response(
    new ReadableStream({
      async start(controller) {
        for await (const chunk of stream) {
          controller.enqueue(encoder.encode(`data: ${JSON.stringify(chunk)}\n\n`));
        }
        controller.close();
      }
    }),
    { headers: { 'Content-Type': 'text/event-stream' } }
  );
}
```

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Response streams progressively
  When AI starts responding
  Then text should appear token by token
  And UI should update in real-time

@standard
Scenario: User can cancel generation
  Given AI is generating a response
  When I click "Stop"
  Then generation should be cancelled
  And partial response should be preserved
```

#### Definition of Done
- [ ] SSE endpoint implemented
- [ ] Client-side consumer
- [ ] Cancel functionality
- [ ] Error handling
- [ ] Reconnection logic
- [ ] E2E test

---

### Issue #21: Implement "Apply to Project" Functionality

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-4`, `ai`, `files`
**Estimated Complexity:** Medium

#### User Story
As a user, I want to apply generated code to my project, so that I can use the AI output.

#### Description
Implement the "Apply to Project" button that parses AI-generated code and creates/updates files in the project.

#### Technical Requirements
- Parse code blocks from AI response
- Detect file paths from code block headers
- Create or update files in project_files
- Handle multiple files from single response

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User applies generated code
  Given AI has generated a React component
  When I click "Apply to Project"
  Then a new file should be created
  And the file should open in the editor
  And I should see success toast
```

#### Definition of Done
- [ ] Code block parser
- [ ] Apply button component
- [ ] File creation logic
- [ ] Multi-file support
- [ ] Error handling
- [ ] E2E test

---

### Issue #22: Implement Chat History Persistence

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-4`, `chat`, `database`
**Estimated Complexity:** Medium

#### User Story
As a user, I want my chat history saved, so that I can continue conversations when I return.

#### Description
Persist chat messages to the database and restore them when opening a project.

#### Technical Requirements
- Store messages in `generations` table
- Load history on project open
- Limit context window (last 10 messages)
- Clear history option

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Chat history is restored
  Given I had a conversation yesterday
  When I open the project today
  Then all previous messages should be visible

@standard
Scenario: User clears chat history
  When I click "Clear Chat"
  And I confirm
  Then all messages should be deleted
```

#### Definition of Done
- [ ] Messages stored in DB
- [ ] History loading on mount
- [ ] Context window limiting
- [ ] Clear history function
- [ ] Integration test

---

### Issue #23: Implement Model Fallback (GPT-4)

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-4`, `ai`, `openai`
**Estimated Complexity:** Medium

#### User Story
As a user, I want the system to fall back to GPT-4 if Claude is unavailable, so that I can always generate code.

#### Description
Implement automatic model fallback from Claude to GPT-4 when the primary provider fails.

#### Technical Requirements
- OpenAI provider implementation
- Model router with fallback logic
- User notification when using fallback
- Consistent prompt format across providers

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Fallback to GPT-4 on Claude error
  Given Claude API returns 503
  When I send a generation request
  Then the system should retry with GPT-4
  And I should see "Using GPT-4 (Claude unavailable)"
```

#### Definition of Done
- [ ] OpenAI provider implemented
- [ ] Model router with fallback
- [ ] Notification to user
- [ ] Unit tests
- [ ] Integration test

---

## Epic 5: Editor Mode (5 Issues)

### Issue #24: Integrate Monaco Editor

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-5`, `editor`, `monaco`
**Estimated Complexity:** High

#### User Story
As a developer, I want a VS Code-like code editor, so that I can write and edit code comfortably.

#### Description
Integrate Monaco Editor with TypeScript support, syntax highlighting, and IntelliSense.

#### Technical Requirements
- @monaco-editor/react package
- TypeScript language support
- Syntax highlighting for TS, TSX, JS, JSX, HTML, CSS, JSON
- Theme support (light/dark)
- Lazy loading for performance

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Monaco Editor loads file
  Given I click a file in the file tree
  When the editor loads
  Then I should see the file content
  And syntax highlighting should be active
  And line numbers should be visible

@standard
Scenario: IntelliSense works
  Given I am editing TypeScript
  When I type "React."
  Then I should see autocomplete suggestions
```

#### Definition of Done
- [ ] Monaco package installed
- [ ] Editor component created
- [ ] Language detection
- [ ] Theme support
- [ ] Lazy loading
- [ ] Component tests

---

### Issue #25: Implement File Tree Component

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-5`, `editor`, `ui`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want a file tree to navigate my project, so that I can easily find and open files.

#### Description
Create a file tree component that displays the project's file structure with expand/collapse and context menu.

#### UI Features
- Folder expand/collapse
- File icons by type
- Context menu (New, Rename, Delete)
- Drag and drop (future)

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: File tree displays project structure
  Given my project has folders and files
  When I view the file tree
  Then I should see all files organized in folders
  And clicking a file should open it in the editor

@standard
Scenario: Context menu works
  When I right-click a file
  Then I should see options: Rename, Delete
  When I right-click a folder
  Then I should also see: New File, New Folder
```

#### Definition of Done
- [ ] File tree component
- [ ] Folder expand/collapse
- [ ] File icons
- [ ] Context menu
- [ ] Click to open file
- [ ] Component tests

---

### Issue #26: Implement Multi-Tab Support

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-5`, `editor`, `ui`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want to open multiple files in tabs, so that I can work on several files at once.

#### Description
Implement a tab bar for the editor that shows open files with dirty indicators and close buttons.

#### Technical Requirements
- Tab bar component
- Track open files in state
- Dirty indicator for unsaved changes
- Close tab with unsaved warning
- Tab reordering (drag)

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Opening multiple files
  When I click "App.tsx" then "utils.ts"
  Then two tabs should appear
  And clicking a tab switches the editor content

@standard
Scenario: Unsaved indicator
  When I modify a file without saving
  Then the tab should show a dot indicator
  When I save
  Then the indicator should disappear
```

#### Definition of Done
- [ ] Tab bar component
- [ ] Open files tracking
- [ ] Dirty indicator
- [ ] Close confirmation
- [ ] Component tests

---

### Issue #27: Implement Auto-Save

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-5`, `editor`, `feature`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want my changes auto-saved, so that I don't lose work.

#### Description
Implement debounced auto-save that triggers after the user stops typing for a configurable period.

#### Technical Requirements
- Debounce saves (1000ms default)
- Queue saves to prevent conflicts
- Show "Saving..." / "Saved" indicator
- Handle save errors gracefully

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Auto-save triggers after typing
  Given I make changes in the editor
  When I stop typing for 2 seconds
  Then the file should auto-save
  And I should see "Auto-saved" briefly

@error-handling
Scenario: Save error is handled
  Given the network fails during save
  Then I should see "Save failed" error
  And my changes should be preserved locally
```

#### Definition of Done
- [ ] Debounced save hook
- [ ] Save queue management
- [ ] Status indicator
- [ ] Error handling
- [ ] Integration test

---

### Issue #28: Implement Editor Keyboard Shortcuts

**Type:** Feature
**Priority:** P2 - Medium
**Labels:** `epic-5`, `editor`, `dx`
**Estimated Complexity:** Low

#### User Story
As a developer, I want keyboard shortcuts for common actions, so that I can work efficiently.

#### Description
Implement standard editor keyboard shortcuts for save, find, format, etc.

#### Shortcuts
| Action | Windows/Linux | Mac |
|--------|--------------|-----|
| Save | Ctrl+S | Cmd+S |
| Find | Ctrl+F | Cmd+F |
| Replace | Ctrl+H | Cmd+H |
| Format | Shift+Alt+F | Shift+Opt+F |
| Go to Line | Ctrl+G | Cmd+G |

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Ctrl+S saves the file
  Given I have unsaved changes
  When I press Ctrl+S
  Then the file should save
  And I should see "Saved" indicator
```

#### Definition of Done
- [ ] Shortcut handlers
- [ ] Prevent default browser actions
- [ ] Visual feedback
- [ ] Documentation

---

## Epic 6: Preview System (5 Issues)

### Issue #29: Create Sandboxed Preview Frame

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-6`, `preview`, `security`
**Estimated Complexity:** High

#### User Story
As a user, I want to see a live preview of my code, so that I can see my changes in real-time.

#### Description
Create an isolated iframe preview that runs the user's code safely without affecting the parent application.

#### Security Requirements
- Sandbox attribute on iframe
- No access to parent localStorage/cookies
- CSP headers enforced
- Cross-origin isolation

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Preview renders user code
  Given I have HTML/CSS/JS in my project
  When I open the preview
  Then my code should render in the iframe
  And it should be interactive

@critical @security
Scenario: Preview is sandboxed
  When malicious code runs in preview
  Then it should NOT access parent window
  And it should NOT access session cookies
  And it should be fully isolated
```

#### Definition of Done
- [ ] Iframe with sandbox attributes
- [ ] Code injection into iframe
- [ ] Security isolation verified
- [ ] CSP headers
- [ ] Security test

---

### Issue #30: Implement Hot Reload for Preview

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-6`, `preview`, `dx`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want the preview to update when I save, so that I can see changes quickly.

#### Description
Implement hot module replacement (HMR) style updates where code changes reflect in the preview without full reload.

#### Technical Requirements
- Debounce preview updates (500ms)
- Preserve state where possible
- Full reload fallback
- Error overlay on failure

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Preview updates on save
  Given I modify CSS in the editor
  When I save
  Then the preview should update within 1 second
  And form inputs should be preserved (if applicable)
```

#### Definition of Done
- [ ] Debounced update trigger
- [ ] Iframe content update
- [ ] State preservation attempt
- [ ] Performance optimization

---

### Issue #31: Implement Console Integration

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-6`, `preview`, `debugging`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want to see console output from my preview, so that I can debug my code.

#### Description
Capture and display console.log, console.error, console.warn from the preview iframe in an integrated console panel.

#### Technical Requirements
- postMessage from iframe to parent
- Console panel component
- Log level styling (error=red, warn=yellow)
- Clear console button
- Timestamp display

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Console logs appear
  Given my code has console.log('Hello')
  When the preview runs
  Then I should see "Hello" in the console panel

@standard
Scenario: Errors are highlighted
  When my code throws an error
  Then the error should appear in red
  And the stack trace should be visible
```

#### Definition of Done
- [ ] Console capture in iframe
- [ ] postMessage to parent
- [ ] Console panel component
- [ ] Log level styling
- [ ] Clear functionality
- [ ] Component test

---

### Issue #32: Implement Error Overlay

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-6`, `preview`, `dx`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want to see errors clearly in the preview, so that I can fix them quickly.

#### Description
Display a visible error overlay in the preview when JavaScript/React errors occur.

#### Features
- Red overlay with error message
- Stack trace with file/line info
- Click to navigate to error in editor
- Dismiss button

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Error overlay shows on runtime error
  Given my code throws an uncaught error
  When the preview runs
  Then I should see a red error overlay
  And the error message should be visible
  And clicking the line number should jump to the error
```

#### Definition of Done
- [ ] Error boundary in preview
- [ ] Error overlay component
- [ ] Navigate to error line
- [ ] Dismiss functionality

---

### Issue #33: Implement Preview Resize and Layout

**Type:** Feature
**Priority:** P2 - Medium
**Labels:** `epic-6`, `preview`, `ui`
**Estimated Complexity:** Low

#### User Story
As a user, I want to resize the preview panel, so that I can adjust my workspace.

#### Description
Implement resizable panels for editor/preview split view with drag handle.

#### Features
- Draggable divider
- Minimum widths
- Collapse buttons
- Persist layout preference

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: User resizes preview
  When I drag the divider
  Then the preview and editor should resize
  And the layout should persist on reload
```

#### Definition of Done
- [ ] Resizable panel component
- [ ] Minimum widths
- [ ] Collapse buttons
- [ ] localStorage persistence

---

## Epic 7: Deployment (4 Issues)

### Issue #34: Implement Vercel OAuth Integration

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-7`, `deploy`, `oauth`, `security`
**Estimated Complexity:** High

#### User Story
As a user, I want to connect my Vercel account, so that I can deploy my projects.

#### Description
Implement OAuth flow with Vercel for account linking and deployment authorization.

#### Technical Requirements
- Vercel OAuth registration
- OAuth flow with PKCE
- Token storage (encrypted)
- Token refresh handling
- Disconnect functionality

#### Security
- Tokens encrypted at rest
- Tokens not exposed to client
- User-specific RLS policies

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User connects Vercel
  Given I have not connected Vercel
  When I click "Connect Vercel"
  Then I should be redirected to Vercel authorization
  When I authorize
  Then I should be redirected back with account linked

@critical @security
Scenario: Tokens are stored securely
  Given I have connected Vercel
  When I inspect the database
  Then the token should be encrypted
  And it should not be accessible via client
```

#### Definition of Done
- [ ] Vercel OAuth app registered
- [ ] OAuth flow implemented
- [ ] Token encryption
- [ ] Token refresh
- [ ] Disconnect option
- [ ] Security tests

---

### Issue #35: Implement Deploy to Vercel Flow

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `epic-7`, `deploy`, `vercel`
**Estimated Complexity:** High

#### User Story
As a user, I want to deploy my project to Vercel with one click, so that I can share my app.

#### Description
Implement the deployment flow that packages project files and deploys them via Vercel API.

#### Technical Requirements
- Vercel Deployment API integration
- Project packaging (files → upload)
- Environment variable configuration
- Deployment status polling
- Real-time log streaming

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: User deploys project
  Given I have a valid project
  When I click "Deploy to Vercel"
  And I configure options
  And I click "Start Deployment"
  Then a deployment should start
  And I should see progress updates
  When complete
  Then I should see the live URL

@error-handling
Scenario: Build fails
  Given my project has errors
  When I deploy
  Then I should see "Build Failed"
  And I should see the error logs
```

#### Definition of Done
- [ ] Vercel API integration
- [ ] File packaging
- [ ] Deployment trigger
- [ ] Status polling
- [ ] Log streaming
- [ ] Error handling
- [ ] E2E test

---

### Issue #36: Implement Deployment Status Tracking

**Type:** Feature
**Priority:** P1 - High
**Labels:** `epic-7`, `deploy`, `ui`
**Estimated Complexity:** Medium

#### User Story
As a user, I want to track my deployment progress, so that I know when it's ready.

#### Description
Create a deployment status UI that shows real-time progress and build logs.

#### UI Features
- Status indicators (Queued, Building, Ready, Failed)
- Build log streaming
- Deployment URL (when ready)
- Cancel deployment button

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: User sees deployment progress
  Given a deployment is in progress
  When I view the deployment panel
  Then I should see the current status
  And build logs should stream in real-time
  When it completes
  Then I should see the deployment URL
```

#### Definition of Done
- [ ] Status polling
- [ ] Status indicators
- [ ] Log display
- [ ] Cancel functionality
- [ ] URL display
- [ ] Component test

---

### Issue #37: Implement Deployment History

**Type:** Feature
**Priority:** P2 - Medium
**Labels:** `epic-7`, `deploy`, `ui`
**Estimated Complexity:** Low

#### User Story
As a user, I want to see my deployment history, so that I can track past deployments and rollback if needed.

#### Description
Display a list of past deployments with status, URL, and timestamp.

#### Features
- Deployment history list
- Status, URL, timestamp for each
- Click to view logs
- Future: rollback functionality

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: User views deployment history
  Given I have deployed 5 times
  When I view deployment history
  Then I should see all 5 deployments
  And each should show timestamp, status, URL
```

#### Definition of Done
- [ ] History query from DB
- [ ] History list component
- [ ] Status indicators
- [ ] Link to deployed URL

---

## Cross-Cutting Issues (5 Issues)

### Issue #38: Set Up CI/CD Pipeline

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `infrastructure`, `ci-cd`, `devops`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want automated testing and deployment, so that we catch issues early and deploy reliably.

#### Description
Set up GitHub Actions for CI (lint, type check, test) and CD (Vercel deploy on merge).

#### Workflow
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - run: pnpm install
      - run: pnpm lint
      - run: pnpm type-check
      - run: pnpm test --coverage
      - uses: codecov/codecov-action@v3
```

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: CI runs on PR
  Given I create a pull request
  Then GitHub Actions should run lint, type-check, tests
  And the PR should show status checks

@standard
Scenario: Failing tests block merge
  Given a test is failing
  Then the PR should not be mergeable
```

#### Definition of Done
- [ ] CI workflow for lint/test
- [ ] Coverage reporting
- [ ] Status checks required
- [ ] Vercel preview deploys

---

### Issue #39: Implement Rate Limiting

**Type:** Feature
**Priority:** P0 - Critical
**Labels:** `security`, `api`, `infrastructure`
**Estimated Complexity:** Medium

#### User Story
As the system, I want rate limiting on API endpoints, so that we prevent abuse.

#### Description
Implement rate limiting using Vercel Edge middleware and Upstash Redis.

#### Limits
| Endpoint | Limit |
|----------|-------|
| /api/generate | 20/minute |
| /api/deploy | 5/5 minutes |
| /api/auth/* | 10/minute |

#### Acceptance Criteria (Gherkin)
```gherkin
@critical
Scenario: Rate limit is enforced
  Given I have made 20 requests in 1 minute
  When I make another request
  Then I should receive 429 Too Many Requests
  And I should see retry-after header
```

#### Definition of Done
- [ ] Upstash Redis setup
- [ ] Edge middleware
- [ ] Per-user limiting
- [ ] Error responses
- [ ] Integration test

---

### Issue #40: Implement Error Tracking (Sentry)

**Type:** Feature
**Priority:** P1 - High
**Labels:** `infrastructure`, `monitoring`, `dx`
**Estimated Complexity:** Low

#### User Story
As a developer, I want to track errors in production, so that I can fix issues quickly.

#### Description
Integrate Sentry for error tracking and performance monitoring.

#### Technical Requirements
- @sentry/nextjs package
- Source map uploads
- User context in errors
- Performance tracing

#### Acceptance Criteria (Gherkin)
```gherkin
@standard
Scenario: Errors are reported to Sentry
  Given an unhandled error occurs in production
  Then the error should be sent to Sentry
  And it should include user context
  And it should include stack trace with source maps
```

#### Definition of Done
- [ ] Sentry package installed
- [ ] Configuration complete
- [ ] Source map uploads
- [ ] User context
- [ ] Test error reporting

---

### Issue #41: Create API Documentation

**Type:** Documentation
**Priority:** P2 - Medium
**Labels:** `documentation`, `api`
**Estimated Complexity:** Medium

#### User Story
As a developer, I want API documentation, so that I understand how to use the endpoints.

#### Description
Create OpenAPI/Swagger documentation for all API endpoints.

#### Endpoints to Document
- `/api/projects` - Project CRUD
- `/api/projects/:id/files` - File CRUD
- `/api/generate/code` - AI generation
- `/api/deploy/vercel` - Deployment

#### Definition of Done
- [ ] OpenAPI spec file
- [ ] All endpoints documented
- [ ] Request/response schemas
- [ ] Authentication documented
- [ ] Error codes documented

---

### Issue #42: Implement Usage Analytics

**Type:** Feature
**Priority:** P2 - Medium
**Labels:** `analytics`, `infrastructure`
**Estimated Complexity:** Low

#### User Story
As a product owner, I want to track usage metrics, so that I can understand how the product is used.

#### Description
Implement basic analytics for tracking key user actions and AI usage.

#### Metrics to Track
- User signups
- Projects created
- AI generations (count, tokens, duration)
- Deployments
- Page views

#### Technical Requirements
- Vercel Analytics (built-in)
- Custom events for AI usage
- Token usage aggregation

#### Definition of Done
- [ ] Vercel Analytics enabled
- [ ] Custom event tracking
- [ ] Token usage tracking
- [ ] Dashboard view

---

## Summary

| Epic | Issues | Priority |
|------|--------|----------|
| Epic 1: Foundation | 6 | P0 |
| Epic 2: Authentication | 6 | P0 |
| Epic 3: Project Management | 5 | P0 |
| Epic 4: Chat Mode | 6 | P0 |
| Epic 5: Editor Mode | 5 | P0 |
| Epic 6: Preview System | 5 | P1 |
| Epic 7: Deployment | 4 | P0 |
| Cross-Cutting | 5 | Mixed |
| **Total** | **42** | - |

### Implementation Order (Critical Path)

```
Phase 1: Foundation (Week 1-2)
├── #1 Next.js 15 Setup
├── #2 Supabase Integration
├── #3 Tailwind + shadcn
├── #4 App Shell
├── #5 Env Validation
└── #6 Tooling (ESLint, Prettier, Husky)

Phase 2: Auth (Week 2-3)
├── #7 Registration
├── #8 Login
├── #9 OAuth
├── #10 Protected Routes
├── #11 Logout
└── #12 Database Schema + RLS

Phase 3: Core Features (Week 3-5)
├── #13-17 Project Management
├── #18-23 Chat Mode + AI
└── #24-28 Editor Mode

Phase 4: Polish (Week 5-6)
├── #29-33 Preview System
├── #34-37 Deployment
└── #38-42 Cross-Cutting
```

---

**Ready for review and issue creation.**
