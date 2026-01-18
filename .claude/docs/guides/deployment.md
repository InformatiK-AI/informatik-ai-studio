# Deployment Guide - InformatiK-AI Studio

> Load this document when setting up CI/CD, deploying to production, or configuring environments.

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Production Setup                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   GitHub ──push──> Vercel (Auto Deploy)                         │
│      │                   │                                       │
│      │              ┌────┴────┐                                  │
│      │              │ Preview │ (PR branches)                    │
│      │              │ Staging │ (develop branch)                 │
│      │              │  Prod   │ (main branch)                    │
│      │              └────┬────┘                                  │
│      │                   │                                       │
│      │                   ▼                                       │
│      │              Supabase                                     │
│      │         ┌────────┴────────┐                              │
│      │         │ Auth │ DB │ Storage                            │
│      │         └─────────────────┘                              │
│      │                                                          │
│      └──────> GitHub Actions (CI)                               │
│                   │                                              │
│              Tests + Lint + Type Check                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Vercel Configuration

### vercel.json

```json
{
  "framework": "nextjs",
  "buildCommand": "pnpm build",
  "installCommand": "pnpm install",
  "regions": ["iad1"],
  "functions": {
    "app/api/**/*.ts": {
      "maxDuration": 30
    },
    "app/api/generate/**/*.ts": {
      "maxDuration": 60
    }
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

### Environment Variables (Vercel Dashboard)

| Variable | Environment | Notes |
|----------|-------------|-------|
| `NEXT_PUBLIC_SUPABASE_URL` | All | Public |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | All | Public |
| `SUPABASE_SERVICE_ROLE_KEY` | All | **Secret** |
| `ANTHROPIC_API_KEY` | All | **Secret** |
| `OPENAI_API_KEY` | All | **Secret** |
| `NEXT_PUBLIC_APP_URL` | Per-env | Preview/Prod URLs differ |

**Setup via CLI:**
```bash
# Link project
vercel link

# Add secrets (interactive)
vercel env add ANTHROPIC_API_KEY production
vercel env add ANTHROPIC_API_KEY preview
vercel env add ANTHROPIC_API_KEY development
```

---

## Supabase Configuration

### Database Migrations

```bash
# Generate migration from schema changes
pnpm supabase db diff -f migration_name

# Apply migrations locally
pnpm supabase db push

# Deploy to production
pnpm supabase db push --linked
```

### RLS Policies (Example)

```sql
-- projects table: users can only access their own projects
CREATE POLICY "Users can view own projects"
ON projects FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can create projects"
ON projects FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own projects"
ON projects FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own projects"
ON projects FOR DELETE
USING (auth.uid() = user_id);
```

### Storage Buckets

```sql
-- Project files bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('project-files', 'project-files', false);

-- RLS for storage
CREATE POLICY "Users can access own project files"
ON storage.objects FOR ALL
USING (
  bucket_id = 'project-files' AND
  (storage.foldername(name))[1] = auth.uid()::text
);
```

---

## GitHub Actions CI/CD

### .github/workflows/ci.yml

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Type check
        run: pnpm tsc --noEmit

      - name: Lint
        run: pnpm lint

      - name: Unit tests
        run: pnpm test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  e2e:
    runs-on: ubuntu-latest
    needs: lint-and-test

    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Install Playwright
        run: pnpm exec playwright install --with-deps

      - name: Run E2E tests
        run: pnpm test:e2e
        env:
          NEXT_PUBLIC_SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          NEXT_PUBLIC_SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}

      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-report
          path: playwright-report/
```

---

## Environment Setup

### Development (.env.local)

```bash
# Supabase (local or dev project)
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-local-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-local-service-key

# AI Providers
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Staging

- Vercel Preview deployments
- Separate Supabase project (staging)
- Same API keys (or separate staging keys)

### Production

- Vercel Production deployment
- Production Supabase project
- Production API keys with higher rate limits

---

## Deployment Checklist

### Pre-Deploy

- [ ] All tests passing (unit + E2E)
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Environment variables configured in Vercel
- [ ] Supabase migrations applied
- [ ] RLS policies verified
- [ ] API rate limits configured

### Post-Deploy

- [ ] Verify homepage loads
- [ ] Test authentication flow
- [ ] Test code generation (AI endpoints)
- [ ] Check error tracking (if configured)
- [ ] Verify database connectivity
- [ ] Test one full user flow (create project, generate code, preview)

---

## Rollback Procedures

### Vercel Rollback

```bash
# List deployments
vercel ls

# Promote previous deployment
vercel promote <deployment-url>
```

### Database Rollback

```bash
# View migration history
pnpm supabase migration list

# Rollback last migration (manual SQL)
# Create a down migration and apply
```

### Emergency Procedures

1. **Site Down**: Check Vercel status, redeploy last working commit
2. **Database Issues**: Check Supabase dashboard, verify connection limits
3. **AI API Failure**: Check provider status, verify API keys, check rate limits
4. **Auth Broken**: Verify Supabase Auth settings, check JWT configuration

---

## Monitoring

### Recommended Tools

| Tool | Purpose |
|------|---------|
| Vercel Analytics | Core Web Vitals, traffic |
| Sentry | Error tracking |
| Supabase Dashboard | DB metrics, auth logs |
| Anthropic Console | AI usage, costs |

### Key Metrics

- **P95 Response Time**: < 500ms for pages, < 2s for AI generation
- **Error Rate**: < 0.1%
- **Uptime**: 99.9%
- **AI Token Usage**: Monitor daily to avoid surprise costs

---

## Cost Optimization

| Resource | Optimization |
|----------|--------------|
| Vercel | Use Edge functions where possible |
| Supabase | Connection pooling, proper indexes |
| Anthropic | Cache common prompts, use Haiku for simple tasks |
| OpenAI | Batch requests, use GPT-4o-mini for fallback |
