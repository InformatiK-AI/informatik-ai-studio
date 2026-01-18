# Semantic Skill Discovery

Natural language search for finding the right skills and agents.

## Purpose

Instead of memorizing 34+ skill names, users can describe what they need:
- "I need to optimize SQL queries" → `senior-backend`, `senior-data-engineer`
- "set up CI/CD pipeline" → `senior-devops`, `ci-cd-architect`
- "review my code for security issues" → `senior-security`, `code-reviewer`

## How It Works

1. **TF-IDF Indexing** - Skills are indexed by their descriptions, tags, and capabilities
2. **Query Matching** - User queries are matched against the index using cosine similarity
3. **Ranking** - Results are ranked by relevance score

## Usage

```python
from discovery import SkillDiscovery

discovery = SkillDiscovery()

# Find skills for a query
results = discovery.search("optimize database performance")
for result in results:
    print(f"{result['skill']}: {result['score']:.2f}")

# Output:
# senior-data-engineer: 0.85
# senior-backend: 0.72
# database-architect: 0.68
```

## CLI Usage

```bash
# Interactive search
python search.py "I need to build a REST API"

# With limit
python search.py "security audit" --limit 5

# Include agents
python search.py "database schema design" --include-agents
```

## Files

| File | Purpose |
|------|---------|
| `indexer.py` | Builds TF-IDF index from skills and agents |
| `search.py` | Search interface and CLI |
| `index.json` | Pre-built search index (auto-generated) |

## Updating the Index

The index is automatically rebuilt when:
- MANIFEST.json changes
- New skills are added
- `python indexer.py --rebuild` is run

## Search Tips

- Use natural language: "how do I set up authentication"
- Include technology names: "React performance optimization"
- Describe the task: "review pull request for bugs"
- Mention the domain: "data pipeline orchestration"
