# Claude.md Architect Skill

A comprehensive skill for designing, creating, and maintaining future-proof CLAUDE.md files that serve as project "Constitutions."

## What This Skill Does

This skill enables Claude to:

- Bootstrap new projects with complete CLAUDE.md files
- Audit and improve existing CLAUDE.md files
- Apply Factory Verticals (standard tech stacks) consistently
- Ensure best practices for project documentation
- Define agent coordination and responsibilities

## When This Skill Triggers

Claude will automatically use this skill when you:

- Ask to create a new CLAUDE.md file
- Request help bootstrapping a new project
- Want to audit or improve an existing CLAUDE.md
- Need to modernize legacy project documentation
- Ask about project documentation standards

## Key Features

### Factory Verticals

The skill includes three proven, pre-configured tech stacks:

- **Vertical A**: Astro + React + Tailwind (static/hybrid sites)
- **Vertical B**: Next.js + Supabase (full-stack apps)
- **Vertical C**: Python + AI SDK (AI/ML projects)

See `references/factory-verticals.md` for detailed specifications.

### Comprehensive Template

Includes a complete CLAUDE.md template covering:

- Project metadata and objectives
- Technology stack and architecture
- Core team structure (agents and roles)
- Directory structure and file organization
- Environment variables and configuration
- Development workflow and git practices
- Code standards and testing requirements
- Deployment and release processes

See `references/claude-md-template.md` for the full template.

### Automated Validation

The skill now includes:

- **Quality Scoring**: 0-100 score based on length, completeness, redundancy, scannability
- **Redundancy Detection**: Flags duplicate commands/workflows across sections
- **Token Estimation**: Ensures CLAUDE.md consumes <5% of agent context budget
- **Validation Reports**: Detailed feedback before user approval

### Migration Support

Included migration guide for converting legacy documentation:

- Map README, ARCHITECTURE.md, CONTRIBUTING.md → CLAUDE.md sections
- Content transformation rules (consolidate, enrich, prune)
- Validation-first approach ensures quality output

See `references/migration-guide.md` for details.

## Example Usage

**Creating a new project:**

```
"Help me bootstrap a new SaaS project for task management with user authentication"
```

Claude will:

1. Recommend Next.js + Supabase (Vertical B)
2. Generate a complete CLAUDE.md with all sections
3. Define core team including security-architect and acceptance-validator
4. Present for your approval

**Auditing existing project:**

```
"Can you review and improve our CLAUDE.md?"
```

Claude will:

1. Read the current CLAUDE.md
2. Identify gaps and outdated information
3. Compare against best practices
4. Propose specific improvements
5. Generate an updated version

## Installation

This skill should be installed in your project:

```bash
# Copy skill to project .claude directory
cp -r claude-md-architect .claude/skills/

# Restart Claude Code to load the skill
```

Or for personal use across all projects:

```bash
# Copy to personal Claude directory
cp -r claude-md-architect ~/.claude/skills/

# Restart Claude Code
```

## Files Included

```
claude-md-architect/
├── SKILL.md                          # Main skill instructions
├── README.md                         # This file
├── references/
│   ├── factory-verticals.md         # Standard tech stack specifications
│   ├── claude-md-template.md        # Complete CLAUDE.md template
│   ├── claude-md-minimal.md         # Minimal template for new projects
│   ├── validation-checklist.md      # Quality validation framework
│   ├── migration-guide.md           # Legacy docs → CLAUDE.md migration
│   └── best-practices-examples.md   # Good vs bad examples
├── scripts/                          # Reserved for future automation
└── assets/                           # Reserved for example files
```

## Customization

### Adding Your Own Tech Stacks

Edit `references/factory-verticals.md` to add organization-specific stacks or update existing ones.

### Modifying the Template

Edit `references/claude-md-template.md` to match your organization's documentation standards.

### Extending the Skill

Add scripts to `scripts/` for:

- Automated CLAUDE.md validation
- Migration tools for legacy docs
- Project structure generators

## Best Practices

1. **Review Generated Files**: Always review Claude's CLAUDE.md before committing
2. **Keep Updated**: Update Factory Verticals as your tech stack evolves
3. **Team Alignment**: Share customizations across your team
4. **Iterate**: Improve the skill based on real usage patterns

## Version

**Version**: 2.1.0
**Created**: 2026-01-07
**Last Updated**: 2026-01-11

### Changelog

- **2.1.0** (2026-01-11): Optimization release
  - Reduced file length by 27% (618 → ~470 lines)
  - Consolidated redundant hooks-setup warnings (4 → 1 + reminders)
  - Replaced inline validation framework with reference to validation-checklist.md
  - Extracted verbose examples to best-practices-examples.md
  - Added Quick Decision Tree for faster workflow navigation
  - Added migration workflow reference
  - Quality score improved: 75/100 → 88/100
- **2.0.0** (2026-01-11): Added validation framework, quality scoring, migration guide, enhanced audit mode
- **1.0.0** (2026-01-07): Initial release

## Author

Created for future-proof project documentation and strategic planning.

## License

[Add your license here]
