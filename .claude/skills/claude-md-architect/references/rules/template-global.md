# Template: Global Rules File

This template is for files in `.claude/rules/` that are automatically loaded for ALL tasks.

**Characteristics**:
- Auto-loaded by Claude Code
- Applied to every task regardless of file paths
- Should be concise and actionable (50-150 lines)
- No YAML frontmatter required

---

## Template: code-standards.md

```markdown
# Code Standards

## Language & Formatting

- **Language**: [TypeScript/JavaScript/Python/etc.]
- **Formatter**: [Prettier/Black/etc.] - Run before commit
- **Linter**: [ESLint/Ruff/etc.] - Zero warnings policy

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Files | kebab-case | `user-profile.tsx` |
| Components | PascalCase | `UserProfile` |
| Functions | camelCase | `getUserProfile` |
| Constants | SCREAMING_SNAKE | `MAX_RETRY_COUNT` |
| Interfaces | PascalCase + I prefix | `IUserProfile` (optional) |

## Code Organization

### File Structure

```
// 1. Imports (external → internal → types)
import { useState } from 'react';
import { Button } from '@/components/ui';
import type { User } from '@/types';

// 2. Types/Interfaces (if not in separate file)
interface Props { ... }

// 3. Constants
const MAX_ITEMS = 10;

// 4. Main component/function
export function Component() { ... }

// 5. Helper functions (if not extracted)
function helper() { ... }
```

### ABOUTME Headers

Every significant file MUST have an ABOUTME header:

```typescript
/**
 * ABOUTME: [One-line description of what this file does]
 * RESPONSIBILITY: [Primary responsibility]
 * DEPENDENCIES: [Key dependencies]
 */
```

## Error Handling

- Always use typed errors
- Never swallow errors silently
- Log errors with context
- User-facing errors must be friendly

## Async Patterns

- Prefer async/await over .then()
- Always handle rejected promises
- Use try/catch for async operations
- Set timeouts for external calls

## Comments

- Code should be self-documenting
- Comment "why", not "what"
- Remove commented-out code
- Update comments when code changes
```

---

## Template: testing-policy.md

```markdown
# Testing Policy

## NO EXCEPTIONS Rule

**Every feature MUST have tests. NO EXCEPTIONS.**

- No PR merges without passing tests
- No "we'll add tests later" excuses
- Test-related CI failures block deployment

## Test Types

| Type | Location | Coverage Target |
|------|----------|-----------------|
| Unit | `tests/unit/` or `*.test.ts` | 80% |
| Integration | `tests/integration/` | Critical paths |
| E2E | `tests/e2e/` or `e2e/` | Happy paths |

## Test Requirements by Feature Type

### API Endpoints
- [ ] Success case (200/201)
- [ ] Validation errors (400)
- [ ] Authentication (401)
- [ ] Authorization (403)
- [ ] Not found (404)
- [ ] Server errors (500)

### UI Components
- [ ] Renders correctly
- [ ] Props variations
- [ ] User interactions
- [ ] Accessibility (a11y)
- [ ] Loading states
- [ ] Error states

### Business Logic
- [ ] Happy path
- [ ] Edge cases
- [ ] Error conditions
- [ ] Boundary values

## Test Commands

```bash
[package_manager] test              # Run all tests
[package_manager] test:watch        # Watch mode
[package_manager] test:coverage     # With coverage
[package_manager] test:e2e          # E2E tests
```

## CI Integration

- Tests run on every PR
- Coverage report generated
- Failing tests block merge
- Flaky tests must be fixed or quarantined
```

---

## Template: security-policy.md

