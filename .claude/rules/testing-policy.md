# Testing Policy - InformatiK-AI Studio

## NO EXCEPTIONS Rule

**Every feature MUST have tests. NO EXCEPTIONS.**

- No PR merges without passing tests
- No "we'll add tests later" excuses
- Test-related CI failures block deployment
- AI-generated code MUST be tested before integration

## Test Types

| Type | Location | Coverage Target | Tool |
|------|----------|-----------------|------|
| Unit | `*.test.ts` / `__tests__/` | 80% | Vitest |
| Integration | `tests/integration/` | Critical paths | Vitest |
| E2E | `tests/e2e/` | Happy paths | Playwright |
| Component | `*.test.tsx` | All components | Vitest + Testing Library |

## Test Requirements by Feature Type

### API Endpoints

- [ ] Success case (200/201)
- [ ] Validation errors (400)
- [ ] Authentication (401)
- [ ] Authorization (403)
- [ ] Not found (404)
- [ ] Rate limiting (429)
- [ ] Server errors (500)

### UI Components

- [ ] Renders correctly
- [ ] Props variations
- [ ] User interactions
- [ ] Loading states
- [ ] Error states
- [ ] Accessibility (a11y)

### AI Generation Features

- [ ] Successful generation
- [ ] Model fallback (Claude -> GPT)
- [ ] Token limit handling
- [ ] Timeout handling
- [ ] Invalid prompt handling
- [ ] Streaming response handling

### Editor Features

- [ ] File operations (create, save, delete)
- [ ] Syntax highlighting
- [ ] Auto-complete
- [ ] Error markers
- [ ] Keyboard shortcuts

## Test Commands

```bash
pnpm test              # Run all unit tests
pnpm test:watch        # Watch mode
pnpm test:coverage     # With coverage report
pnpm test:e2e          # E2E tests (Playwright)
pnpm test:e2e:ui       # E2E with UI mode
```

## CI Integration

- Tests run on every PR
- Coverage report generated and uploaded
- Failing tests block merge
- Flaky tests must be fixed or quarantined within 24h

## Mocking Strategy

### What to Mock

- External AI APIs (Anthropic, OpenAI)
- Supabase client (use test instance)
- File system operations
- Time-dependent functions

### What NOT to Mock

- Business logic being tested
- Simple utility functions
- React component rendering

```typescript
// Mock AI provider
vi.mock('@/lib/ai/providers/anthropic', () => ({
  generateCode: vi.fn().mockResolvedValue({
    code: 'function hello() {}',
    tokens: 100
  })
}));
```
