# Scripts Documentation

This directory contains executable scripts for the **senior-security** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `security_auditor.py` | Audit codebase for security issues | Production |
| `threat_modeler.py` | Generate threat models | Production |
| `pentest_automator.py` | Automate penetration testing tasks | Production |

---

## security_auditor.py

**Purpose:** Audits codebase for security vulnerabilities, misconfigurations, and OWASP Top 10 issues.

### Usage

```bash
python3 security_auditor.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Code path to audit |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Security Checks

- SQL injection patterns
- XSS vulnerabilities
- CSRF protection
- Authentication weaknesses
- Secrets in code
- Dependency vulnerabilities

---

## threat_modeler.py

**Purpose:** Generates threat models based on system architecture using STRIDE or PASTA methodologies.

### Usage

```bash
python3 threat_modeler.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Architecture diagram or config |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Methodologies

- STRIDE (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation)
- PASTA (Process for Attack Simulation and Threat Analysis)
- Attack trees

---

## pentest_automator.py

**Purpose:** Automates common penetration testing tasks for authorized security assessments.

### Usage

```bash
python3 pentest_automator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Target URL or config |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Automated Tests

- Port scanning
- Service enumeration
- Web vulnerability scanning
- SSL/TLS analysis

**Note:** Only use on systems you have authorization to test.

### Dependencies

All scripts require Python 3.8+ (stdlib only)
