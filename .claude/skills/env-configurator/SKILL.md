---
name: env-configurator
description: Generates .env template files from CLAUDE.md environment variables section. Validates required variables, provides secure defaults, and creates example files for documentation.
---

# Environment Configurator

## Purpose

Automates the creation of environment variable configuration files (.env, .env.template, .env.example) based on the project's CLAUDE.md specifications. Ensures all required environment variables are documented, provides secure defaults, and helps prevent configuration errors.

## When to Use This Skill

Use this skill when:
- Setting up a new project for the first time
- Onboarding new developers who need environment setup
- Documenting environment variables for the team
- Deploying to a new environment (staging, production)
- After adding new environment variables to the codebase
- Auditing environment configuration for completeness

**Trigger phrases**: "create env file", "generate .env template", "set up environment variables", "configure environment"

## Workflow

### Step 1: Read Environment Variable Definitions

Read `CLAUDE.md` to extract `[environment_variables]` section:

```markdown
## [environment_variables]

# Application
PORT: Application port number (default: 3000)
NODE_ENV: Environment mode (development/production)

# Database
DATABASE_URL: PostgreSQL connection string
REDIS_URL: Redis connection string (optional)

# Authentication
JWT_SECRET: Secret key for JWT signing (required, generate with openssl rand -base64 32)
SESSION_SECRET: Secret key for sessions

# External APIs
STRIPE_API_KEY: Stripe API key for payments
STRIPE_WEBHOOK_SECRET: Stripe webhook signing secret
OPENAI_API_KEY: OpenAI API key (optional)

# Email
SMTP_HOST: SMTP server host
SMTP_PORT: SMTP server port (default: 587)
SMTP_USER: SMTP username
SMTP_PASSWORD: SMTP password

# Feature Flags
ENABLE_ANALYTICS: Enable analytics tracking (default: false)
```

### Step 2: Parse Variable Definitions

Extract information for each variable:
- **Name**: Variable name (e.g., `DATABASE_URL`)
- **Description**: What the variable is for
- **Type**: String, number, boolean, URL, etc.
- **Required**: Whether it's required or optional
- **Default**: Default value if any
- **Example**: Example value for documentation

### Step 3: Generate .env.template

Create `.env.template` with all variables but NO sensitive values:

```bash
# .env.template
# Copy this file to .env and fill in the values

# =============================================================================
# Application Configuration
# =============================================================================

# Application port number (default: 3000)
PORT=3000

# Environment mode (development/production)
NODE_ENV=development

# =============================================================================
# Database Configuration
# =============================================================================

# PostgreSQL connection string
# Required: Yes
# Example: postgresql://user:password@localhost:5432/dbname
DATABASE_URL=

# Redis connection string (optional)
# Required: No
# Example: redis://localhost:6379
REDIS_URL=

# =============================================================================
# Authentication
# =============================================================================

# Secret key for JWT signing
# Required: Yes
# Generate with: openssl rand -base64 32
JWT_SECRET=

# Secret key for sessions
# Required: Yes
SESSION_SECRET=

# =============================================================================
# External APIs
# =============================================================================

# Stripe API key for payments
# Required: Yes
STRIPE_API_KEY=

# Stripe webhook signing secret
# Required: Yes
STRIPE_WEBHOOK_SECRET=

# OpenAI API key (optional)
# Required: No
OPENAI_API_KEY=

# =============================================================================
# Email Configuration
# =============================================================================

# SMTP server host
SMTP_HOST=

# SMTP server port
SMTP_PORT=587

# SMTP username
SMTP_USER=

# SMTP password
SMTP_PASSWORD=

# =============================================================================
# Feature Flags
# =============================================================================

# Enable analytics tracking
ENABLE_ANALYTICS=false
```

### Step 4: Generate .env.example

Create `.env.example` with fake/example values for documentation:

```bash
# .env.example
# Example environment configuration
# DO NOT use these values in production!

# Application
PORT=3000
NODE_ENV=development

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=example_jwt_secret_do_not_use_in_production
SESSION_SECRET=example_session_secret_do_not_use

# External APIs
STRIPE_API_KEY=sk_test_51EXAMPLE_key_here
STRIPE_WEBHOOK_SECRET=whsec_EXAMPLE_webhook_secret
OPENAI_API_KEY=sk-proj-EXAMPLE_openai_key

# Email
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=587
SMTP_USER=your_mailtrap_user
SMTP_PASSWORD=your_mailtrap_password

# Feature Flags
ENABLE_ANALYTICS=false
```

### Step 5: Generate .env (Local Development)

Optionally create `.env` with development defaults:

```bash
# .env
# Local development environment
# This file is gitignored - never commit to version control!

PORT=3000
NODE_ENV=development

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/myapp_dev
REDIS_URL=redis://localhost:6379

# TODO: Generate these secrets
JWT_SECRET=
SESSION_SECRET=

# TODO: Add your API keys
STRIPE_API_KEY=
STRIPE_WEBHOOK_SECRET=
OPENAI_API_KEY=

# Email (use Mailtrap for development)
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

ENABLE_ANALYTICS=false
```

### Step 6: Generate README Section

Create documentation section for environment setup:

```markdown
## Environment Setup

This project requires environment variables to be configured before running.

### Quick Start

1. Copy the template file:
   ```bash
   cp .env.template .env
   ```

2. Fill in the required values in `.env`

3. Generate secrets:
   ```bash
   # JWT Secret
   openssl rand -base64 32

   # Session Secret
   openssl rand -base64 32
   ```

### Required Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | `postgresql://user:pass@localhost:5432/db` |
| `JWT_SECRET` | Secret for JWT signing | Yes | (generate with openssl) |
| `STRIPE_API_KEY` | Stripe API key | Yes | `sk_test_...` |

