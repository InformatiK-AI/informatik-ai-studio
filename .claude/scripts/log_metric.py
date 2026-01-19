#!/usr/bin/env python3
"""
Logs workflow metrics to .claude/logs/metrics.json

Usage:
    python3 log_metric.py --command flow-plan --status success \
        --feature "auth_system" --start-time 1234567890 --end-time 1234567899

Arguments:
    --command: The flow command name (flow-plan, flow-feature-build, etc.)
    --status: Task status (success, fail, escalated, aborted)
    --feature: Feature name being worked on
    --start-time: Unix timestamp when task started
    --end-time: Unix timestamp when task ended
    --agents-used: Comma-separated list of agents invoked (optional)
    --workflow: Workflow type TDD/RAD/Standard (optional)
    --iteration: Current iteration number (optional)
    --scope: Scope type feature/epic/project (optional)
    --plan-name: Plan name (optional)
    --issue-number: Issue number if created (optional)
    --vcs-tool: VCS tool used gh/glab (optional)
    --preflight-retries: Number of preflight retries (optional)
    --validation-status: Validation status PASS/WARNINGS/FAIL (optional)
    --warnings-count: Number of warnings (optional)
    --errors-count: Number of errors (optional)
"""
import argparse
import json
import os
from datetime import datetime
from pathlib import Path


def ensure_log_directory():
    """Ensure the log directory exists."""
    log_dir = Path(".claude/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def load_existing_metrics(log_file):
    """Load existing metrics or create new structure."""
    if log_file.exists():
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # If file is corrupted, start fresh
            pass
    return {"version": "1.0", "entries": []}


def calculate_duration(start_time, end_time):
    """Calculate duration in milliseconds."""
    if start_time and end_time:
        try:
            start = int(start_time)
            end = int(end_time)
            return (end - start) * 1000
        except (ValueError, TypeError):
            pass
    return None


def parse_list_arg(value):
    """Parse comma-separated list argument."""
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def log_metric(args):
    """Log a metric entry to the metrics file."""
    log_dir = ensure_log_directory()
    log_file = log_dir / "metrics.json"

    metrics = load_existing_metrics(log_file)

    # Create new entry
    entry = {
        "id": len(metrics["entries"]) + 1,
        "command": args.command,
        "status": args.status,
        "feature": args.feature or "",
        "start_time": args.start_time or "",
        "end_time": args.end_time or "",
        "duration_ms": calculate_duration(args.start_time, args.end_time),
        "agents_used": parse_list_arg(args.agents_used),
        "workflow": args.workflow or "",
        "iteration": args.iteration,
        "scope": args.scope or "",
        "plan_name": args.plan_name or "",
        "issue_number": args.issue_number or "",
        "vcs_tool": args.vcs_tool or "",
        "preflight_retries": args.preflight_retries,
        "validation_status": args.validation_status or "",
        "warnings_count": args.warnings_count,
        "errors_count": args.errors_count,
        "logged_at": datetime.now().isoformat()
    }

    # Remove None values for cleaner JSON
    entry = {k: v for k, v in entry.items() if v is not None and v != ""}

    metrics["entries"].append(entry)

    # Write updated metrics
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)

    print(f"Metric logged: {args.command} - {args.status}")


def main():
    parser = argparse.ArgumentParser(
        description="Log workflow metrics to .claude/logs/metrics.json"
    )

    # Required arguments
    parser.add_argument(
        "--command",
        required=True,
        help="The flow command name (e.g., flow-plan, flow-feature-build)"
    )
    parser.add_argument(
        "--status",
        required=True,
        choices=["success", "fail", "escalated", "aborted", "preflight_failed"],
        help="Task status"
    )

    # Optional arguments
    parser.add_argument("--feature", default="", help="Feature name")
    parser.add_argument("--start-time", default="", help="Unix timestamp when started")
    parser.add_argument("--end-time", default="", help="Unix timestamp when ended")
    parser.add_argument("--agents-used", default="", help="Comma-separated agent list")
    parser.add_argument("--workflow", default="", help="Workflow type (TDD/RAD/Standard)")
    parser.add_argument("--iteration", type=int, default=None, help="Iteration number")
    parser.add_argument("--scope", default="", help="Scope (feature/epic/project)")
    parser.add_argument("--plan-name", default="", help="Plan name")
    parser.add_argument("--issue-number", default="", help="Issue number if created")
    parser.add_argument("--vcs-tool", default="", help="VCS tool (gh/glab)")
    parser.add_argument("--preflight-retries", type=int, default=None, help="Preflight retry count")
    parser.add_argument("--validation-status", default="", help="Validation status")
    parser.add_argument("--warnings-count", type=int, default=None, help="Warnings count")
    parser.add_argument("--errors-count", type=int, default=None, help="Errors count")

    args = parser.parse_args()
    log_metric(args)


if __name__ == "__main__":
    main()
