# Scripts Documentation

This directory contains executable scripts for the **skill-creator** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `init_skill.py` | Initialize a new skill from template | Production |
| `quick_validate.py` | Validate skill structure and frontmatter | Production |
| `package_skill.py` | Package skill into distributable zip | Production |

---

## init_skill.py

**Purpose:** Creates a new skill directory with template SKILL.md and example resource directories (scripts/, references/, assets/).

### Usage

```bash
python3 init_skill.py <skill-name> --path <path>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `skill-name` | Yes | Hyphen-case identifier (e.g., "data-analyzer") |
| `--path` | Yes | Directory where skill folder will be created |

### Skill Name Requirements

- Hyphen-case format (lowercase letters, digits, hyphens)
- Maximum 40 characters
- Must match directory name exactly
- Cannot start/end with hyphen or have consecutive hyphens

### Output

Creates the following structure:
```
<path>/<skill-name>/
├── SKILL.md              # Main skill file with TODOs
├── scripts/
│   └── example.py        # Example executable script
├── references/
│   └── api_reference.md  # Example reference doc
└── assets/
    └── example_asset.txt # Example asset placeholder
```

### Example

```bash
# Create skill in skills directory
python3 init_skill.py my-api-helper --path .claude/skills

# Create skill in custom location
python3 init_skill.py data-processor --path /projects/custom-skills
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Skill created successfully |
| `1` | Error (directory exists, invalid name, etc.) |

---

## quick_validate.py

**Purpose:** Validates a skill's structure and YAML frontmatter. Checks for required fields, naming conventions, and formatting rules.

### Usage

```bash
python3 quick_validate.py <skill_directory>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `skill_directory` | Yes | Path to the skill directory to validate |

### Validation Checks

1. **SKILL.md Existence** - File must exist in skill directory
2. **YAML Frontmatter** - Must start with `---` delimiter
3. **Required Fields:**
   - `name:` - Must be present
   - `description:` - Must be present
4. **Name Format:**
   - Must be hyphen-case (lowercase, digits, hyphens)
   - Cannot start/end with hyphen
   - Cannot have consecutive hyphens
5. **Description Format:**
   - Cannot contain angle brackets (`<` or `>`)

### Output

```
Skill is valid!
```
or
```
Missing 'name' in frontmatter
```

### Example

```bash
# Validate a skill
python3 quick_validate.py .claude/skills/my-skill

# Use in CI pipeline
python3 quick_validate.py ./skills/new-feature || exit 1
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Skill is valid |
| `1` | Validation failed |

---

## package_skill.py

**Purpose:** Packages a validated skill into a distributable ZIP file. Runs validation before packaging.

### Usage

```bash
python3 package_skill.py <path/to/skill-folder> [output-directory]
```

### Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `skill-folder` | Yes | - | Path to the skill directory |
| `output-directory` | No | Current dir | Where to save the ZIP file |

### Process

1. Validates skill folder exists
2. Checks SKILL.md is present
3. Runs `quick_validate.py` validation
4. Creates ZIP with skill directory structure preserved

### Output

Creates `<skill-name>.zip` containing the full skill directory.

```
📦 Packaging skill: .claude/skills/my-skill

🔍 Validating skill...
✅ Skill is valid!

  Added: my-skill/SKILL.md
  Added: my-skill/scripts/helper.py
  Added: my-skill/references/guide.md

✅ Successfully packaged skill to: ./my-skill.zip
```

### Example

```bash
# Package to current directory
python3 package_skill.py .claude/skills/my-skill

# Package to specific output directory
python3 package_skill.py .claude/skills/my-skill ./dist
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Skill packaged successfully |
| `1` | Error (validation failed, path not found, etc.) |

### Dependencies

- Requires `quick_validate.py` in same directory (imported as module)
- Python 3.8+ standard library only
