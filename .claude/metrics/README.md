# Framework Metrics System

Usage analytics and telemetry for the InformatiK-AI-meth framework.

## Purpose

This metrics system provides visibility into:
1. **Skill Usage** - Which skills are invoked most frequently
2. **Agent Usage** - Agent invocation patterns and durations
3. **Workflow Metrics** - Flow command completion rates
4. **Bottleneck Detection** - Identify slow or failing components
5. **Usage Trends** - Track adoption over time

## Components

| File | Purpose |
|------|---------|
| `collector.py` | Collects and records metrics events |
| `storage.py` | SQLite storage layer |
| `dashboard.py` | CLI dashboard for viewing metrics |
| `exporter.py` | Export metrics to JSON/CSV |
| `metrics.db` | SQLite database (auto-created) |

## Quick Start

```bash
# View dashboard
python dashboard.py

# Export metrics
python exporter.py --format json --output metrics_report.json

# Clear old metrics (older than 30 days)
python storage.py --cleanup --days 30
```

## Metrics Collected

### Skill Metrics
- `skill.invoked` - Skill was invoked
- `skill.completed` - Skill completed successfully
- `skill.failed` - Skill failed with error
- `skill.duration` - Time taken to complete

### Agent Metrics
- `agent.invoked` - Agent was invoked
- `agent.completed` - Agent completed plan
- `agent.blocked` - Agent blocked by dependency
- `agent.duration` - Time taken to complete

### Workflow Metrics
- `flow.started` - Flow command started
- `flow.phase_completed` - Phase completed
- `flow.completed` - Flow completed successfully
- `flow.failed` - Flow failed

## Integration

### Recording Metrics (for skill/agent developers)

```python
from metrics.collector import MetricsCollector

collector = MetricsCollector()

# Record skill invocation
collector.record_skill_invocation("senior-backend", {
    "trigger": "user_request",
    "context": "api_development"
})

# Record completion with duration
collector.record_skill_completion("senior-backend", duration_ms=1500)
```

### Querying Metrics

```python
from metrics.storage import MetricsStorage

storage = MetricsStorage()

# Get top skills by usage
top_skills = storage.get_top_skills(limit=10)

# Get agent success rates
agent_stats = storage.get_agent_stats()

# Get daily trends
trends = storage.get_daily_trends(days=7)
```

## Privacy

- All metrics are stored **locally** in `metrics.db`
- No data is sent externally
- User can delete metrics at any time
- No PII is collected

## Schema

See `storage.py` for the complete database schema.
