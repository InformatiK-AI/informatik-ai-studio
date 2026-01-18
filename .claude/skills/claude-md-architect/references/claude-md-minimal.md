# CLAUDE.md Minimal Template

This is a **minimal viable** CLAUDE.md template for new projects, simple stacks, and early-stage development. It includes only essential sections to get agents started quickly.

**Target Length:** 300-400 lines
**Use When:** Bootstrapping new projects, proof-of-concepts, simple applications
**Expand Later:** Add sections from [claude-md-template.md](./claude-md-template.md) as the project grows

---

````markdown
# [Project Name]

> **Version**: 1.0.0
> **Last Updated**: YYYY-MM-DD
> **Status**: [Development | Production]

---

## [ESSENTIAL] Project Metadata

**Description**: [1-2 sentence description of what this project does]

**Objectives**:

- [Primary objective - what problem does this solve?]
- [Key success criteria]

**Repository**: [GitHub URL]
**Tech Stack**: [See [stack] section below]

---

## [ESSENTIAL] Technology Stack

**Factory Vertical**: [A | B | C] - [See references/factory-verticals.md]

**Core Technologies**:

- **Framework**: [e.g., Astro 5, Next.js 14, FastAPI 0.109]
- **Language**: [e.g., TypeScript 5.7, Python 3.11]
- **Styling**: [e.g., Tailwind CSS 4, CSS Modules]
- **Database**: [e.g., Supabase (PostgreSQL), None (static)]

**Key Dependencies**:

```json
{
  "framework": "version",
  "key-library": "version"
}
```
````

**Rationale**: [1-2 sentences on why this stack was chosen]

---

## [ESSENTIAL] Core Team

Define specialized agents and their responsibilities.

### @security-architect

- **Role**: Security analysis and vulnerability assessment
- **When to Invoke**: Before merging features that touch auth, data handling, or external APIs

### @acceptance-validator

- **Role**: Quality assurance and acceptance testing
- **When to Invoke**: Before marking features as complete

### [Add other project-specific agents as needed]

---

## [ESSENTIAL] Directory Structure

```
project/
├── src/                    # Source code
│   ├── [key-directory]/   # [Brief description]
│   └── [key-directory]/   # [Brief description]
├── tests/                 # Test files
├── public/                # Static assets (if applicable)
├── .claude/              # Claude Code configuration
├── .env.example          # Example environment variables
├── package.json          # Dependencies (or pyproject.toml, requirements.txt)
└── README.md             # Public documentation
```

**Key Paths**:

- Configuration: `[path/to/config]`
- Main entry point: `[path/to/main]`
- [Other critical paths]

---

## [ESSENTIAL] Environment Variables

### Required

```env
# [Category - e.g., API Keys, Database]
VAR_NAME=description-of-what-this-is

# [Additional categories as needed]
```

### Optional

```env
# [Optional variables]
FEATURE_FLAG=true
```

**Where to Set**:

- Local: `.env.local` (not committed)
- Production: [Vercel/Netlify dashboard, etc.]

---

## [ESSENTIAL] Commands

### Development

```bash
[package-manager] run dev       # Start development server
[package-manager] run build     # Build for production
[package-manager] run preview   # Preview production build
```

### Testing

```bash
[package-manager] test          # Run all tests
[package-manager] run test:coverage  # Run with coverage
```

### Code Quality

```bash
[package-manager] run lint      # Lint code
[package-manager] run format    # Format code
[package-manager] run type-check # Check types (if TypeScript)
```

---

## [ESSENTIAL] Development Workflow

### Git Workflow

**Branch Naming**:

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation

**Commit Format**:

```
type(scope): brief description

Types: feat, fix, docs, refactor, test, chore
```

### Pre-commit Checklist

- [ ] All tests pass
- [ ] No linting errors
- [ ] TypeScript compiles (if applicable)
- [ ] New features have tests

### Pull Request Process

