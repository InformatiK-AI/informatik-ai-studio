---
name: dependency-installer
description: Automates dependency installation for Node.js, Python, Ruby, and other projects. Auto-detects package managers and handles installation, lock file conflicts, and verification.
---

# Dependency Installer

## Purpose

Automates the process of installing project dependencies across multiple languages and package managers. This skill eliminates manual installation steps, handles lock file conflicts intelligently, and verifies successful installation.

## When to Use This Skill

Use this skill immediately after:
- Cloning a new repository
- Creating a new project with package.json/requirements.txt/Gemfile/etc.
- Switching branches that have dependency changes
- After merge conflicts in lock files
- When setting up CI/CD environments
- When onboarding new developers

**Trigger phrases**: "install dependencies", "run npm install", "install packages", "set up project dependencies"

## Workflow

### Step 1: Detect Project Type and Package Manager

**Auto-detect package manager from lock files:**

```bash
# Check for lock files in project root
if [ -f "pnpm-lock.yaml" ]; then
    PKG_MANAGER="pnpm"
elif [ -f "yarn.lock" ]; then
    PKG_MANAGER="yarn"
elif [ -f "package-lock.json" ]; then
    PKG_MANAGER="npm"
elif [ -f "bun.lockb" ]; then
    PKG_MANAGER="bun"
elif [ -f "package.json" ]; then
    PKG_MANAGER="npm"  # Default to npm if no lock file

elif [ -f "poetry.lock" ]; then
    PKG_MANAGER="poetry"
elif [ -f "Pipfile.lock" ]; then
    PKG_MANAGER="pipenv"
elif [ -f "requirements.txt" ]; then
    PKG_MANAGER="pip"

elif [ -f "Gemfile.lock" ]; then
    PKG_MANAGER="bundle"

elif [ -f "Cargo.lock" ]; then
    PKG_MANAGER="cargo"

elif [ -f "go.mod" ]; then
    PKG_MANAGER="go"

elif [ -f "composer.lock" ]; then
    PKG_MANAGER="composer"
fi
```

### Step 2: Check for Existing Installation

Before installing, check if dependencies are already installed:

**Node.js (npm/pnpm/yarn/bun):**
```bash
if [ -d "node_modules" ] && [ -f "package-lock.json" ]; then
    echo "✓ Dependencies appear to be installed"
    echo "Run 'npm ci' to ensure clean install or 'npm install' to update"
fi
```

**Python (pip/poetry/pipenv):**
```bash
# Check if venv exists and has packages
if [ -d "venv" ] || [ -d ".venv" ]; then
    echo "✓ Virtual environment exists"
fi
```

### Step 3: Install Dependencies

Execute appropriate install command based on detected package manager:

#### Node.js

**pnpm (fastest, disk-efficient):**
```bash
pnpm install --frozen-lockfile
```

**npm:**
```bash
# Clean install (recommended for CI)
npm ci

# Or regular install (updates lock file if needed)
npm install
```

**yarn:**
```bash
# Yarn 1.x
yarn install --frozen-lockfile

# Yarn 2+ (Berry)
yarn install --immutable
```

**bun:**
```bash
bun install --frozen-lockfile
```

#### Python

**pip with venv:**
```bash
# Create virtual environment if doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate and install
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Or with extras
pip install -r requirements-dev.txt
```

**poetry:**
```bash
poetry install

# Without dev dependencies
poetry install --without dev

# Sync exact versions from lock
poetry install --sync
```

**pipenv:**
```bash
pipenv install

# Install dev dependencies
pipenv install --dev
```

#### Ruby

**bundler:**
```bash
bundle install

# Or specific path
bundle install --path vendor/bundle
```

#### Rust

**cargo:**
```bash
cargo fetch  # Download dependencies
cargo build  # Build project (also installs deps)
```

#### Go

**go modules:**
```bash
go mod download  # Download dependencies
go mod tidy      # Clean up unused dependencies
```

#### PHP

**composer:**
```bash
composer install

# Without dev dependencies
composer install --no-dev

# Optimize autoloader
composer install --optimize-autoloader
```

### Step 4: Handle Lock File Conflicts

When lock files have merge conflicts:

```bash
# For npm
rm package-lock.json
npm install

# For pnpm
rm pnpm-lock.yaml
pnpm install

# For yarn
rm yarn.lock
yarn install

# For Python poetry
rm poetry.lock
poetry lock
poetry install

# Commit the regenerated lock file
git add [lock-file]
git commit -m "chore: regenerate lock file after merge"
```

### Step 5: Verify Installation

After installation, verify dependencies are correctly installed:

#### Node.js Verification

```bash
# Check node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ Installation failed: node_modules not found"
    exit 1
fi

# Verify package integrity (npm)
npm ls --depth=0

# Check for vulnerabilities
npm audit

# Check outdated packages (informational)
npm outdated
```

#### Python Verification

```bash
# Verify packages installed
pip list

# Check for security vulnerabilities
pip-audit  # If installed

# Verify specific package
python -c "import flask" || echo "❌ Flask not installed"
```

#### General Verification

```bash
# Run a simple test or build to ensure dependencies work
npm run build || echo "Build failed, dependencies may be incomplete"
```

### Step 6: Report Results

Provide clear feedback to the user:

```
✅ Dependencies installed successfully!

Package Manager: pnpm
Total Packages: 847
Installation Time: 12.3s

Next Steps:
- Run tests: pnpm test
- Start dev server: pnpm dev
- Build for production: pnpm build
```

