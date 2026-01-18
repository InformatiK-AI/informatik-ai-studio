# Security Policy - InformatiK-AI Studio

## CRITICAL: API Key Handling

### API Keys Storage

- **NEVER** store API keys in code or git
- **NEVER** expose keys to client-side code
- Use `NEXT_PUBLIC_` prefix ONLY for public values
- All AI API calls MUST go through server routes

```typescript
// WRONG - Exposes key to client
const anthropic = new Anthropic({ apiKey: process.env.NEXT_PUBLIC_API_KEY });

// CORRECT - Server-side only
// app/api/generate/route.ts
const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
```

### Environment Variables

| Variable | Client Safe | Storage Location |
|----------|-------------|------------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Yes | .env.local |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Yes | .env.local |
| `SUPABASE_SERVICE_ROLE_KEY` | **NO** | Vercel secrets |
| `ANTHROPIC_API_KEY` | **NO** | Vercel secrets |
| `OPENAI_API_KEY` | **NO** | Vercel secrets |

## OWASP Top 10 Prevention

### Injection Prevention

- Use Supabase client with parameterized queries
- Sanitize all user inputs before AI prompts
- Validate file names and paths

```typescript
// NEVER do this with user input
const prompt = `Generate code for: ${userInput}`;

// ALWAYS sanitize
const sanitized = sanitizePrompt(userInput);
const prompt = buildPrompt(sanitized);
```

### Authentication (Supabase Auth)

- Use Supabase Auth for all user management
- Implement Row Level Security (RLS) on all tables
- Session tokens managed by Supabase client
- Require email verification for sensitive operations

### Code Execution Security

- Generated code runs in isolated sandbox (iframe/WebContainer)
- NEVER execute generated code on server
- Validate code output before preview
- Rate limit generation requests

## Security Review Triggers

@security-architect MUST review:

- [ ] Authentication/authorization changes
- [ ] API key handling modifications
- [ ] New AI model integrations
- [ ] File upload/download features
- [ ] Deploy functionality
- [ ] Database schema with user data

## Forbidden Patterns

```typescript
// NEVER expose API keys
const apiKey = process.env.ANTHROPIC_API_KEY; // In client component

// NEVER execute user code on server
eval(userGeneratedCode);
exec(userCommand);

// NEVER trust AI output without validation
const code = await generateCode(prompt);
fs.writeFileSync(code.path, code.content); // Path traversal risk!
```

## Required Patterns

```typescript
// API calls through server routes
export async function POST(req: Request) {
  const session = await getSession();
  if (!session) return unauthorized();

  // Validate input
  const body = await req.json();
  const validated = schema.parse(body);

  // Make AI call server-side
  const result = await anthropic.messages.create({...});

  return NextResponse.json(result);
}
```

## Rate Limiting

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/generate` | 20 | 1 minute |
| `/api/deploy` | 5 | 5 minutes |
| `/api/auth/*` | 10 | 1 minute |

Implement using Vercel Edge middleware or Upstash Redis.