1. Create feature branch
2. Implement changes with tests
3. Run quality checks: `[lint && type-check && test]`
4. Open PR with description
5. Request review (invoke `@acceptance-validator` if needed)
6. Merge after approval

---

## [ESSENTIAL] Code Standards

### General Principles

- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple
- **Test Coverage**: Aim for 80%+ on critical paths

### [Language]-Specific Standards

[Add 3-5 key conventions for your primary language]

Examples:

- Use `const` over `let` (JavaScript/TypeScript)
- Prefer composition over inheritance
- Keep functions small (<50 lines)
- Use descriptive names

### File Naming

- Components: PascalCase (`UserProfile.tsx`)
- Utilities: camelCase (`formatDate.ts`)
- Constants: UPPER_SNAKE_CASE (`API_URL.ts`)

---

## [ESSENTIAL] Testing Requirements

### Coverage Expectations

- **Minimum**: 80% overall
- **Critical paths**: 100% (auth, payments, core logic)

### Test Types

**Unit Tests**: `tests/unit/` or co-located `*.test.[ext]`
**Integration Tests**: `tests/integration/`

### What to Test

- ✅ Business logic and utilities
- ✅ Component behavior
- ✅ Error handling
- ❌ Implementation details
- ❌ Third-party libraries

---

## [RECOMMENDED] Deployment

### Environments

| Environment | URL              | Branch | Auto-Deploy |
| ----------- | ---------------- | ------ | ----------- |
| Development | localhost        | `*`    | No          |
| Production  | [production-url] | `main` | Yes         |

### Deployment Process

**Automated** (Continuous Deployment):

1. Push to `main`
2. CI/CD runs tests and builds
3. Deploys automatically

**Rollback**: [Hosting platform's rollback feature or `git revert`]

---

## [OPTIONAL] Project-Specific Context

[Add any critical business rules, domain knowledge, or external integrations here]

Example:

- **Authentication**: Using [Auth0/Supabase/custom]
- **Key Business Rules**: [List 2-3 critical rules]
- **External APIs**: [List key integrations]

---

## Quick Reference

**Key Commands**:

- Dev: `[package-manager] run dev`
- Build: `[package-manager] run build`
- Test: `[package-manager] test`

**Key Files**:

- Config: `[config-file-path]`
- Entry: `[main-file-path]`

**Key Rules**:

- Test everything (80%+ coverage)
- Follow commit conventions
- No secrets in code

**Need Help?**

- Read: [Link to external docs]
- Ask: [Team contact/Slack channel]

---

## Expanding This CLAUDE.md

As your project grows, consider adding these sections from [claude-md-template.md](./claude-md-template.md):

- **[agent_guidelines]**: Detailed agent collaboration patterns
- **[security_requirements]**: Comprehensive security checklist
- **[performance_requirements]**: Performance targets and optimization strategies
- **[roadmap]**: Feature roadmap and technical debt tracking

Move detailed patterns to:

- `.claude/docs/patterns/` - Implementation patterns
- `.claude/docs/architecture/` - System design docs
- `.claude/examples/` - Code examples

---

**End of Minimal CLAUDE.md**

```

---

## Usage Notes

This minimal template:

1. **Starts lean**: Only essential sections for agents to begin work
2. **Grows with project**: Add sections as needed, don't over-document upfront
3. **300-400 lines**: Optimal for quick parsing by agents and humans
4. **Quick Reference**: Agents find key info in <100 tokens
5. **Expansion path**: Clear guidance on when and how to add more detail

**When to Use Full Template:**
- Enterprise/multi-team projects
- Complex technical requirements
- Established projects with extensive patterns
- Projects requiring detailed agent coordination

**Progressive Disclosure Approach:**
1. Start with this minimal template
2. Add sections from full template as needs arise
3. Extract lengthy details to separate files (`.claude/docs/`, `.claude/examples/`)
4. Keep main CLAUDE.md focused and scannable
```
