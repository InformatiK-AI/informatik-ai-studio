# Scripts Documentation

This directory contains executable scripts for the **ux-researcher-designer** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `persona_generator.py` | Generate user personas from data | Production |

---

## persona_generator.py

**Purpose:** Generates data-driven user personas from research data, analytics, and user interviews.

### Usage

```bash
python3 persona_generator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Research data or analytics export |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Persona Components

- Demographics
- Goals and motivations
- Pain points and frustrations
- Behaviors and patterns
- Technology proficiency
- Quote/voice of customer
- Journey touchpoints

### Input Formats

- Survey responses (CSV, JSON)
- Interview transcripts
- Analytics data
- Customer feedback

### Output

Generates structured persona documents with:
- Persona profile card
- User journey map
- Empathy map
- Opportunity areas

### Dependencies

Python 3.8+ (stdlib only)
