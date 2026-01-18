#!/usr/bin/env python3
"""
Metrics exporter for generating reports.

Usage:
    python exporter.py --format json --output report.json
    python exporter.py --format csv --output report.csv
    python exporter.py --format markdown --output report.md
"""

import argparse
import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from .storage import MetricsStorage


class MetricsExporter:
    """Export metrics to various formats."""

    def __init__(self, storage: MetricsStorage = None):
        self.storage = storage or MetricsStorage()

    def gather_all_metrics(self, days: int = 30) -> Dict:
        """Gather all metrics into a single dict."""
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "period_days": days,
            "summary": self.storage.get_database_stats(),
            "top_skills": self.storage.get_top_skills(limit=20, days=days),
            "top_agents": self.storage.get_top_agents(limit=20, days=days),
            "flow_stats": self.storage.get_flow_stats(days=days),
            "daily_trends": self.storage.get_daily_trends(days=min(days, 30)),
            "bottlenecks": self.storage.get_bottlenecks(days=days),
            "failure_rates": self.storage.get_failure_rates(days=days)
        }

    def export_json(self, output_path: Path, days: int = 30):
        """Export metrics to JSON."""
        metrics = self.gather_all_metrics(days=days)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        print(f"Exported to {output_path}")

    def export_csv(self, output_path: Path, days: int = 30):
        """Export metrics to CSV (multiple files)."""
        metrics = self.gather_all_metrics(days=days)
        base_path = output_path.parent
        base_name = output_path.stem

        # Skills CSV
        skills_path = base_path / f"{base_name}_skills.csv"
        self._write_csv(skills_path, metrics["top_skills"])

        # Agents CSV
        agents_path = base_path / f"{base_name}_agents.csv"
        self._write_csv(agents_path, metrics["top_agents"])

        # Flows CSV
        flows_path = base_path / f"{base_name}_flows.csv"
        self._write_csv(flows_path, metrics["flow_stats"])

        # Trends CSV
        trends_path = base_path / f"{base_name}_trends.csv"
        self._write_csv(trends_path, metrics["daily_trends"])

        print(f"Exported CSV files to {base_path}/")

    def _write_csv(self, path: Path, data: List[Dict]):
        """Write data to CSV file."""
        if not data:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def export_markdown(self, output_path: Path, days: int = 30):
        """Export metrics to Markdown report."""
        metrics = self.gather_all_metrics(days=days)

        lines = [
            f"# Framework Metrics Report",
            f"",
            f"**Generated:** {metrics['generated_at']}",
            f"**Period:** Last {days} days",
            f"",
            f"## Summary",
            f"",
            f"| Metric | Value |",
            f"|--------|-------|",
        ]

        for key, value in metrics["summary"].items():
            lines.append(f"| {key} | {value:,} |")

        # Top Skills
        lines.extend([
            f"",
            f"## Top Skills",
            f"",
            f"| Skill | Invocations | Completions | Failures | Avg Duration |",
            f"|-------|-------------|-------------|----------|--------------|",
        ])
        for s in metrics["top_skills"][:10]:
            avg_ms = int(s['avg_duration_ms'] or 0)
            lines.append(f"| {s['skill_name']} | {s['invocations']} | {s['completions']} | {s['failures']} | {avg_ms}ms |")

        # Top Agents
        lines.extend([
            f"",
            f"## Top Agents",
            f"",
            f"| Agent | Invocations | Completions | Blocked | Failures |",
            f"|-------|-------------|-------------|---------|----------|",
        ])
        for a in metrics["top_agents"][:10]:
            lines.append(f"| {a['agent_name']} | {a['invocations']} | {a['completions']} | {a['blocked']} | {a['failures']} |")

        # Flow Stats
        lines.extend([
            f"",
            f"## Flow Commands",
            f"",
            f"| Flow | Invocations | Completions | Failures | Success Rate |",
            f"|------|-------------|-------------|----------|--------------|",
        ])
        for f in metrics["flow_stats"]:
            rate = (f['completions'] / f['invocations'] * 100) if f['invocations'] > 0 else 0
            lines.append(f"| {f['flow_name']} | {f['invocations']} | {f['completions']} | {f['failures']} | {rate:.1f}% |")

        # Bottlenecks
        if metrics["bottlenecks"]:
            lines.extend([
                f"",
                f"## Bottlenecks",
                f"",
                f"| Type | Name | Avg Duration | Max Duration |",
                f"|------|------|--------------|--------------|",
            ])
            for b in metrics["bottlenecks"]:
                lines.append(f"| {b['type']} | {b['name']} | {int(b['avg_duration_ms'])}ms | {int(b['max_duration_ms'])}ms |")

        # Failure Rates
        if metrics["failure_rates"]:
            lines.extend([
                f"",
                f"## Failure Rates",
                f"",
                f"| Type | Name | Total | Failures | Rate |",
                f"|------|------|-------|----------|------|",
            ])
            for f in metrics["failure_rates"]:
                lines.append(f"| {f['type']} | {f['name']} | {f['total']} | {f['failures']} | {f['failure_rate']}% |")

        # Daily Trends
        lines.extend([
            f"",
            f"## Daily Trends",
            f"",
            f"| Date | Total Events | Invocations | Completions | Failures |",
            f"|------|--------------|-------------|-------------|----------|",
        ])
        for t in metrics["daily_trends"]:
            lines.append(f"| {t['date']} | {t['total_events']} | {t['invocations']} | {t['completions']} | {t['failures']} |")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"Exported to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Export metrics")
    parser.add_argument("--format", choices=["json", "csv", "markdown", "md"],
                        default="json", help="Output format")
    parser.add_argument("--output", "-o", type=str, required=True,
                        help="Output file path")
    parser.add_argument("--days", type=int, default=30,
                        help="Days to include in report")
    args = parser.parse_args()

    exporter = MetricsExporter()
    output_path = Path(args.output)

    if args.format == "json":
        exporter.export_json(output_path, days=args.days)
    elif args.format == "csv":
        exporter.export_csv(output_path, days=args.days)
    elif args.format in ["markdown", "md"]:
        exporter.export_markdown(output_path, days=args.days)


if __name__ == "__main__":
    main()
