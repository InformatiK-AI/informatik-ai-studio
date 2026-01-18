# Acceptance Validator Skill

## Overview

The **Acceptance Validator** is the project's quality gatekeeper, responsible for:
- Defining clear, testable Acceptance Criteria (AC) using Gherkin syntax
- Validating implementations against those criteria before merge

## Quick Start

### Define Acceptance Criteria (Planning Phase)
```
/acceptance-validator define user_authentication
```

This will:
1. Read the feature context and all related plans
2. Generate Gherkin scenarios covering happy paths, edge cases, and errors
3. Save to `.claude/docs/{feature}/acceptance_criteria.md`

### Validate Implementation (QA Phase)
```
/acceptance-validator validate user_authentication
```

This will:
1. Read `CLAUDE.md` to determine validation method (Playwright/API-Test/Manual)
2. Load the acceptance criteria file
3. Execute validation based on the method
4. Generate a detailed PASS/FAIL report

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Main skill definition with workflows and examples |
| `README.md` | This documentation file |
| `references/gherkin_best_practices.md` | Guide for writing quality Gherkin |
| `references/validation_patterns.md` | Patterns for each validation method |

## Validation Methods

The skill supports three validation approaches (configured in `CLAUDE.md`):

| Method | Use Case | Automation |
|--------|----------|------------|
| **Playwright** | Frontend/E2E testing | Full |
| **API-Test** | Backend/API testing | Full |
| **Manual-Only** | Complex UI/UX flows | Checklist |

## Output Locations

- **Acceptance Criteria:** `.claude/docs/{feature}/acceptance_criteria.md`
- **Validation Reports:** Posted inline to session or PR comments

## Related Skills & Agents

- `@test-strategy-planner` - Designs test strategy before AC definition
- `@implementation-test-engineer` - Writes actual test code
- `flow-qa-validate` - Orchestrates the QA validation phase

## Version

- **Version:** 1.0.0
- **Last Updated:** 2026-01-17
