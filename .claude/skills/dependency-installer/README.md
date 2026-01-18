# Dependency Installer Skill

Automates dependency installation across multiple programming languages and package managers.

## Features

- **Multi-Language Support**: Node.js, Python, Ruby, Rust, Go, PHP
- **Auto-Detection**: Automatically detects package manager from lock files
- **Conflict Resolution**: Handles lock file merge conflicts
- **Verification**: Verifies successful installation
- **CI/CD Ready**: Optimized commands for continuous integration
- **Error Handling**: Provides helpful error messages and solutions

## Supported Package Managers

### Node.js
- **pnpm** (recommended): Fast, disk-efficient package manager
- **npm**: Default Node.js package manager
- **yarn**: Alternative package manager (v1.x and v2+)
- **bun**: Ultra-fast all-in-one toolkit

### Python
- **pip**: Standard Python package installer
- **poetry**: Modern dependency management
- **pipenv**: Virtual environment + dependency manager

### Ruby
- **bundler**: Ruby dependency manager

### Rust
- **cargo**: Rust's package manager

### Go
- **go modules**: Go's dependency management

### PHP
- **composer**: PHP dependency manager

## Quick Start

```bash
# Invoke via Claude
"Install the project dependencies"

# Or run script directly
python .claude/skills/dependency-installer/scripts/install_dependencies.py
```

## Common Use Cases

### 1. New Project Setup
```bash
git clone https://github.com/user/project
cd project
# Use skill: "Install dependencies"
```

### 2. After Branch Switch
```bash
git checkout feature-branch
# Use skill: "Install dependencies to sync with branch"
```

### 3. Lock File Conflict Resolution
```bash
git merge main
# Conflict in package-lock.json
# Use skill: "Resolve lock file conflict and install dependencies"
```

### 4. CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
- name: Install dependencies
  run: python .claude/skills/dependency-installer/scripts/install_dependencies.py
```

## Installation Options

### Node.js

**Clean Install (CI/CD)**:
```bash
npm ci              # Fast, uses lock file exactly
pnpm install --frozen-lockfile
yarn install --immutable
```

**Regular Install (Development)**:
```bash
npm install         # Updates lock file if needed
pnpm install
yarn install
```

### Python

**With Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**With Poetry**:
```bash
poetry install
```

## Troubleshooting

### Permission Errors (npm)
```bash
# Use Node version manager (recommended)
nvm install 20
nvm use 20

# Or fix npm permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
```

### Lock File Out of Sync
```bash
# Delete and regenerate
rm package-lock.json
npm install
```

### Network Issues
```bash
# Configure registry mirror
npm config set registry https://registry.npmmirror.com

# Configure proxy
npm config set proxy http://proxy.company.com:8080
```

### Disk Space
```bash
# Clean cache
npm cache clean --force
pnpm store prune
yarn cache clean

# Check space
df -h
```

## Performance Tips

1. **Use pnpm**: 2-3x faster than npm, saves disk space
2. **Enable Caching**: Cache node_modules in CI/CD
3. **Use Frozen Lockfiles**: `--frozen-lockfile` prevents unexpected updates
4. **Parallelize**: Some managers support parallel downloads
5. **Clean Caches**: Periodically clean to free disk space

## Integration Examples

### GitHub Actions
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'

- run: pnpm install --frozen-lockfile
```

### GitLab CI
```yaml
install:
  script:
    - pnpm install --frozen-lockfile
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .pnpm-store/
```

### Docker
```dockerfile
COPY package*.json ./
RUN npm ci --only=production
```

## Advanced Features

### Automated Installation Script

The included Python script provides:
- Color-coded output
- Progress indicators
- Error detection and helpful messages
- Installation verification
- Time tracking
- Security audit integration

**Usage**:
```bash
python .claude/skills/dependency-installer/scripts/install_dependencies.py

# Options:
--force           # Force reinstall even if already installed
--skip-audit      # Skip security audit
--dev             # Include development dependencies
```

## Related Skills

- **hooks-setup**: Automatically configures Git hooks after installation
- **env-configurator**: Sets up environment variables after dependencies
- **ci-cd-architect**: Designs CI/CD pipelines with dependency installation

## Contributing

To extend this skill with new package managers:

1. Add detection logic to `scripts/install_dependencies.py`
2. Add install commands to SKILL.md
3. Update supported package managers list
4. Add troubleshooting section if needed

## License

Part of Genesis Factory v5 framework.
