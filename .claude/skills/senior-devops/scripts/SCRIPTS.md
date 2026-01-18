# Scripts Documentation

This directory contains executable scripts for the **senior-devops** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `pipeline_generator.py` | Generate CI/CD pipeline configurations | Production |
| `terraform_scaffolder.py` | Scaffold Terraform infrastructure | Production |
| `deployment_manager.py` | Manage deployment workflows | Production |

---

## pipeline_generator.py

**Purpose:** Generates CI/CD pipeline configurations for GitHub Actions, GitLab CI, Jenkins, and other platforms.

### Usage

```bash
python3 pipeline_generator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Project path or pipeline type |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Supported Platforms

- GitHub Actions (.github/workflows/)
- GitLab CI (.gitlab-ci.yml)
- Jenkins (Jenkinsfile)
- CircleCI (.circleci/config.yml)

### Pipeline Stages

- Build, Test, Lint
- Security scanning
- Container build
- Deployment (staging, production)

---

## terraform_scaffolder.py

**Purpose:** Scaffolds Terraform infrastructure as code configurations for various cloud providers.

### Usage

```bash
python3 terraform_scaffolder.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Infrastructure type or cloud provider |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output directory |

### Generated Structure

```
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
└── modules/
```

---

## deployment_manager.py

**Purpose:** Manages deployment workflows including rollbacks, blue-green deployments, and canary releases.

### Usage

```bash
python3 deployment_manager.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Deployment config or environment |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Supported Strategies

- Rolling deployment
- Blue-green deployment
- Canary release
- Rollback automation

### Dependencies

All scripts require Python 3.8+ (stdlib only)
