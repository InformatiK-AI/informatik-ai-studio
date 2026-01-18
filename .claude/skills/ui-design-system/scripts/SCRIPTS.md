# Scripts Documentation

This directory contains executable scripts for the **ui-design-system** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `design_token_generator.py` | Generate design tokens | Production |

---

## design_token_generator.py

**Purpose:** Generates design tokens from Figma, Sketch, or manual configuration. Outputs CSS variables, SCSS, or JavaScript/TypeScript formats.

### Usage

```bash
python3 design_token_generator.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Design file or token config |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Token Categories

- Colors (primary, secondary, semantic)
- Typography (font families, sizes, weights)
- Spacing (margin, padding scales)
- Borders (radius, width)
- Shadows
- Breakpoints
- Z-index

### Output Formats

```css
/* CSS Variables */
:root {
  --color-primary: #007bff;
  --spacing-sm: 8px;
  --font-size-base: 16px;
}
```

```javascript
// JavaScript/TypeScript
export const tokens = {
  color: { primary: '#007bff' },
  spacing: { sm: '8px' },
  fontSize: { base: '16px' }
};
```

### Dependencies

Python 3.8+ (stdlib only)
