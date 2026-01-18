---
name: ci-cd-architect
description: Generates CI/CD pipeline configurations for GitHub Actions, GitLab CI, Jenkins, and other platforms. Reads CLAUDE.md deployment strategy and creates optimized pipelines with testing, security scanning, and deployment stages.
---

# CI/CD Architect

## Purpose

Automates the creation of CI/CD pipeline configurations tailored to your project's technology stack and deployment platform. This skill generates production-ready pipeline files with best practices for testing, security scanning, building, and deployment.

## When to Use This Skill

Use this skill when:
- Setting up a new repository and need CI/CD pipelines
- Migrating from one CI/CD platform to another
- Adding new stages to existing pipelines (security scanning, E2E tests)
- Standardizing CI/CD across multiple projects
- Updating pipelines after major framework changes

**Trigger phrases**: "create CI/CD pipeline", "generate GitHub Actions workflow", "set up GitLab CI", "configure deployment pipeline"

## Workflow

### Step 1: Read Project Configuration

**Read CLAUDE.md to understand:**
- `[stack]` - Technology stack (Node.js, Python, etc.)
- `[deployment].platform` - Where to deploy (Vercel, AWS, etc.)
- `[deployment].ci_cd` - CI/CD platform (GitHub Actions, GitLab CI, etc.)
- `[testing_requirements]` - Test commands and coverage requirements
- `[code_standards]` - Linting and formatting tools

### Step 2: Select Pipeline Template

Based on `[deployment].ci_cd`, select appropriate template:

- **GitHub Actions**: `.github/workflows/ci-cd.yml`
- **GitLab CI**: `.gitlab-ci.yml`
- **Jenkins**: `Jenkinsfile`
- **CircleCI**: `.circleci/config.yml`
- **Azure Pipelines**: `azure-pipelines.yml`
- **Bitbucket Pipelines**: `bitbucket-pipelines.yml`

### Step 3: Generate Pipeline Configuration

Create pipeline with standard stages:

#### Stage 1: Build
- Check out code
- Set up language runtime (Node.js, Python, etc.)
- Install dependencies
- Cache dependencies for faster builds

#### Stage 2: Lint & Format
- Run linter (ESLint, Pylint, etc.)
- Run formatter checks (Prettier, Black)
- Run type checker (TypeScript, mypy)

#### Stage 3: Test
- Run unit tests
- Run integration tests
- Run E2E tests (if applicable)
- Generate coverage reports
- Upload coverage to Codecov/Coveralls

#### Stage 4: Security
- Run SAST (Semgrep, SonarQube)
- Run dependency vulnerability scanning (Snyk, npm audit)
- Run secrets detection (gitleaks)
- Container image scanning (if Docker used)

#### Stage 5: Build Artifacts
- Build production bundle
- Build Docker image (if applicable)
- Run smoke tests on build

#### Stage 6: Deploy
- Deploy to staging (on develop branch)
- Deploy to production (on main branch, manual approval)
- Run post-deployment health checks

### Step 4: Add Platform-Specific Features

#### GitHub Actions
- Use actions from marketplace (setup-node, checkout, etc.)
- Configure matrix builds for cross-platform testing
- Set up branch protection rules
- Configure deployment environments

#### GitLab CI
- Use GitLab-specific features (artifacts, caching)
- Configure Auto DevOps if applicable
- Set up GitLab Container Registry
- Configure merge request pipelines

#### Jenkins
- Use declarative pipeline syntax
- Configure Jenkins agents/nodes
- Set up credentials management
- Configure notifications (Slack, email)

### Step 5: Write Configuration File

Generate the complete pipeline configuration and save to appropriate location.

## Example: GitHub Actions (Node.js + Vercel)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  NODE_VERSION: '20'

jobs:
  # Stage 1 & 2: Build and Lint
  build-and-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run linter
        run: pnpm lint

      - name: Run type check
        run: pnpm type-check

  # Stage 3: Test
  test:
    runs-on: ubuntu-latest
    needs: build-and-lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Run unit tests
        run: pnpm test:unit --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage/coverage-final.json

      - name: Run E2E tests
        run: pnpm test:e2e

  # Stage 4: Security
  security:
    runs-on: ubuntu-latest
    needs: build-and-lint
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Semgrep SAST
        uses: returntocorp/semgrep-action@v1
        with:
          config: auto

      - name: Run Snyk security scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Run gitleaks secrets scan
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  # Stage 5: Build
  build:
    runs-on: ubuntu-latest
    needs: [test, security]
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build application
        run: pnpm build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/

  # Stage 6: Deploy to Staging
  deploy-staging:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to Vercel (Staging)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          scope: ${{ secrets.VERCEL_ORG_ID }}

  # Stage 6: Deploy to Production
  deploy-production:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://example.com
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to Vercel (Production)
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          scope: ${{ secrets.VERCEL_ORG_ID }}

      - name: Post-deployment health check
        run: |
          curl -f https://example.com/health || exit 1
```

## Example: GitLab CI (Python + AWS)

```yaml
# .gitlab-ci.yml
image: python:3.11

stages:
  - build
  - test
  - security
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  DOCKER_IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt

# Stage 1: Install dependencies
install:
  stage: build
  script:
    - pip install -r requirements-dev.txt
  artifacts:
    paths:
      - venv/

# Stage 2: Lint
lint:
  stage: test
  script:
    - black --check .
    - flake8 .
    - mypy .

