# CLAUDE.md Best Practices - Examples

This reference file provides concrete examples of good vs. bad practices for CLAUDE.md files.

## Writing Style Examples

### ✅ GOOD - Clear, Imperative Language

```markdown
## [commands]

pnpm dev # Development server
pnpm build # Production build
pnpm test # Run test suite
```

**Why it works**: Direct, scannable, actionable

### ❌ BAD - Verbose with Explanations

```markdown
## [commands]

Run `pnpm dev` to start the development server on localhost:3000. This will enable hot reloading...
Run `pnpm build` to create an optimized production bundle...
```

**Why it fails**: Unnecessarily verbose, harder to scan, explains obvious behavior

---

## Content Organization Examples

### ✅ GOOD - Referenced Detail

```markdown
### Animation Standards

- Use Framer Motion for interactive animations
- Follow performance best practices (will-change, transform/opacity only)
- See [Animation Patterns](./.claude/docs/patterns/animations.md) for detailed examples
```

**Why it works**: Essential info in CLAUDE.md, details extracted for on-demand loading

### ❌ BAD - Inline 50-line Example

```markdown
### Animation Standards

Here's how to create a fade animation:
[50 lines of code example]
```

**Why it fails**: Bloats CLAUDE.md, consumes agent context unnecessarily

---

## Tech Stack Documentation

### ✅ GOOD - Stack with Rationale

```markdown
## [stack]

**Framework**: Next.js 14 (App Router)
**Database**: PostgreSQL via Supabase
**Authentication**: Supabase Auth (JWT-based)
**Styling**: Tailwind CSS 3.4+

**Rationale**:

- Next.js provides SSR + API routes in single framework
- Supabase handles auth, database, and real-time out of the box
- Tailwind enables rapid UI development with design system consistency
```

**Why it works**: Clear choices + justification helps agents understand architectural decisions

### ❌ BAD - Stack Without Context

```markdown
## [stack]

- React
- Node.js
- PostgreSQL
```

**Why it fails**: No context on why these choices, no guidance for agents

---

## Environment Variables

### ✅ GOOD - Documented Variables

```markdown
## [environment_variables]

**Required**:

- `DATABASE_URL` - PostgreSQL connection string (from Supabase dashboard)
- `NEXTAUTH_SECRET` - Random 32-char string for session encryption
- `STRIPE_SECRET_KEY` - Stripe API key for payments

**Optional**:

- `ANALYTICS_ID` - Google Analytics measurement ID
- `LOG_LEVEL` - Log verbosity (default: 'info', options: 'debug' | 'info' | 'warn' | 'error')
```

**Why it works**: Clear purpose, source hints, optionality marked

### ❌ BAD - Listed Without Context

```markdown
## [environment_variables]

- DATABASE_URL
- NEXTAUTH_SECRET
- STRIPE_SECRET_KEY
```

**Why it fails**: No guidance on what these are or where to get values

---

## Directory Structure

### ✅ GOOD - Key Paths Only

```markdown
## [directory_structure]

src/
├── app/ # Next.js app router pages
├── components/ # Reusable UI components
├── lib/ # Utilities and helpers
│ ├── db/ # Database client and queries
│ └── auth/ # Authentication utilities
└── types/ # TypeScript type definitions

**Key Files**:

- `src/app/api/` - API route handlers
- `src/lib/db/schema.ts` - Database schema definitions
- `src/middleware.ts` - Auth and request middleware
```

**Why it works**: Shows high-level organization + critical files, not exhaustive

### ❌ BAD - Exhaustive Listing

```markdown
## [directory_structure]

src/
├── app/
│ ├── page.tsx
│ ├── layout.tsx
│ ├── globals.css
│ ├── (auth)/
│ │ ├── login/
│ │ │ └── page.tsx
│ │ └── signup/
│ │ └── page.tsx
[...continues for 100+ lines]
```

**Why it fails**: Overwhelming, unmaintainable, obvious from file system

---

## Testing Requirements

### ✅ GOOD - Clear Policy

```markdown
## [testing_requirements]

**NO EXCEPTIONS POLICY**: All code must include appropriate tests before PR approval.

**Coverage Targets**:

- Unit tests: 80%+ for `src/lib/` utilities
- Integration tests: All API routes must have happy path + error cases
- E2E tests: Critical user flows (signup, checkout, dashboard)

**Required Tests**:

- New features: Unit + integration tests
- Bug fixes: Regression test demonstrating the fix
- Refactors: Existing test suite must pass

**Commands**:

- `pnpm test` - Run full test suite
- `pnpm test:watch` - Watch mode for development
- `pnpm test:coverage` - Generate coverage report
```

**Why it works**: Unambiguous expectations, specific targets, clear commands

### ❌ BAD - Vague Guidance

```markdown
## [testing]

Please write tests for your code when possible. Try to get good coverage.
```

**Why it fails**: Subjective, not enforceable, agents don't know what "good" means

---

## Agent Role Definitions

### ✅ GOOD - Specific Responsibilities

