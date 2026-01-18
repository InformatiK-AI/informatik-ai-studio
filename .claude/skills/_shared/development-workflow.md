<!-- mixin-version: 1.0.0 -->
<!-- mixin-id: development-workflow -->
<!-- last-updated: 2026-01-17 -->

## Development Workflow

### 1. Setup and Configuration

```bash
# Install dependencies
npm install
# or
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

### 2. Run Quality Checks

```bash
# Use the analyzer script
python scripts/{{ANALYZER_SCRIPT}} .

# Review recommendations
# Apply fixes
```

### 3. Implement Best Practices

Follow the patterns and practices documented in:
- `references/{{PATTERN_REFERENCE}}`
- `references/{{WORKFLOW_REFERENCE}}`
- `references/{{TECHNICAL_REFERENCE}}`
