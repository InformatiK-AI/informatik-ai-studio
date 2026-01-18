# CLAUDE.md Template (Comprehensive)

This template provides a **comprehensive** structure for creating future-proof CLAUDE.md files.

**Target Length:** 800-1000 lines (complex projects)
**Use When:** Enterprise projects, multi-team coordination, complex technical requirements

**Sections are labeled:**

- **[ESSENTIAL]** - Required for all projects
- **[RECOMMENDED]** - Include for most production projects
- **[OPTIONAL]** - Only if relevant to your project

**For simpler projects, use [claude-md-minimal.md](./claude-md-minimal.md) instead.**

Adapt sections based on project needs, but maintain the overall organization.

---

````markdown
# [Project Name]

> **Version**: 1.0.0
> **Last Updated**: YYYY-MM-DD
> **Status**: [Development | Production | Maintenance]

## [ESSENTIAL] Project Metadata

**Description**: [Concise 1-2 sentence description of what this project does]

**Objectives**:

- [Primary objective - what problem does this solve?]
- [Secondary objectives]
- [Success criteria]

**Repository**: [GitHub URL or other VCS]
**Documentation**: [Link to external docs if applicable]
**Production URL**: [If deployed]

---

## [ESSENTIAL] Technology Stack

**Architecture**: [Monolith | Microservices | Serverless | JAMstack]

**Core Technologies**:

- **Framework**: [e.g., Next.js 14, Astro 4, FastAPI 0.109]
- **Language**: [e.g., TypeScript 5.3, Python 3.11]
- **Database**: [e.g., PostgreSQL 15 via Supabase, None (static)]
- **Styling**: [e.g., Tailwind CSS 3.4]
- **Authentication**: [e.g., Supabase Auth, None, Auth0]

**Key Dependencies**:

```json
{
  "framework": "version",
  "library": "version"
}
```
````

**Rationale**: [Why this stack? What alternatives were considered?]

**Factory Vertical**: [A | B | C | Custom - reference factory-verticals.md]

---

## [ESSENTIAL] Core Team

Define specialized agents and their responsibilities. All agents must coordinate through this CLAUDE.md.

### Required Agents

#### @security-architect

- **Role**: Security analysis and vulnerability assessment
- **Responsibilities**:
  - Review code for security vulnerabilities
  - Validate authentication and authorization logic
  - Check for OWASP Top 10 vulnerabilities
  - Review environment variable handling
  - Assess API security
- **When to Invoke**: Before merging features that touch auth, data handling, or external APIs

#### @acceptance-validator

- **Role**: Quality assurance and acceptance testing
- **Responsibilities**:
  - Verify features meet requirements
  - Test user workflows end-to-end
  - Validate edge cases
  - Ensure documentation is updated
  - Confirm tests pass and coverage is adequate
- **When to Invoke**: Before marking features as complete

### Project-Specific Agents

#### @[agent-name]

- **Role**: [Brief description]
- **Responsibilities**:
  - [Specific task 1]
  - [Specific task 2]