```markdown
## [core_team]

### @security-architect

**Role**: Security review and threat modeling
**Invoke when**:

- Implementing authentication or authorization
- Handling sensitive data (PII, payments, credentials)
- Adding new API endpoints that mutate data
- Before deploying changes to production
  **Responsibilities**:
- Review for OWASP Top 10 vulnerabilities
- Validate input sanitization and output encoding
- Check for injection risks (SQL, XSS, command)
- Verify secure credential storage and transmission
```

**Why it works**: Clear trigger conditions, specific checklist, actionable

### ❌ BAD - Generic Description

```markdown
## [core_team]

### @security-architect

Handles security stuff. Invoke when needed for security things.
```

**Why it fails**: Agents don't know when to invoke or what to check

---

## Workflow Documentation

### ✅ GOOD - Concrete Process

```markdown
## [workflow]

**Development Process**:

1. Create feature branch from `main`: `git checkout -b feature/your-feature`
2. Implement changes with tests
3. Run local validation: `pnpm lint && pnpm test && pnpm build`
4. Commit with conventional commits: `feat: add user profile page`
5. Push and create PR with description and test plan
6. Address review feedback
7. Squash merge to `main` after approval

**Branch Naming**:

- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code improvements
- `docs/` - Documentation only

**Commit Convention**:

- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code change without behavior change
- `test:` - Test additions or changes
- `docs:` - Documentation updates
```

**Why it works**: Step-by-step process, examples, naming standards

### ❌ BAD - High-Level Only

```markdown
## [workflow]

We use git for version control. Create branches for features, then make PRs.
```

**Why it fails**: No specific guidance, agents don't know the exact process

---

## Version Control for CLAUDE.md

### ✅ GOOD - Semantic Versioning

```yaml
# CLAUDE.md

Version: 1.2.0
Last Updated: 2026-01-11
Status: Production
```

**With Changelog**:

```markdown
## [change_log]

### Version 1.2.0 (2026-01-11)

- Added `animation-specialist` agent for advanced interactions
- Updated `[stack]` to include Framer Motion 12+
- Extracted animation patterns to `.claude/docs/patterns/animations.md`
- Rationale: Growing complexity of scroll-driven animations

### Version 1.1.0 (2025-12-15)

- Added `[testing_requirements]` with NO EXCEPTIONS policy
- Defined CI/CD pipeline in `[deployment]`
```

**Why it works**: Track evolution, understand why changes were made, reference history

### ❌ BAD - No Versioning

```markdown
# CLAUDE.md

[Content with no version info or change tracking]
```

**Why it fails**: Can't track when changes were made or why decisions were updated

---

## Common Mistakes Summary

### Length Management

❌ **Too Long**: 1200-line CLAUDE.md with 100-line code examples inline
✅ **Right Size**: 600-line CLAUDE.md with code examples in `.claude/examples/`

### Redundancy

❌ **Duplicated**: Same workflow commands in `[workflow]`, `[commands]`, and `[quick_reference]`
✅ **Single Source**: Workflow details in `[workflow]` section, referenced elsewhere

### Specificity

❌ **Too Generic**: "Use React for the frontend"
✅ **Specific**: "React 18+ with TypeScript 5.0, use functional components with hooks"

### Maintainability

❌ **Static**: No version, no changelog, outdated tech references
✅ **Evolving**: Versioned, changelog maintained, reviewed quarterly

---

## Quick Reference Example

### ✅ GOOD - Scannable Summary

```markdown
## Quick Reference

**Essential Commands**:

- `pnpm dev` - Start dev server
- `pnpm build` - Production build
- `pnpm test` - Run tests

**Key Paths**:

- `src/app/` - Pages and routing
- `src/lib/db/` - Database layer
- `.env.local` - Environment variables

**Critical Rules**:

- All code requires tests (NO EXCEPTIONS)
- Security-architect reviews all auth changes
- Conventional commits required

**Emergency Contacts**:

- Tech Lead: @username
- Security: security@company.com
```

**Why it works**: Agent can orient in <100 tokens, all essentials available

### ❌ BAD - Missing Quick Reference

```markdown
[No quick reference section, agent must scan entire file]
```

**Why it fails**: Wastes time and context finding basic information

---

## Template Selection Guide

### Use Minimal Template When:

- New project, early stage
- Simple tech stack (static site, single-page app)
- Small team (1-3 developers)
- Proof-of-concept or prototype

### Use Standard Template When:

- Production application
- Moderate complexity (full-stack, database, auth)
- Established team with defined processes
- Long-term maintenance expected

### Use Comprehensive Template When:

- Enterprise-scale project
- Complex architecture (microservices, multiple databases)
- Large team (5+ developers, multiple squads)
- Strict compliance or security requirements

---

## Final Checklist

Before approving a CLAUDE.md:

- [ ] Length: 500-700 lines (standard), not exceeding 1000
- [ ] Quick Reference section present
- [ ] All tech choices have rationale
- [ ] Agent roles clearly defined with trigger conditions
- [ ] Testing requirements specify coverage expectations
- [ ] No duplicate content across sections
- [ ] Code examples >20 lines extracted to separate files
- [ ] Version and changelog included
- [ ] Validates at 75+ quality score

---

For more detailed validation criteria, see [Validation Checklist](./validation-checklist.md).