# Stage 3: Test
test:unit:
  stage: test
  script:
    - pytest tests/unit --cov=app --cov-report=xml
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

test:integration:
  stage: test
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test_db
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test_db
  script:
    - pytest tests/integration

# Stage 4: Security
security:sast:
  stage: security
  image: returntocorp/semgrep
  script:
    - semgrep --config auto --json -o gl-sast-report.json
  artifacts:
    reports:
      sast: gl-sast-report.json

security:dependency-scan:
  stage: security
  script:
    - pip install safety
    - safety check --json

security:secrets:
  stage: security
  image: zricethezav/gitleaks:latest
  script:
    - gitleaks detect --source . --verbose --redact

# Stage 5: Build Docker image
build:docker:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $DOCKER_IMAGE .
    - docker push $DOCKER_IMAGE
  only:
    - main
    - develop

# Stage 6: Deploy to staging
deploy:staging:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cloud-deploy/aws-base:latest
  script:
    - aws ecs update-service --cluster staging-cluster --service app-service --force-new-deployment
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - develop

# Stage 6: Deploy to production
deploy:production:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/cloud-deploy/aws-base:latest
  script:
    - aws ecs update-service --cluster production-cluster --service app-service --force-new-deployment
  environment:
    name: production
    url: https://example.com
  when: manual
  only:
    - main
```

## Pipeline Best Practices

### 1. Performance Optimization
- **Cache dependencies**: node_modules, pip cache, Maven .m2
- **Use matrix builds**: Test across multiple versions in parallel
- **Fail fast**: Run quick checks (lint) before slow ones (E2E tests)
- **Artifacts**: Share build outputs between jobs

### 2. Security Integration
- **SAST**: Static analysis (Semgrep, SonarQube)
- **Dependency scanning**: Check for vulnerable packages (Snyk, npm audit)
- **Secrets detection**: Scan for leaked credentials (gitleaks)
- **Container scanning**: Scan Docker images (Trivy, Grype)

### 3. Testing Strategy
- **Unit tests**: Fast, run on every commit
- **Integration tests**: Run before merge
- **E2E tests**: Run on staging environment
- **Coverage thresholds**: Enforce minimum coverage (e.g., 80%)

### 4. Deployment Strategy
- **Staging first**: Always deploy to staging before production
- **Manual gates**: Require approval for production deployments
- **Health checks**: Verify deployment success with health endpoints
- **Rollback**: Automate rollback on health check failures

### 5. Notification Strategy
- **Slack/Teams**: Notify on build failures and deployments
- **Email**: Notify maintainers on production deployments
- **GitHub/GitLab**: Update PR/MR status automatically

## Platform-Specific Templates

### Template 1: GitHub Actions + Docker + AWS ECS

See `assets/github-actions-docker-ecs.yml`

### Template 2: GitLab CI + Kubernetes

See `assets/gitlab-ci-kubernetes.yml`

### Template 3: Jenkins Declarative Pipeline

See `assets/Jenkinsfile-declarative`

### Template 4: CircleCI with Orbs

See `assets/circleci-config.yml`

## Environment Variables & Secrets

### Required Secrets (GitHub Actions)
```
VERCEL_TOKEN          # For Vercel deployments
VERCEL_ORG_ID         # Vercel organization ID
VERCEL_PROJECT_ID     # Vercel project ID
CODECOV_TOKEN         # For coverage uploads
SNYK_TOKEN            # For security scanning
AWS_ACCESS_KEY_ID     # For AWS deployments
AWS_SECRET_ACCESS_KEY # For AWS deployments
```

### Required Variables (GitLab CI)
```
CI_REGISTRY_IMAGE     # GitLab container registry
AWS_DEFAULT_REGION    # AWS region for deployment
PRODUCTION_CLUSTER    # ECS cluster name
```

## Integration with Other Skills

### After CI/CD Setup
1. **dependency-installer**: Ensures consistent dependency installation
2. **hooks-setup**: Configures pre-commit hooks that match CI checks
3. **env-configurator**: Sets up environment variables for deployment

### Before CI/CD Setup
1. **devops-architect**: Designs overall deployment strategy
2. **claude-md-architect**: Documents deployment requirements in CLAUDE.md

## Automation Script

Use `scripts/generate_pipeline.py` to automatically generate pipelines:

```bash
python .claude/skills/ci-cd-architect/scripts/generate_pipeline.py

# Options:
--platform github        # Generate GitHub Actions workflow
--platform gitlab        # Generate GitLab CI config
--platform jenkins       # Generate Jenkinsfile
--stack node            # Technology stack
--deployment vercel     # Deployment platform
```

## Troubleshooting

### Common Issues

**1. Tests fail in CI but pass locally**
- Ensure same Node/Python version in CI as locally
- Check for missing environment variables
- Verify database/service availability

**2. Build caching not working**
- Verify cache key configuration
- Check cache size limits
- Ensure cache paths are correct

**3. Secrets not available**
- Verify secrets are set in CI/CD platform settings
- Check secret names match exactly (case-sensitive)
- Ensure secrets are available to the branch

**4. Deployment fails silently**
- Add verbose logging to deployment scripts
- Check deployment platform logs
- Verify credentials and permissions

## Resources

- **Templates**: `assets/` - Ready-to-use CI/CD templates
- **Reference**: `references/ci-cd-platforms.md` - Detailed platform comparison
- **Script**: `scripts/generate_pipeline.py` - Automated pipeline generation