- **When to Invoke**: [Conditions that warrant this agent's involvement]

---

## [ESSENTIAL] Directory Structure

```
project/
├── src/                    # Source code
│   ├── components/        # Reusable UI components
│   ├── pages/             # Route pages (or app/ for Next.js)
│   ├── lib/               # Utility functions and business logic
│   └── styles/            # Global styles
├── public/                # Static assets
├── tests/                 # Test files
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── .claude/              # Claude Code configuration
│   ├── CLAUDE.md         # This file
│   ├── agents/           # Agent definitions
│   ├── skills/           # Custom skills
│   └── commands/         # Custom commands
├── .env.example          # Example environment variables
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
└── README.md             # Public documentation
```

**Key Paths**:

- Configuration: `[path/to/config]`
- Business Logic: `[path/to/logic]`
- Database Schema: `[path/to/schema]`
- API Routes: `[path/to/api]`

---

## [ESSENTIAL] Environment Variables

### Required

```env
# API Keys
API_KEY_NAME=description-of-what-this-is
ANOTHER_API_KEY=description

# Database
DATABASE_URL=postgresql://localhost/dbname

# Authentication (if applicable)
AUTH_SECRET=random-secret-key
```

### Optional

```env
# Feature Flags
FEATURE_FLAG_NAME=true

# External Services
ANALYTICS_ID=optional-analytics-key
```

**Where to Set**:

- Local development: `.env.local` (not committed)
- Production: [Hosting platform dashboard, e.g., Vercel, Railway]

---

## [ESSENTIAL] Essential Commands

### Development

```bash
npm run dev              # Start development server (http://localhost:3000)
npm run build            # Build for production
npm run preview          # Preview production build locally
```

### Testing

```bash
npm test                 # Run all tests
npm run test:unit        # Run unit tests only
npm run test:integration # Run integration tests
npm run test:coverage    # Run tests with coverage report
```

### Code Quality

```bash
npm run lint             # Lint code
npm run format           # Format code
npm run type-check       # Check TypeScript types
```

### Database (if applicable)

```bash
npm run db:migrate       # Run database migrations
npm run db:seed          # Seed database with sample data
npm run db:reset         # Reset database (dev only)
```

### Deployment

```bash
npm run deploy           # Deploy to production
# OR: git push (if using continuous deployment)
```

---

## [ESSENTIAL] Development Workflow

### Git Workflow

**Branching Strategy**: [Git Flow | GitHub Flow | Trunk-based]

**Branch Naming**:

- `feature/description` - New features
- `fix/description` - Bug fixes
- `refactor/description` - Code refactoring
- `docs/description` - Documentation updates

**Commit Message Format**:

```
type(scope): brief description

Longer explanation if needed.

Refs: #issue-number
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Pull Request Process

1. Create feature branch from `main`
2. Implement changes with tests
3. Run `npm run lint && npm run type-check && npm test`
4. Push branch and create PR
5. Request review from `@security-architect` (if security-relevant)
6. Request validation from `@acceptance-validator`
7. Address feedback
8. Merge after approval (squash merge preferred)

### Pre-commit Checklist

Before committing code, ensure:

- [ ] All tests pass
- [ ] No linting errors
- [ ] TypeScript compiles without errors
- [ ] New features have tests (>80% coverage)
- [ ] No sensitive data (API keys, secrets) in code
- [ ] Updated relevant documentation

---

## [ESSENTIAL] Code Standards

### General Principles

- **DRY**: Don't Repeat Yourself - extract reusable logic
- **KISS**: Keep It Simple, Stupid - avoid over-engineering
- **YAGNI**: You Aren't Gonna Need It - don't add unused features
- **Separation of Concerns**: Each module should have a single responsibility

### TypeScript/JavaScript

- Use TypeScript for all new code
- Prefer `const` over `let`, avoid `var`
- Use async/await over promises.then()
- Destructure props for cleaner code
- Use optional chaining (`?.`) and nullish coalescing (`??`)

```typescript
// Good
const user = await fetchUser(id);
const name = user?.name ?? "Anonymous";

// Avoid
const user = await fetchUser(id).then((u) => u);
const name = user && user.name ? user.name : "Anonymous";
```

### React Components

- Use functional components with hooks
- Extract complex logic into custom hooks
- Keep components small (<200 lines)
- Use composition over prop drilling (Context or state management)

```typescript
// Good
export function UserProfile({ userId }: Props) {
  const { user, loading } = useUser(userId);

  if (loading) return <Spinner />;
  return <div>{user.name}</div>;
}
```

### File Naming

- Components: PascalCase (`UserProfile.tsx`)
- Utilities: camelCase (`formatDate.ts`)
- Constants: UPPER_SNAKE_CASE (`API_URL.ts`)
- Styles: kebab-case (`user-profile.css`)

### Comments

- Use comments to explain "why", not "what"
- Avoid obvious comments
- Use JSDoc for public APIs

```typescript
// Good
// Retry failed requests due to rate limiting (Issue #123)
const response = await retry(apiCall);

// Bad
// Call the API
const response = await apiCall();
```

---

## [ESSENTIAL] Testing Requirements

### Coverage Expectations

- **Minimum**: 80% overall coverage
- **Critical paths**: 100% coverage (auth, payments, data mutations)
- **Utilities**: 90%+ coverage

### Test Types

**Unit Tests**: Test individual functions/components in isolation

- Location: `tests/unit/` or co-located `*.test.ts`
- Run: `npm run test:unit`

**Integration Tests**: Test feature workflows end-to-end

- Location: `tests/integration/`
- Run: `npm run test:integration`

**E2E Tests** (if applicable): Test full user journeys

- Tool: [Playwright, Cypress, etc.]
- Location: `tests/e2e/`
- Run: `npm run test:e2e`

### What to Test

- ✅ Business logic and utilities
- ✅ Component behavior and user interactions
- ✅ API routes and database operations
- ✅ Error handling and edge cases
- ❌ Implementation details (internal state)
- ❌ Third-party libraries (assume they work)

---

## [RECOMMENDED] Deployment

### Environments

| Environment | URL              | Branch           | Auto-Deploy |
| ----------- | ---------------- | ---------------- | ----------- |
| Development | localhost:3000   | `*`              | No          |
| Preview     | [preview-url]    | feature branches | Yes (on PR) |
| Staging     | [staging-url]    | `develop`        | Yes         |
| Production  | [production-url] | `main`           | Yes         |

### Deployment Process

**Automated** (Continuous Deployment):

1. Push to `main` branch
2. CI/CD runs tests and builds
3. Deploys to production automatically
4. Monitor for errors

**Manual** (if required):

1. Run `npm run build` locally
2. Test production build with `npm run preview`
3. Run `npm run deploy`
4. Verify deployment successful

### Rollback Procedure

If deployment fails:

1. Revert the commit: `git revert HEAD`
2. Push to trigger redeployment
3. OR: Use hosting platform's rollback feature
4. Investigate and fix issue in separate branch

---

## [RECOMMENDED] Agent Coordination Guidelines

### Communication Patterns

**When to Delegate**:

- Task requires specialized expertise outside your role
- Task is in another agent's responsibility area
- You need a second opinion on critical decisions

**How to Delegate**:

```
@agent-name, please [specific request with context]
```

**When to Escalate**:

- Conflicting requirements or priorities
- Technical blocker requires architectural decision
- Timeline or scope concerns

**Escalate to**: @project-coordinator (the human stakeholder)

### Collaboration Rules

- **Read CLAUDE.md first**: Before starting work, review this file
- **Follow the stack**: Don't introduce new frameworks without approval
- **Test your changes**: Run the full test suite before requesting review
- **Document as you go**: Update relevant sections of CLAUDE.md
- **Ask for clarification**: Better to ask than assume

---

## [OPTIONAL] Project-Specific Context

### Business Logic Rules

[Document any critical business rules, calculations, or domain-specific knowledge that agents need to understand]

Example:

- Users can have multiple roles: admin, editor, viewer
- Admins can do everything; editors can create/edit; viewers read-only
- Content must be approved by admin before publishing

### External Integrations

[List and describe any external APIs, webhooks, or services]

Example:

- **Stripe**: Payment processing (API v2023-10-16)
  - Webhook endpoint: `/api/webhooks/stripe`
  - Events: `checkout.session.completed`, `invoice.paid`

### Known Issues / Technical Debt

[Track technical debt and known issues that need addressing]

Example:

- [ ] Refactor legacy authentication system (Issue #456)
- [ ] Optimize database queries for dashboard (Issue #789)
- [ ] Add caching layer for API responses

---

## [RECOMMENDED] Resources

### Documentation

- [Framework docs](https://link-to-docs)
- [API reference](https://link-to-api-docs)
- [Design system](https://link-to-design-system)

### Related Projects

- [Related project name](https://link) - Brief description

### Team Communication

- Slack: #project-channel
- Stand-ups: [Schedule]
- Project manager: [Name/Contact]

---

## Version History

### v1.0.0 (YYYY-MM-DD)

- Initial CLAUDE.md creation
- Defined core team and standards
- Established tech stack and workflow

---

**End of CLAUDE.md**

```

---

## Usage Notes

When using this template:

1. **Don't blindly copy**: Adapt each section to the specific project
2. **Remove irrelevant sections**: If no database, remove database commands
3. **Be specific**: Replace all `[placeholders]` with actual values
4. **Keep it updated**: CLAUDE.md should evolve with the project
5. **Get team buy-in**: Share with stakeholders for feedback before finalizing
6. **Watch the length**: Target 800-1000 lines max for this comprehensive template
7. **Consider minimal template**: For new/simple projects, use [claude-md-minimal.md](./claude-md-minimal.md) instead

### Section Length Estimates

To help manage overall length:

- **[ESSENTIAL] Project Metadata**: ~30-50 lines
- **[ESSENTIAL] Technology Stack**: ~50-80 lines
- **[ESSENTIAL] Core Team**: ~80-120 lines (depends on agent count)
- **[ESSENTIAL] Directory Structure**: ~50-80 lines
- **[ESSENTIAL] Environment Variables**: ~30-60 lines
- **[ESSENTIAL] Commands**: ~40-60 lines
- **[ESSENTIAL] Development Workflow**: ~80-120 lines
- **[ESSENTIAL] Code Standards**: ~100-150 lines
- **[ESSENTIAL] Testing Requirements**: ~80-120 lines
- **[RECOMMENDED] Deployment**: ~60-100 lines
- **[RECOMMENDED] Agent Coordination**: ~60-100 lines
- **[OPTIONAL] Project-Specific Context**: ~50-100 lines
- **[RECOMMENDED] Resources**: ~20-40 lines

**Total Estimated:** ~800-1000 lines (comprehensive)

### Modularization Thresholds

If any section exceeds these thresholds, extract to separate files:

- **Code Standards** > 150 lines → Extract patterns to `.claude/docs/patterns/`
- **Testing Requirements** > 120 lines → Extract strategies to `.claude/docs/patterns/testing-strategies.md`
- **Deployment** > 100 lines → Extract guide to `.claude/docs/guides/deployment-guide.md`
- **Project-Specific Context** > 150 lines → Split by domain to separate files

This template represents a comprehensive CLAUDE.md. Simpler projects may need fewer sections, while complex projects may need additional sections for microservices, infrastructure, or specialized workflows.
```
