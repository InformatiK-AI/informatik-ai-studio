# Skills Testing Suite

Automated test suite for validating skill structure, references, and integrity.

## Purpose

This test suite ensures that:
1. All skills follow the correct structure
2. References and script files exist
3. Mixins are correctly defined and used
4. No broken links or missing dependencies

## Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test
python test_skill_structure.py
python test_skill_references.py
python test_skill_scripts.py
python test_skill_mixins.py
```

## Test Coverage

| Test File | What It Validates |
|-----------|-------------------|
| `test_skill_structure.py` | SKILL.md frontmatter, required sections, markdown format |
| `test_skill_references.py` | All `references/*.md` files exist and are valid |
| `test_skill_scripts.py` | All `scripts/*.py` files exist and are syntactically correct |
| `test_skill_mixins.py` | Mixin files exist, versions match, placeholders defined |
| `test_manifest_integrity.py` | MANIFEST.json matches actual skill files |

## Adding New Tests

1. Create a new `test_*.py` file
2. Import from `test_utils.py`
3. Add test to `run_tests.py`

## Exit Codes

- `0`: All tests passed
- `1`: One or more tests failed
- `2`: Test configuration error