### Optional Variables

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `REDIS_URL` | Redis connection string | - | `redis://localhost:6379` |
| `OPENAI_API_KEY` | OpenAI API key | - | `sk-proj-...` |
| `ENABLE_ANALYTICS` | Enable analytics | `false` | `true` |

### Development vs Production

**Development** (`.env`):
- Use local database
- Use test API keys
- Disable analytics

**Production** (environment variables):
- Use managed database
- Use production API keys
- Enable analytics
- Never commit production values!

### Troubleshooting

**Missing required variable**:
```
Error: DATABASE_URL environment variable is required
```
Solution: Ensure all required variables are set in `.env`

**Invalid database URL**:
```
Error: Invalid DATABASE_URL format
```
Solution: Check connection string format: `postgresql://user:password@host:port/database`
```

### Step 7: Validate Configuration

Create a validation script to check environment variables:

```javascript
// scripts/validate-env.js
const requiredVars = [
  'DATABASE_URL',
  'JWT_SECRET',
  'SESSION_SECRET',
  'STRIPE_API_KEY',
];

const missing = requiredVars.filter(v => !process.env[v]);

if (missing.length > 0) {
  console.error('❌ Missing required environment variables:');
  missing.forEach(v => console.error(`   - ${v}`));
  process.exit(1);
}

console.log('✅ All required environment variables are set');
```

## Environment Variable Best Practices

### 1. Naming Conventions

- **UPPERCASE_WITH_UNDERSCORES**: Standard convention
- **Prefix by category**: `DB_HOST`, `DB_PORT` (related vars grouped)
- **Boolean flags**: `ENABLE_FEATURE` not `FEATURE_ENABLED`
- **Secrets suffix**: `API_KEY`, `API_SECRET`, `TOKEN`

### 2. Security

**Never commit:**
- API keys
- Database passwords
- JWT secrets
- OAuth client secrets
- Encryption keys

**Use .gitignore:**
```
.env
.env.local
.env.*.local
```

**Use environment-specific files:**
- `.env` - Local development (gitignored)
- `.env.template` - Template (committed)
- `.env.example` - Examples (committed)
- `.env.test` - Test environment (committed, no secrets)

### 3. Secret Generation

Generate strong secrets:

```bash
# Random base64 string (32 bytes)
openssl rand -base64 32

# Random hex string (64 characters)
openssl rand -hex 32

# UUID
uuidgen
```

### 4. Validation

Validate at application startup:

```typescript
// config/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']),
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  STRIPE_API_KEY: z.string().startsWith('sk_'),
});

export const env = envSchema.parse(process.env);
```

### 5. Documentation

Document every variable:
- **Purpose**: What it's used for
- **Format**: Expected format/type
- **Example**: Safe example value
- **Required**: Whether it's required
- **Default**: Default value if optional

## Platform-Specific Configuration

### Vercel

Create `vercel.json`:
```json
{
  "env": {
    "DATABASE_URL": "@database-url",
    "JWT_SECRET": "@jwt-secret"
  }
}
```

Set secrets:
```bash
vercel env add DATABASE_URL production
vercel env add JWT_SECRET production
```

### Netlify

Create `netlify.toml`:
```toml
[build.environment]
  NODE_VERSION = "20"

[context.production.environment]
  NODE_ENV = "production"
```

Set secrets in Netlify UI:
Site settings → Environment variables

### Docker

Pass env vars to container:
```bash
docker run -e DATABASE_URL="..." -e JWT_SECRET="..." myapp
```

Or use env file:
```bash
docker run --env-file .env.production myapp
```

### AWS (Parameter Store)

Store secrets in AWS Systems Manager Parameter Store:
```bash
aws ssm put-parameter \
  --name "/myapp/prod/database-url" \
  --value "postgresql://..." \
  --type "SecureString"
```

Retrieve in application:
```javascript
const { SSM } = require('@aws-sdk/client-ssm');
const ssm = new SSM();

const param = await ssm.getParameter({
  Name: '/myapp/prod/database-url',
  WithDecryption: true
});

process.env.DATABASE_URL = param.Parameter.Value;
```

## Automation Script

Use `scripts/generate_env.py` to automatically generate env files:

```bash
python .claude/skills/env-configurator/scripts/generate_env.py

# Options:
--template    # Generate .env.template
--example     # Generate .env.example
--local       # Generate .env for local dev
--readme      # Generate README section
--all         # Generate all files
```

## Integration with CI/CD

### GitHub Actions

```yaml
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  JWT_SECRET: ${{ secrets.JWT_SECRET }}

steps:
  - name: Validate environment
    run: npm run validate:env
```

### GitLab CI

```yaml
variables:
  NODE_ENV: production

before_script:
  - export DATABASE_URL=$DATABASE_URL_SECRET
```

## Common Patterns

### Multi-Environment Setup

```
.env                  # Local development (gitignored)
.env.template         # Template (committed)
.env.example          # Examples (committed)
.env.test             # Test environment (committed)
.env.staging          # Staging (managed by platform)
.env.production       # Production (managed by platform)
```

### Hierarchical Configuration

```bash
# Base config (shared)
.env

# Environment-specific overrides
.env.development
.env.production

# Local overrides (gitignored)
.env.local
```

Load order (later files override earlier):
1. `.env`
2. `.env.{environment}`
3. `.env.local`

## Resources

- **Script**: `scripts/generate_env.py` - Automated generation
- **Validation**: `scripts/validate_env.py` - Environment validation
- **Reference**: `references/env-best-practices.md` - Comprehensive guide
