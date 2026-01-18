# CI/CD Architect Skill

Generates production-ready CI/CD pipeline configurations for multiple platforms.

## Features

- **Multi-Platform**: GitHub Actions, GitLab CI, Jenkins, CircleCI, Azure Pipelines
- **Best Practices**: Includes testing, security scanning, deployment stages
- **Technology-Aware**: Adapts to Node.js, Python, Ruby, Go, Rust, etc.
- **Security-First**: Integrates SAST, dependency scanning, secrets detection
- **Optimized**: Caching, parallel jobs, fail-fast strategies

## Supported Platforms

- **GitHub Actions** - Most popular for GitHub repos
- **GitLab CI/CD** - Native GitLab integration
- **Jenkins** - Enterprise CI/CD server
- **CircleCI** - Cloud-based CI/CD
- **Azure Pipelines** - Microsoft ecosystem
- **Bitbucket Pipelines** - For Bitbucket repos

## Quick Start

```bash
# Invoke via Claude
"Create a CI/CD pipeline for GitHub Actions"

# Or generate directly
python .claude/skills/ci-cd-architect/scripts/generate_pipeline.py --platform github
```

## Pipeline Stages

All generated pipelines include:

1. **Build**: Dependency installation, caching
2. **Lint**: Code quality checks (ESLint, Prettier, etc.)
3. **Test**: Unit, integration, E2E tests with coverage
4. **Security**: SAST, dependency scanning, secrets detection
5. **Build Artifacts**: Production builds, Docker images
6. **Deploy**: Staging and production deployments

## Example Workflows

### GitHub Actions (Node.js)

```yaml
name: CI/CD
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test --coverage

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-args: '--prod'
```

### GitLab CI (Python)

```yaml
image: python:3.11

stages: [test, deploy]

test:
  stage: test
  script:
    - pip install -r requirements-dev.txt
    - pytest --cov

deploy:
  stage: deploy
  script:
    - aws ecs update-service --cluster prod --service app --force-new-deployment
  only: [main]
  when: manual
```

## Configuration

### Required Secrets

Set these in your CI/CD platform:

**GitHub Actions**:
- Settings → Secrets and variables → Actions → New repository secret

**GitLab CI**:
- Settings → CI/CD → Variables → Add variable

**Common secrets**:
- `CODECOV_TOKEN` - For coverage uploads
- `SNYK_TOKEN` - For security scanning
- `VERCEL_TOKEN` - For Vercel deployments
- `AWS_ACCESS_KEY_ID` - For AWS deployments
- `AWS_SECRET_ACCESS_KEY` - For AWS deployments

### Environment Variables

Configure in CLAUDE.md:

```markdown
## [deployment]

platform: Vercel
ci_cd: GitHub Actions
environments:
  - name: staging
    url: https://staging.example.com
  - name: production
    url: https://example.com
    manual_approval: true
```

## Advanced Features

### Matrix Builds

Test across multiple versions:

```yaml
strategy:
  matrix:
    node-version: [18, 20, 21]
    os: [ubuntu-latest, windows-latest, macos-latest]
```

### Conditional Execution

Run jobs only when needed:

```yaml
if: |
  github.event_name == 'push' &&
  github.ref == 'refs/heads/main'
```

### Caching

Speed up builds with caching:

```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Artifacts

Share build outputs:

```yaml
- uses: actions/upload-artifact@v3
  with:
    name: build
    path: dist/
```

## Security Integration

### SAST (Static Analysis)

```yaml
- name: Run Semgrep
  uses: returntocorp/semgrep-action@v1
```

### Dependency Scanning

```yaml
- name: Run Snyk
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### Secrets Detection

```yaml
- name: Run gitleaks
  uses: gitleaks/gitleaks-action@v2
```

## Best Practices

1. **Cache aggressively**: node_modules, pip cache, Docker layers
2. **Run quick checks first**: Lint before tests, tests before builds
3. **Use matrix builds**: Test across versions and platforms
4. **Require manual approval**: For production deployments
5. **Add health checks**: Verify deployments succeeded
6. **Set up notifications**: Alert team on failures
7. **Monitor build times**: Optimize slow steps

## Troubleshooting

### Build Failures

**Tests pass locally but fail in CI**:
- Check Node/Python versions match
- Verify environment variables are set
- Ensure database/services are available

**Caching issues**:
- Clear cache and rebuild
- Verify cache key is correct
- Check cache size limits

**Deployment failures**:
- Check credentials and permissions
- Verify target platform is accessible
- Review deployment logs

### Performance Issues

**Slow builds**:
- Enable caching
- Use smaller Docker images
- Run jobs in parallel
- Use matrix builds sparingly

## Templates

Pre-configured templates available in `assets/`:

- `github-actions-node-vercel.yml` - Node.js with Vercel
- `github-actions-docker-ecs.yml` - Docker with AWS ECS
- `gitlab-ci-kubernetes.yml` - GitLab with Kubernetes
- `Jenkinsfile-declarative` - Jenkins declarative pipeline
- `circleci-config.yml` - CircleCI with orbs

## Related Skills

- **devops-architect**: Designs overall deployment strategy
- **dependency-installer**: Consistent dependency installation
- **hooks-setup**: Local checks matching CI pipeline

## Contributing

To add support for new platforms:

1. Create template in `assets/`
2. Add platform detection to `scripts/generate_pipeline.py`
3. Update SKILL.md with examples
4. Add to supported platforms list

## License

Part of Genesis Factory v5 framework.
