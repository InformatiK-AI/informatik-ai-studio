"""
Framework Metrics System.

Provides usage analytics and telemetry for skills, agents, and flows.

Quick Start:
    from metrics import get_collector

    collector = get_collector()
    collector.record_skill_invocation("senior-backend")

    # Or with context manager
    with collector.track_skill("senior-backend") as tracker:
        # ... skill execution ...
        pass
"""

from .storage import MetricsStorage
from .collector import MetricsCollector, get_collector
from .dashboard import MetricsDashboard
from .exporter import MetricsExporter

__all__ = [
    "MetricsStorage",
    "MetricsCollector",
    "MetricsDashboard",
    "MetricsExporter",
    "get_collector",
]

__version__ = "1.0.0"
