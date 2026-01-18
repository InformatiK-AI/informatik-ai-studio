# Scripts Documentation

This directory contains executable scripts for the **senior-frontend** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `bundle_analyzer.py` | Analyze JavaScript/TypeScript bundle sizes | Production |
| `component_generator.py` | Generate React/Vue/Svelte components | Production |
| `frontend_scaffolder.py` | Scaffold frontend project structure | Production |

---

## bundle_analyzer.py

**Purpose:** Analyzes JavaScript/TypeScript bundle sizes to identify optimization opportunities, large dependencies, and tree-shaking issues.

### Usage

```bash
python3 bundle_analyzer.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Target path to analyze (build output or project root) |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Output

```
==================================================
REPORT
==================================================
Target: ./dist
Status: success
Findings: 5
==================================================
```

Identifies:
- Bundle size breakdown
- Largest dependencies
- Duplicate packages
- Tree-shaking opportunities

---

## component_generator.py

**Purpose:** Generates React, Vue, or Svelte component scaffolds with TypeScript support, tests, and Storybook stories.

### Usage

```bash
python3 component_generator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Component name or path |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output directory |

### Generated Files

- `ComponentName.tsx` - Main component file
- `ComponentName.test.tsx` - Unit tests
- `ComponentName.stories.tsx` - Storybook stories
- `index.ts` - Barrel export

---

## frontend_scaffolder.py

**Purpose:** Scaffolds complete frontend project structures based on chosen framework and configuration.

### Usage

```bash
python3 frontend_scaffolder.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Project name or path |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output directory |

### Scaffolds Include

- Project configuration (tsconfig, eslint, prettier)
- Component structure
- State management setup
- Routing configuration
- API client scaffolding

### Dependencies

All scripts require Python 3.8+ (stdlib only)
