# API Contracts - InformatiK-AI Studio

> Load this document when working on API endpoints, route handlers, or client-server integration.

## Base Configuration

- **Base URL**: `/api`
- **Auth**: Supabase session (JWT in cookie)
- **Content-Type**: `application/json`
- **Rate Limiting**: Via Vercel Edge middleware + Upstash Redis

---

## Projects API

### List Projects

```
GET /api/projects
```

**Response 200:**
```json
{
  "success": true,
  "data": [
    {
      "id": "proj_abc123",
      "name": "My App",
      "description": "A todo app",
      "framework": "nextjs",
      "createdAt": "2026-01-15T10:00:00Z",
      "updatedAt": "2026-01-16T14:30:00Z",
      "lastDeployedAt": null
    }
  ],
  "meta": {
    "total": 1,
    "page": 1,
    "limit": 20
  }
}
```

### Get Project

```
GET /api/projects/:id
```

**Response 200:**
```json
{
  "success": true,
  "data": {
    "id": "proj_abc123",
    "name": "My App",
    "description": "A todo app",
    "framework": "nextjs",
    "files": [
      { "path": "app/page.tsx", "type": "file" },
      { "path": "app/layout.tsx", "type": "file" },
      { "path": "components", "type": "directory" }
    ],
    "settings": {
      "aiModel": "claude-3-5-sonnet",
      "autoSave": true
    },
    "createdAt": "2026-01-15T10:00:00Z",
    "updatedAt": "2026-01-16T14:30:00Z"
  }
}
```

### Create Project

```
POST /api/projects
```

**Request:**
```json
{
  "name": "My App",
  "description": "A todo app",
  "framework": "nextjs",
  "template": "blank" | "starter" | "dashboard"
}
```

**Response 201:**
```json
{
  "success": true,
  "data": {
    "id": "proj_abc123",
    "name": "My App",
    ...
  }
}
```

### Update Project

```
PUT /api/projects/:id
```

**Request:**
```json
{
  "name": "Updated Name",
  "description": "New description"
}
```

### Delete Project

```
DELETE /api/projects/:id
```

**Response 204:** No content

---

## AI Generation API

### Generate Code

```
POST /api/generate/code
```

**Request:**
```json
{
  "projectId": "proj_abc123",
  "prompt": "Add a login form with email and password",
  "context": {
    "currentFile": "app/page.tsx",
    "selectedCode": null
  },
  "options": {
    "model": "claude-3-5-sonnet",
    "stream": true
  }
}
```

**Response (streaming):**
```
event: start
data: {"generationId": "gen_xyz789"}

event: chunk
data: {"content": "import { useState }"}

event: chunk
data: {"content": " from 'react';"}

event: done
data: {"tokensUsed": 1500, "duration": 2340}
```

**Rate Limit:** 20 requests/minute

### Fix Code

```
POST /api/generate/fix
```

**Request:**
```json
{
  "projectId": "proj_abc123",
  "code": "function broken() { ... }",
  "error": "TypeError: Cannot read property 'x' of undefined",
  "options": {
    "model": "claude-3-5-sonnet"
  }
}
```

### Explain Code

```
POST /api/generate/explain
```

**Request:**
```json
{
  "code": "const memoized = useMemo(() => ..., [deps])",
  "detail": "brief" | "detailed"
}
```

---

## File Operations API

### Get File Content

```
GET /api/projects/:id/files?path=app/page.tsx
```

**Response 200:**
```json
{
  "success": true,
  "data": {
    "path": "app/page.tsx",
    "content": "export default function Page() {...}",
    "language": "typescript",
    "size": 1024,
    "lastModified": "2026-01-16T14:30:00Z"
  }
}
```

### Save File

```
PUT /api/projects/:id/files
```

**Request:**
```json
{
  "path": "app/page.tsx",
  "content": "export default function Page() { return <div>Hello</div> }"
}
```

### Create File/Directory

```
POST /api/projects/:id/files
```

**Request:**
```json
{
  "path": "components/Button.tsx",
  "type": "file",
  "content": "export function Button() {...}"
}
```

### Delete File

```
DELETE /api/projects/:id/files?path=components/old.tsx
```

---

## Deploy API

### Deploy to Vercel

```
POST /api/deploy/vercel
```

**Request:**
```json
{
  "projectId": "proj_abc123",
  "options": {
    "production": false,
    "environment": {
      "NEXT_PUBLIC_API_URL": "https://api.example.com"
    }
  }
}
```

**Response 202:**
```json
{
  "success": true,
  "data": {
    "deployId": "dpl_abc123",
    "status": "building",
    "url": null
  }
}
```

### Check Deploy Status

```
GET /api/deploy/:deployId/status
```

**Response 200:**
```json
{
  "success": true,
  "data": {
    "deployId": "dpl_abc123",
    "status": "ready",
    "url": "https://my-app-abc123.vercel.app",
    "createdAt": "2026-01-16T15:00:00Z",
    "readyAt": "2026-01-16T15:02:30Z"
  }
}
```

**Status Values:** `queued` | `building` | `ready` | `error` | `canceled`

---

## Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid session |
| `FORBIDDEN` | 403 | No access to resource |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Invalid request body |
| `RATE_LIMITED` | 429 | Too many requests |
| `TOKEN_LIMIT_EXCEEDED` | 400 | Prompt too long |
| `GENERATION_ERROR` | 500 | AI generation failed |
| `DEPLOY_ERROR` | 500 | Deployment failed |
| `PROVIDER_UNAVAILABLE` | 503 | AI provider down |

---

## Validation Schemas (Zod)

```typescript
// lib/validations/project.ts
export const createProjectSchema = z.object({
  name: z.string().min(1).max(100),
  description: z.string().max(500).optional(),
  framework: z.enum(['nextjs', 'react', 'vue', 'svelte']),
  template: z.enum(['blank', 'starter', 'dashboard']).default('blank'),
});

// lib/validations/generate.ts
export const generateCodeSchema = z.object({
  projectId: z.string(),
  prompt: z.string().min(1).max(10000),
  context: z.object({
    currentFile: z.string().optional(),
    selectedCode: z.string().optional(),
  }).optional(),
  options: z.object({
    model: z.enum(['claude-3-5-sonnet', 'gpt-4o']).default('claude-3-5-sonnet'),
    stream: z.boolean().default(true),
  }).optional(),
});
```
