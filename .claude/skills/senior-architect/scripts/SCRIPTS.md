# Scripts Documentation

This directory contains executable scripts for the **senior-architect** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `architecture_diagram_generator.py` | Generate architecture diagrams | Production |
| `dependency_analyzer.py` | Analyze project dependencies | Production |
| `project_architect.py` | Design project architecture | Production |

---

## architecture_diagram_generator.py

**Purpose:** Generates architecture diagrams from code analysis or configuration. Supports C4 model, component diagrams, and sequence diagrams.

### Usage

```bash
python3 architecture_diagram_generator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Project path or config file |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Diagram Types

- System context diagram
- Container diagram
- Component diagram
- Deployment diagram
- Sequence diagrams

### Output Formats

- Mermaid markdown
- PlantUML
- SVG/PNG (with external renderer)

---

## dependency_analyzer.py

**Purpose:** Analyzes project dependencies to identify circular dependencies, unused packages, and security vulnerabilities.

### Usage

```bash
python3 dependency_analyzer.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Project path to analyze |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Analysis Includes

- Dependency tree visualization
- Circular dependency detection
- Unused dependency identification
- Version conflict analysis
- Security vulnerability check

---

## project_architect.py

**Purpose:** Designs and validates project architecture patterns based on requirements and best practices.

### Usage

```bash
python3 project_architect.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Requirements file or project path |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Recommendations Include

- Architecture pattern selection
- Tech stack recommendations
- Scalability considerations
- Security architecture
- Data flow design

### Dependencies

All scripts require Python 3.8+ (stdlib only)
