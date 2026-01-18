---
description: Rules for API endpoints and server routes
paths:
  - "app/api/**"
  - "lib/api/**"
  - "**/*.route.ts"
---

# API Development Rules - InformatiK-AI Studio

## Endpoint Design

### URL Conventions

```
GET    /api/projects              # List user projects
GET    /api/projects/:id          # Get single project
POST   /api/projects              # Create project
PUT    /api/projects/:id          # Update project
DELETE /api/projects/:id          # Delete project

POST   /api/generate/code         # Generate code with AI
POST   /api/generate/fix          # Fix code with AI
POST   /api/generate/explain      # Explain code with AI

POST   /api/deploy/vercel         # Deploy to Vercel
POST   /api/deploy/netlify        # Deploy to Netlify
GET    /api/deploy/:id/status     # Check deploy status
```

### Route Handler Pattern

```typescript
// app/api/generate/code/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { generateCodeSchema } from '@/lib/validations';

export async function POST(req: NextRequest) {
  // 1. Auth check
  const supabase = createClient();
  const { data: { session } } = await supabase.auth.getSession();

  if (!session) {
    return NextResponse.json(
      { success: false, error: { code: 'UNAUTHORIZED', message: 'Login required' } },
      { status: 401 }
    );
  }

  // 2. Validate input
  const body = await req.json();
  const validated = generateCodeSchema.safeParse(body);

  if (!validated.success) {
    return NextResponse.json(
      { success: false, error: { code: 'VALIDATION_ERROR', details: validated.error.issues } },
      { status: 400 }
    );
  }

  // 3. Business logic
  try {
    const result = await generateCode(validated.data);
    return NextResponse.json({ success: true, data: result });
  } catch (error) {
    // 4. Error handling
    return NextResponse.json(
      { success: false, error: { code: 'GENERATION_ERROR', message: error.message } },
      { status: 500 }
    );
  }
}
```

## AI Generation Endpoints

### Rate Limiting

All `/api/generate/*` endpoints MUST implement:

```typescript
import { rateLimit } from '@/lib/rate-limit';

const limiter = rateLimit({
  interval: 60 * 1000, // 1 minute
  uniqueTokenPerInterval: 500,
});

export async function POST(req: NextRequest) {
  try {
    await limiter.check(req, 20); // 20 requests per minute
  } catch {
    return NextResponse.json(
      { success: false, error: { code: 'RATE_LIMITED' } },
      { status: 429 }
    );
  }
  // ... rest of handler
}
```

### Streaming Responses

For AI generation, use streaming:

```typescript
export async function POST(req: NextRequest) {
  // ... validation

  const stream = new TransformStream();
  const writer = stream.writable.getWriter();

  // Start generation in background
  generateCodeStream(validated.data, writer);

  return new Response(stream.readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

## Response Format

### Success Response

```json
{
  "success": true,
  "data": {
    "code": "function hello() {...}",
    "language": "typescript",
    "tokensUsed": 1500,
    "model": "claude-3-5-sonnet"
  },
  "meta": {
    "generationId": "gen_123",
    "duration": 2340
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "TOKEN_LIMIT_EXCEEDED",
    "message": "Request exceeds maximum token limit",
    "details": {
      "requested": 50000,
      "maximum": 30000
    }
  }
}
```

## Status Codes

| Code | Use When |
|------|----------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (validation) |
| 401 | Unauthorized (auth required) |
| 403 | Forbidden (no permission) |
| 404 | Not Found |
| 429 | Rate Limited |
| 500 | Internal Server Error |
| 503 | Service Unavailable (AI provider down) |

## Security

- All routes require Supabase session
- AI API keys accessed only server-side
- Log generation requests (user, prompt summary, tokens)
- Sanitize prompts before sending to AI