## Example: Complete Installation Workflow

```bash
#!/bin/bash

echo "🚀 Installing project dependencies..."

# Step 1: Detect package manager
if [ -f "pnpm-lock.yaml" ]; then
    echo "📦 Detected: pnpm"
    PKG_MANAGER="pnpm"
    INSTALL_CMD="pnpm install --frozen-lockfile"
elif [ -f "package-lock.json" ]; then
    echo "📦 Detected: npm"
    PKG_MANAGER="npm"
    INSTALL_CMD="npm ci"
elif [ -f "yarn.lock" ]; then
    echo "📦 Detected: yarn"
    PKG_MANAGER="yarn"
    INSTALL_CMD="yarn install --frozen-lockfile"
elif [ -f "poetry.lock" ]; then
    echo "📦 Detected: poetry"
    PKG_MANAGER="poetry"
    INSTALL_CMD="poetry install"
else
    echo "❌ No lock file found. Unable to determine package manager."
    exit 1
fi

# Step 2: Check if already installed
if [ "$PKG_MANAGER" = "pnpm" ] || [ "$PKG_MANAGER" = "npm" ] || [ "$PKG_MANAGER" = "yarn" ]; then
    if [ -d "node_modules" ]; then
        echo "ℹ️  node_modules exists. Running install to ensure consistency..."
    fi
fi

# Step 3: Run installation
echo "⏳ Running: $INSTALL_CMD"
START_TIME=$(date +%s)

if $INSTALL_CMD; then
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))

    echo "✅ Installation completed in ${DURATION}s"

    # Step 4: Verify
    if [ "$PKG_MANAGER" = "pnpm" ] || [ "$PKG_MANAGER" = "npm" ] || [ "$PKG_MANAGER" = "yarn" ]; then
        PKG_COUNT=$(find node_modules -maxdepth 1 -type d | wc -l)
        echo "📊 Total packages: $PKG_COUNT"
    fi

    # Step 5: Security audit
    echo "🔒 Running security audit..."
    if [ "$PKG_MANAGER" = "npm" ]; then
        npm audit --production || echo "⚠️  Security vulnerabilities found"
    elif [ "$PKG_MANAGER" = "pnpm" ]; then
        pnpm audit --production || echo "⚠️  Security vulnerabilities found"
    fi

    echo ""
    echo "🎉 Ready to develop!"
    echo "Next: $PKG_MANAGER run dev"
else
    echo "❌ Installation failed"
    exit 1
fi
```

## Common Issues and Solutions

### Issue 1: "EACCES" Permission Errors (npm)

**Problem**: npm tries to write to system directories

**Solution**:
```bash
# Option 1: Use a Node version manager (recommended)
# Install nvm or fnm, then reinstall Node

# Option 2: Change npm's default directory
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Option 3: Fix permissions (not recommended)
sudo chown -R $(whoami) ~/.npm
```

### Issue 2: Lock File Out of Sync

**Problem**: "Lock file is out of sync with package.json"

**Solution**:
```bash
# Delete and regenerate lock file
rm pnpm-lock.yaml  # or package-lock.json or yarn.lock
pnpm install       # or npm install or yarn install
```

### Issue 3: Disk Space Issues

**Problem**: "ENOSPC: no space left on device"

**Solution**:
```bash
# Clean package manager cache
npm cache clean --force
# or
pnpm store prune
# or
yarn cache clean

# Check disk space
df -h
```

### Issue 4: Network/Proxy Issues

**Problem**: Cannot download packages due to network

**Solution**:
```bash
# Configure proxy (if behind corporate proxy)
npm config set proxy http://proxy.company.com:8080
npm config set https-proxy http://proxy.company.com:8080

# Or use a different registry
npm config set registry https://registry.npmmirror.com

# For Python
pip install --proxy http://proxy.company.com:8080 -r requirements.txt
```

### Issue 5: Conflicting Peer Dependencies

**Problem**: npm/yarn reports peer dependency conflicts

**Solution**:
```bash
# npm 7+: Use --legacy-peer-deps
npm install --legacy-peer-deps

# Or force install (not recommended)
npm install --force

# Best: Update dependencies to resolve conflicts
npm update [package-name]
```

## Integration with CI/CD

### GitHub Actions

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'pnpm'  # or 'npm' or 'yarn'

- name: Install dependencies
  run: pnpm install --frozen-lockfile
```

### GitLab CI

```yaml
install:
  script:
    - pnpm install --frozen-lockfile
  cache:
    paths:
      - node_modules/
      - .pnpm-store/
```

### Docker

```dockerfile
# Node.js
COPY package*.json ./
RUN npm ci --only=production

# Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
```

## Performance Tips

1. **Use CI-optimized commands**: `npm ci` instead of `npm install`
2. **Enable caching**: Cache node_modules or .pnpm-store in CI
3. **Use frozen lockfiles**: Prevent unexpected updates
4. **Parallelize when possible**: Some package managers support parallel downloads
5. **Clean cache periodically**: Free up disk space

## Automation Script

See `scripts/install_dependencies.py` for a comprehensive Python script that:
- Auto-detects all supported package managers
- Provides colored output and progress indicators
- Handles errors gracefully with helpful messages
- Verifies installation success
- Generates installation reports

**Usage**:
```bash
python .claude/skills/dependency-installer/scripts/install_dependencies.py
```

## Resources

- **Script**: `scripts/install_dependencies.py` - Automated installation with verification
- **Reference**: `references/package-managers.md` - Detailed guide for all package managers
