# Code Standards - InformatiK-AI Studio

## Language & Formatting

- **Language**: TypeScript 5.x (strict mode enabled)
- **Formatter**: Prettier - Run before commit
- **Linter**: ESLint + typescript-eslint - Zero warnings policy

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | kebab-case | `code-editor.tsx` |
| Components | PascalCase | `CodeEditor` |
| Functions | camelCase | `generateCode` |
| Constants | SCREAMING_SNAKE | `MAX_TOKEN_LIMIT` |
| Types/Interfaces | PascalCase | `ProjectConfig` |
| Hooks | camelCase + use prefix | `useCodeGeneration` |

## Code Organization

### File Structure

```typescript
// 1. Imports (external -> internal -> types)
import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import type { Project } from '@/types';

// 2. Types (if not in separate file)
interface Props { ... }

// 3. Constants
const DEFAULT_MODEL = 'claude-3-5-sonnet';

// 4. Main component/function
export function Component() { ... }

// 5. Helper functions (if not extracted)
function formatCode() { ... }
```

### ABOUTME Headers

Every significant file MUST have an ABOUTME header:

```typescript
/**
 * ABOUTME: Editor principal con Monaco para edicion de codigo
 * RESPONSIBILITY: Renderizar editor, manejar cambios, syntax highlighting
 * DEPENDENCIES: Monaco Editor, Supabase (auto-save)
 */
```

## React/Next.js Patterns

### Server vs Client Components

```typescript
// Server Component (default) - app/projects/page.tsx
export default async function ProjectsPage() {
  const projects = await getProjects(); // Direct DB access
  return <ProjectList projects={projects} />;
}

// Client Component - components/editor/code-editor.tsx
'use client';
export function CodeEditor() {
  const [code, setCode] = useState('');
  // Client-side interactivity
}
```

### Server Actions

```typescript
// app/actions/project.ts
'use server';

export async function createProject(formData: FormData) {
  // Validate, save to DB, revalidate
}
```

## Error Handling

- Always use typed errors with `Result<T, E>` pattern
- Never swallow errors silently
- Log errors with context (project ID, user action)
- User-facing errors must be friendly and actionable

```typescript
// Use typed results
type Result<T, E = Error> = { ok: true; data: T } | { ok: false; error: E };

async function generateCode(): Promise<Result<string, GenerationError>> {
  // Implementation
}
```

## Async Patterns

- Prefer async/await over .then()
- Always handle rejected promises
- Use try/catch for async operations
- Set timeouts for AI API calls (30s default)
- Use AbortController for cancellable operations

## Comments

- Code should be self-documenting
- Comment "why", not "what"
- Remove commented-out code
- Update comments when code changes
- Document AI prompt engineering decisions