```markdown
# Security Policy

## OWASP Top 10 Prevention

### Injection Prevention
- Use parameterized queries (NEVER string concatenation)
- Sanitize all user inputs
- Validate data types and formats

### Authentication
- Use secure session management
- Implement rate limiting on auth endpoints
- Require strong passwords (min 12 chars)
- Use MFA when possible

### Sensitive Data
- Never log sensitive data (passwords, tokens, PII)
- Encrypt data at rest and in transit
- Use environment variables for secrets
- Never commit secrets to git

### Access Control
- Implement least privilege principle
- Validate authorization on every request
- Use row-level security (RLS) if applicable

## Security Review Triggers

@security-architect MUST review:
- [ ] Authentication changes
- [ ] Authorization logic
- [ ] Data handling
- [ ] External API integrations
- [ ] File uploads
- [ ] Database queries

## Forbidden Patterns

```typescript
// NEVER DO THIS:
const query = `SELECT * FROM users WHERE id = ${userId}`;  // SQL Injection
innerHTML = userInput;  // XSS
eval(userCode);  // Code injection
```

## Required Patterns

```typescript
// ALWAYS DO THIS:
const query = db.query('SELECT * FROM users WHERE id = $1', [userId]);
textContent = userInput;  // Safe
// Never use eval with user input
```
```

---

## Template: git-workflow.md

```markdown
# Git Workflow

## Branching Strategy

| Branch | Purpose | Protected |
|--------|---------|-----------|
| `main` | Production | Yes |
| `develop` | Integration | Yes |
| `feature/*` | New features | No |
| `fix/*` | Bug fixes | No |
| `hotfix/*` | Production fixes | No |

## Branch Naming

```
feature/{issue-number}-{short-description}
fix/{issue-number}-{short-description}
hotfix/{issue-number}-{short-description}

Examples:
feature/123-add-user-auth
fix/456-login-validation-error
hotfix/789-security-patch
```

## Commit Messages

Use Conventional Commits format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructure
- `test`: Tests
- `chore`: Maintenance

**Examples**:
```
feat(auth): add JWT refresh token support
fix(api): handle null user gracefully
docs(readme): update installation steps
```

## Pull Request Requirements

- [ ] Descriptive title (conventional commit format)
- [ ] Description with context
- [ ] Link to issue/ticket
- [ ] All tests passing
- [ ] No merge conflicts
- [ ] At least 1 approval
- [ ] Security review (if applicable)
```

---

## Template: agent-coordination.md

```markdown
# Agent Coordination

## Agent Invocation Protocol

### When to Invoke Specialists

| Condition | Agent | Priority |
|-----------|-------|----------|
| Database schema changes | @database-architect | Required |
| New API endpoints | @api-contract-designer | Required |
| Backend business logic | @domain-logic-architect | Required |
| UI/Component work | @frontend-architect | Required |
| Security-sensitive changes | @security-architect | **MANDATORY** |
| Before feature completion | @acceptance-validator | **MANDATORY** |

### Invocation Order (DAG)

For full-stack features, invoke in this order:

```
1. @database-architect (if DB changes)
   ↓
2. @api-contract-designer (if API changes)
   ↓
3. @domain-logic-architect + @frontend-architect (parallel)
   ↓
4. @security-architect (MANDATORY gate)
   ↓
5. @implementation-test-engineer
```

## Output Artifacts

Each agent produces specific output files:

| Agent | Output File | Location |
|-------|-------------|----------|
| @database-architect | `database.md` | `.claude/docs/{feature}/` |
| @api-contract-designer | `api_contract.md` | `.claude/docs/{feature}/` |
| @domain-logic-architect | `backend.md` | `.claude/docs/{feature}/` |
| @frontend-architect | `frontend.md` | `.claude/docs/{feature}/` |
| @security-architect | `security_plan.md` | `.claude/docs/{feature}/` |

## Cross-Agent Validation

The `implementation-orchestrator` validates coherence:

- Database ↔ API contract (types, naming)
- API contract ↔ Backend (endpoints, handlers)
- Backend ↔ Frontend (API calls, state)

## Missing Agent Protocol

If a required agent is unavailable:

1. Invoke `@agent-librarian "scout: {agent-name}"`
2. Review and approve the draft
3. Continue with the recruited agent
```

---

## Usage Notes

1. **Keep files focused**: Each rules file should cover ONE domain
2. **Be actionable**: Rules should be clear "do this, not that"
3. **Use tables**: Easy to scan and reference
4. **Include examples**: Show correct and incorrect patterns
5. **Update regularly**: Rules should evolve with the project
