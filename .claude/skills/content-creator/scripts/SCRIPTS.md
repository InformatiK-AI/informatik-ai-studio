# Scripts Documentation

This directory contains executable scripts for the **content-creator** skill.

## Scripts Overview

| Script | Purpose | Status |
|--------|---------|--------|
| `brand_voice_analyzer.py` | Analyze and define brand voice | Production |
| `seo_optimizer.py` | Optimize content for SEO | Production |

---

## brand_voice_analyzer.py

**Purpose:** Analyzes existing content to extract brand voice characteristics and generates style guidelines.

### Usage

```bash
python3 brand_voice_analyzer.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Content samples or directory |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Analysis Includes

- Tone attributes (formal/casual, serious/playful)
- Vocabulary patterns
- Sentence structure
- Common phrases and expressions
- Reading level
- Personality traits

### Output

Generates brand voice guidelines with:
- Voice characteristics
- Do's and don'ts
- Example rewrites
- Word choice recommendations

---

## seo_optimizer.py

**Purpose:** Analyzes and optimizes content for search engine optimization including keywords, meta tags, and readability.

### Usage

```bash
python3 seo_optimizer.py <target> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `target` | Yes | Content file or URL |
| `--verbose`, `-v` | No | Enable verbose output |
| `--json` | No | Output results as JSON |
| `--output`, `-o` | No | Output file path |

### Optimization Checks

- Keyword density and placement
- Title tag optimization
- Meta description
- Header structure (H1, H2, H3)
- Internal/external links
- Image alt text
- Readability score
- Content length

### Output

Generates SEO report with:
- Current score
- Optimization suggestions
- Keyword recommendations
- Competitor comparison (if provided)

### Dependencies

All scripts require Python 3.8+ (stdlib only)
