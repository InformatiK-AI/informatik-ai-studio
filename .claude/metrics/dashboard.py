#!/usr/bin/env python3
"""
CLI Dashboard for framework metrics visualization.

Usage:
    python dashboard.py              # Show full dashboard
    python dashboard.py --skills     # Skills only
    python dashboard.py --agents     # Agents only
    python dashboard.py --flows      # Flows only
    python dashboard.py --bottlenecks # Show bottlenecks
    python dashboard.py --failures   # Show failure rates
    python dashboard.py --trends     # Show daily trends
"""

import argparse
from datetime import datetime
from typing import List, Dict

from .storage import MetricsStorage


class MetricsDashboard:
    """CLI dashboard for metrics visualization."""

    def __init__(self, storage: MetricsStorage = None):
        self.storage = storage or MetricsStorage()

    def render_header(self, title: str):
        """Render section header."""
        width = 60
        print()
        print("=" * width)
        print(f"  {title}")
        print("=" * width)

    def render_table(self, headers: List[str], rows: List[List], widths: List[int] = None):
        """Render a simple ASCII table."""
        if not rows:
            print("  No data available")
            return

        # Calculate widths
        if widths is None:
            widths = [max(len(str(h)), max(len(str(r[i])) for r in rows)) + 2
                      for i, h in enumerate(headers)]

        # Header
        header_line = "  " + "".join(h.ljust(w) for h, w in zip(headers, widths))
        print(header_line)
        print("  " + "-" * sum(widths))

        # Rows
        for row in rows:
            row_line = "  " + "".join(str(c).ljust(w) for c, w in zip(row, widths))
            print(row_line)

    def render_bar(self, value: float, max_value: float, width: int = 20) -> str:
        """Render a simple bar chart."""
        if max_value == 0:
            return "[" + " " * width + "]"
        filled = int((value / max_value) * width)
        return "[" + "█" * filled + " " * (width - filled) + "]"

    def show_skills(self, days: int = 30, limit: int = 10):
        """Show top skills."""
        self.render_header(f"TOP SKILLS (Last {days} days)")

        skills = self.storage.get_top_skills(limit=limit, days=days)
        if not skills:
            print("  No skill usage data")
            return

        max_invocations = max(s['invocations'] for s in skills)

        headers = ["Skill", "Invocations", "Success", "Failed", "Avg Time", ""]
        rows = []
        for s in skills:
            success_rate = (s['completions'] / s['invocations'] * 100) if s['invocations'] > 0 else 0
            avg_time = f"{int(s['avg_duration_ms'] or 0)}ms"
            bar = self.render_bar(s['invocations'], max_invocations, 15)
            rows.append([
                s['skill_name'],
                str(s['invocations']),
                f"{success_rate:.0f}%",
                str(s['failures']),
                avg_time,
                bar
            ])

        self.render_table(headers, rows, [25, 12, 10, 8, 10, 17])

    def show_agents(self, days: int = 30, limit: int = 10):
        """Show top agents."""
        self.render_header(f"TOP AGENTS (Last {days} days)")

        agents = self.storage.get_top_agents(limit=limit, days=days)
        if not agents:
            print("  No agent usage data")
            return

        max_invocations = max(a['invocations'] for a in agents)

        headers = ["Agent", "Invocations", "Completed", "Blocked", "Failed", ""]
        rows = []
        for a in agents:
            bar = self.render_bar(a['invocations'], max_invocations, 15)
            rows.append([
                a['agent_name'],
                str(a['invocations']),
                str(a['completions']),
                str(a['blocked']),
                str(a['failures']),
                bar
            ])

        self.render_table(headers, rows, [25, 12, 10, 10, 8, 17])

    def show_flows(self, days: int = 30):
        """Show flow statistics."""
        self.render_header(f"FLOW COMMANDS (Last {days} days)")

        flows = self.storage.get_flow_stats(days=days)
        if not flows:
            print("  No flow usage data")
            return

        headers = ["Flow", "Started", "Completed", "Failed", "Success Rate", "Avg Time"]
        rows = []
        for f in flows:
            success_rate = (f['completions'] / f['invocations'] * 100) if f['invocations'] > 0 else 0
            avg_time = f"{int(f['avg_duration_ms'] or 0)}ms"
            rows.append([
                f['flow_name'],
                str(f['invocations']),
                str(f['completions']),
                str(f['failures']),
                f"{success_rate:.1f}%",
                avg_time
            ])

        self.render_table(headers, rows)

    def show_trends(self, days: int = 7):
        """Show daily trends."""
        self.render_header(f"DAILY TRENDS (Last {days} days)")

        trends = self.storage.get_daily_trends(days=days)
        if not trends:
            print("  No trend data")
            return

        max_events = max(t['total_events'] for t in trends) if trends else 1

        headers = ["Date", "Events", "Invocations", "Completions", "Failures", "Activity"]
        rows = []
        for t in trends:
            bar = self.render_bar(t['total_events'], max_events, 20)
            rows.append([
                t['date'],
                str(t['total_events']),
                str(t['invocations']),
                str(t['completions']),
                str(t['failures']),
                bar
            ])

        self.render_table(headers, rows, [12, 8, 12, 12, 10, 22])

    def show_bottlenecks(self, threshold_ms: int = 5000, days: int = 7):
        """Show potential bottlenecks."""
        self.render_header(f"BOTTLENECKS (>{threshold_ms}ms avg, last {days} days)")

        bottlenecks = self.storage.get_bottlenecks(threshold_ms=threshold_ms, days=days)
        if not bottlenecks:
            print("  No bottlenecks detected (great!)")
            return

        headers = ["Type", "Name", "Avg Time", "Max Time", "Occurrences"]
        rows = []
        for b in bottlenecks:
            rows.append([
                b['type'].upper(),
                b['name'],
                f"{int(b['avg_duration_ms'])}ms",
                f"{int(b['max_duration_ms'])}ms",
                str(b['occurrences'])
            ])

        self.render_table(headers, rows)

    def show_failures(self, days: int = 7):
        """Show failure rates."""
        self.render_header(f"FAILURE RATES (Last {days} days)")

        failures = self.storage.get_failure_rates(days=days)
        if not failures:
            print("  No failures recorded (excellent!)")
            return

        headers = ["Type", "Name", "Total", "Failures", "Failure Rate"]
        rows = []
        for f in failures:
            rows.append([
                f['type'].upper(),
                f['name'],
                str(f['total']),
                str(f['failures']),
                f"{f['failure_rate']}%"
            ])

        self.render_table(headers, rows)

    def show_summary(self):
        """Show database summary."""
        self.render_header("DATABASE SUMMARY")

        stats = self.storage.get_database_stats()
        print(f"  Skill Events:  {stats.get('skill_events', 0):,}")
        print(f"  Agent Events:  {stats.get('agent_events', 0):,}")
        print(f"  Flow Events:   {stats.get('flow_events', 0):,}")
        print(f"  Sessions:      {stats.get('sessions', 0):,}")
        if 'db_size_bytes' in stats:
            size_kb = stats['db_size_bytes'] / 1024
            print(f"  Database Size: {size_kb:.1f} KB")

    def show_full_dashboard(self, days: int = 30):
        """Show the full dashboard."""
        print()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║         INFORMATIK-AI-METH METRICS DASHBOARD               ║")
        print("║                                                            ║")
        print(f"║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^44} ║")
        print("╚════════════════════════════════════════════════════════════╝")

        self.show_summary()
        self.show_skills(days=days, limit=10)
        self.show_agents(days=days, limit=10)
        self.show_flows(days=days)
        self.show_trends(days=7)
        self.show_bottlenecks(days=7)
        self.show_failures(days=7)

        print()
        print("=" * 60)
        print("  Dashboard complete. Use --help for more options.")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Metrics Dashboard")
    parser.add_argument("--days", type=int, default=30, help="Days to analyze")
    parser.add_argument("--skills", action="store_true", help="Show skills only")
    parser.add_argument("--agents", action="store_true", help="Show agents only")
    parser.add_argument("--flows", action="store_true", help="Show flows only")
    parser.add_argument("--trends", action="store_true", help="Show trends only")
    parser.add_argument("--bottlenecks", action="store_true", help="Show bottlenecks")
    parser.add_argument("--failures", action="store_true", help="Show failures")
    parser.add_argument("--summary", action="store_true", help="Show summary only")
    args = parser.parse_args()

    dashboard = MetricsDashboard()

    # Specific views
    if args.skills:
        dashboard.show_skills(days=args.days)
    elif args.agents:
        dashboard.show_agents(days=args.days)
    elif args.flows:
        dashboard.show_flows(days=args.days)
    elif args.trends:
        dashboard.show_trends(days=args.days)
    elif args.bottlenecks:
        dashboard.show_bottlenecks(days=args.days)
    elif args.failures:
        dashboard.show_failures(days=args.days)
    elif args.summary:
        dashboard.show_summary()
    else:
        # Full dashboard
        dashboard.show_full_dashboard(days=args.days)


if __name__ == "__main__":
    main()
