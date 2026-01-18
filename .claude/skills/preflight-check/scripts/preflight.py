#!/usr/bin/env python3
"""
Pre-Flight Checker

Validates project readiness before starting feature implementation.
Checks context files, agent availability, CLAUDE.md, git status, dependencies, and tools.

Usage:
    python3 preflight.py --feature "user_auth" --output "preflight_report.json"
"""

import argparse
import json
import os
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class CheckResult:
    """Result of a single pre-flight check."""
    check_name: str
    status: str  # "PASS", "WARNING", "FAIL"
    message: str
    fix_suggestion: Optional[str] = None


@dataclass
class PreFlightReport:
    """Complete pre-flight check report."""
    feature: str
    overall_status: str  # "GO", "GO_WITH_WARNINGS", "NO_GO"
    checks: List[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> List[CheckResult]:
        return [c for c in self.checks if c.status == "PASS"]

    @property
    def warnings(self) -> List[CheckResult]:
        return [c for c in self.checks if c.status == "WARNING"]

    @property
    def failures(self) -> List[CheckResult]:
        return [c for c in self.checks if c.status == "FAIL"]

    def determine_overall_status(self):
        """Determine overall status based on check results."""
        if self.failures:
            self.overall_status = "NO_GO"
        elif self.warnings:
            self.overall_status = "GO_WITH_WARNINGS"
        else:
            self.overall_status = "GO"


class PreFlightChecker:
    """Runs comprehensive pre-flight checks."""

    def __init__(self, feature: str, project_root: Path):
        self.feature = feature
        self.project_root = project_root
        self.report = PreFlightReport(feature=feature, overall_status="GO")

    def run_all_checks(self):
        """Run all pre-flight checks."""
        self.check_context_file()
        self.check_agent_availability()
        self.check_claude_md()
        self.check_git_status()
        self.check_dependencies()
        self.check_test_framework()
        self.check_required_tools()

        # Determine overall status
        self.report.determine_overall_status()

    # Phase 1: Context Validation

    def check_context_file(self):
        """Check if feature context file exists and is valid."""
        context_patterns = [
            f"context_session_feature_{self.feature}.md",
            f"context_session_{self.feature}.md",
        ]

        sessions_dir = self.project_root / ".claude" / "sessions"
        context_file = None

        if sessions_dir.exists():
            for pattern in context_patterns:
                candidate = sessions_dir / pattern
                if candidate.exists():
                    context_file = candidate
                    break

        if not context_file:
            self.report.checks.append(CheckResult(
                check_name="Context File Existence",
                status="FAIL",
                message=f"Context file not found for feature '{self.feature}'",
                fix_suggestion=f"Run: flow-plan feature {self.feature}"
            ))
            return

        # Check if file is empty
        if context_file.stat().st_size == 0:
            self.report.checks.append(CheckResult(
                check_name="Context File Content",
                status="FAIL",
                message="Context file is empty",
                fix_suggestion="Re-run flow-plan to generate valid context"
            ))
            return

        # Check for required sections
        with open(context_file, 'r', encoding='utf-8') as f:
            content = f.read()

        required_sections = ["Overview", "Objectives"]
        missing_sections = [s for s in required_sections if s not in content]

        if missing_sections:
            self.report.checks.append(CheckResult(
                check_name="Context File Structure",
                status="WARNING",
                message=f"Missing sections: {', '.join(missing_sections)}",
                fix_suggestion="Update context file to include missing sections"
            ))
        else:
            self.report.checks.append(CheckResult(
                check_name="Context File",
                status="PASS",
                message=f"Context file exists and is valid: {context_file.name}"
            ))

        # Check for placeholder text
        placeholders = ["TODO", "TBD", "FIXME", "XXX"]
        found_placeholders = [p for p in placeholders if p in content]

        if found_placeholders:
            self.report.checks.append(CheckResult(
                check_name="Context Completeness",
                status="WARNING",
                message=f"Found placeholder text: {', '.join(found_placeholders)}",
                fix_suggestion="Complete context file before implementation"
            ))

    # Phase 2: Agent Availability

    def check_agent_availability(self):
        """Check if required agents are available."""
        agents_dir = self.project_root / ".claude" / "agents"

        if not agents_dir.exists():
            self.report.checks.append(CheckResult(
                check_name="Agents Directory",
                status="FAIL",
                message="Agents directory not found: .claude/agents/",
                fix_suggestion="Initialize Genesis Factory structure"
            ))
            return

        # Detect required agents from context (simplified heuristic)
        required_agents = self._detect_required_agents()

        missing_agents = []
        for agent in required_agents:
            agent_file = agents_dir / f"{agent}.md"
            if not agent_file.exists():
                missing_agents.append(agent)

        if missing_agents:
            self.report.checks.append(CheckResult(
                check_name="Agent Availability",
                status="FAIL" if len(missing_agents) > 2 else "WARNING",
                message=f"Missing agents: {', '.join(missing_agents)}",
                fix_suggestion="Invoke @agent-librarian to draft missing agents"
            ))
        else:
            self.report.checks.append(CheckResult(
                check_name="Agent Availability",
                status="PASS",
                message=f"All {len(required_agents)} required agents available"
            ))

    def _detect_required_agents(self) -> List[str]:
        """Detect required agents based on feature context (simplified)."""
        # Default agents for most features
        # Note: acceptance-validator is now a skill, not an agent
        return [
            "security-architect",
            "implementation-test-engineer"
        ]

    # Phase 3: CLAUDE.md Validation

    def check_claude_md(self):
        """Validate CLAUDE.md exists and has required sections."""
        claude_md = self.project_root / "CLAUDE.md"

        if not claude_md.exists():
            self.report.checks.append(CheckResult(
                check_name="CLAUDE.md Existence",
                status="FAIL",
                message="CLAUDE.md not found at project root",
                fix_suggestion="Run: flow-md-architect to create CLAUDE.md"
            ))
            return

        with open(claude_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check required sections
        required_sections = ["[stack]", "[methodology]", "[core_team]"]
        missing_sections = [s for s in required_sections if s not in content]

        if missing_sections:
            self.report.checks.append(CheckResult(
                check_name="CLAUDE.md Sections",
                status="FAIL",
                message=f"Missing sections: {', '.join(missing_sections)}",
                fix_suggestion="Update CLAUDE.md with missing sections"
            ))
            return

        # Check methodology workflow
        workflow_match = re.search(r'workflow[:\s]+(TDD|RAD|Standard)', content, re.IGNORECASE)
        if not workflow_match:
            self.report.checks.append(CheckResult(
                check_name="Methodology Workflow",
                status="WARNING",
                message="Workflow not set in [methodology] section",
                fix_suggestion="Set workflow to 'TDD', 'RAD', or 'Standard'"
            ))
        else:
            self.report.checks.append(CheckResult(
                check_name="CLAUDE.md Configuration",
                status="PASS",
                message=f"CLAUDE.md valid, workflow: {workflow_match.group(1)}"
            ))

    # Phase 4: Git Status

    def check_git_status(self):
        """Check git repository status."""
        try:
            # Check if in git repo
            result = subprocess.run(['git', 'rev-parse', '--git-dir'],
                                    cwd=self.project_root,
                                    capture_output=True,
                                    text=True,
                                    check=False)

            if result.returncode != 0:
                self.report.checks.append(CheckResult(
                    check_name="Git Repository",
                    status="WARNING",
                    message="Not in a git repository",
                    fix_suggestion="Initialize git: git init"
                ))
                return

            # Check for uncommitted changes
            status_result = subprocess.run(['git', 'status', '--porcelain'],
                                           cwd=self.project_root,
                                           capture_output=True,
                                           text=True,
                                           check=True)

            if status_result.stdout.strip():
                lines = status_result.stdout.strip().split('\n')
                self.report.checks.append(CheckResult(
                    check_name="Git Working Tree",
                    status="WARNING",
                    message=f"{len(lines)} uncommitted changes detected",
                    fix_suggestion="Commit or stash changes before implementation"
                ))
            else:
                self.report.checks.append(CheckResult(
                    check_name="Git Working Tree",
                    status="PASS",
                    message="Working tree is clean"
                ))

            # Check for merge conflicts
            if any('UU' in line or 'AA' in line for line in status_result.stdout.split('\n')):
                self.report.checks.append(CheckResult(
                    check_name="Git Merge Conflicts",
                    status="FAIL",
                    message="Merge conflicts detected",
                    fix_suggestion="Resolve conflicts: git merge --continue or --abort"
                ))

            # Check worktree existence
            worktree_path = self.project_root / ".trees" / f"feature-{self.feature}"
            if worktree_path.exists():
                self.report.checks.append(CheckResult(
                    check_name="Git Worktree",
                    status="FAIL",
                    message=f"Worktree already exists: {worktree_path}",
                    fix_suggestion="Delete worktree: git worktree remove .trees/feature-{self.feature}"
                ))

        except subprocess.CalledProcessError as e:
            self.report.checks.append(CheckResult(
                check_name="Git Status Check",
                status="WARNING",
                message=f"Git status check failed: {e}",
                fix_suggestion="Verify git is installed and repository is valid"
            ))

    # Phase 5: Dependency Check

    def check_dependencies(self):
        """Check if project dependencies are installed."""
        # Check Node.js dependencies
        package_json = self.project_root / "package.json"
        if package_json.exists():
            node_modules = self.project_root / "node_modules"
            if not node_modules.exists():
                self.report.checks.append(CheckResult(
                    check_name="Node.js Dependencies",
                    status="WARNING",
                    message="node_modules/ not found",
                    fix_suggestion="Run: npm install"
                ))
            else:
                self.report.checks.append(CheckResult(
                    check_name="Node.js Dependencies",
                    status="PASS",
                    message="node_modules/ exists"
                ))

        # Check Python dependencies
        requirements_txt = self.project_root / "requirements.txt"
        if requirements_txt.exists():
            # Check if virtual environment is activated (simplified)
            if not os.environ.get('VIRTUAL_ENV'):
                self.report.checks.append(CheckResult(
                    check_name="Python Dependencies",
                    status="WARNING",
                    message="Virtual environment not activated",
                    fix_suggestion="Activate venv: source venv/bin/activate"
                ))

    # Phase 6: Test Framework

    def check_test_framework(self):
        """Check if test framework is configured."""
        test_configs = [
            "jest.config.js",
            "jest.config.ts",
            "vitest.config.ts",
            "playwright.config.ts",
            "pytest.ini",
            "tox.ini"
        ]

        config_found = any((self.project_root / config).exists() for config in test_configs)

        if not config_found:
            self.report.checks.append(CheckResult(
                check_name="Test Framework",
                status="WARNING",
                message="No test configuration found",
                fix_suggestion="Configure test framework before implementation"
            ))
        else:
            self.report.checks.append(CheckResult(
                check_name="Test Framework",
                status="PASS",
                message="Test framework configured"
            ))

    # Phase 7: Required Tools

    def check_required_tools(self):
        """Check if required CLI tools are installed."""
        required_tools = {
            'git': 'git',
            'python3': 'python3 or python',
            'gh': 'GitHub CLI (gh)',
        }

        missing_tools = []
        for tool, description in required_tools.items():
            if not shutil.which(tool):
                missing_tools.append(description)

        if missing_tools:
            self.report.checks.append(CheckResult(
                check_name="Required Tools",
                status="FAIL" if 'git' in missing_tools else "WARNING",
                message=f"Missing tools: {', '.join(missing_tools)}",
                fix_suggestion="Install missing tools before proceeding"
            ))
        else:
            self.report.checks.append(CheckResult(
                check_name="Required Tools",
                status="PASS",
                message="All required CLI tools available"
            ))


def print_report(report: PreFlightReport):
    """Print formatted pre-flight report."""
    print("\n" + "="*60)
    print("PRE-FLIGHT CHECK REPORT")
    print("="*60)
    print(f"\nFeature: {report.feature}")
    print(f"\nOVERALL STATUS: {report.overall_status}\n")

    if report.passed:
        print(f"✅ PASS ({len(report.passed)}):")
        for check in report.passed:
            print(f"  - {check.message}")
        print()

    if report.warnings:
        print(f"⚠️  WARNING ({len(report.warnings)}):")
        for check in report.warnings:
            print(f"  - {check.message}")
            if check.fix_suggestion:
                print(f"    Fix: {check.fix_suggestion}")
        print()

    if report.failures:
        print(f"❌ FAIL ({len(report.failures)}):")
        for check in report.failures:
            print(f"  - {check.message}")
            if check.fix_suggestion:
                print(f"    Fix: {check.fix_suggestion}")
        print()

    # Recommendation
    if report.overall_status == "GO":
        print("RECOMMENDATION: ✅ All checks passed. Proceed with implementation.")
    elif report.overall_status == "GO_WITH_WARNINGS":
        print("RECOMMENDATION: ⚠️  Proceed with caution. Address warnings if possible.")
    else:
        print("RECOMMENDATION: ❌ Cannot proceed. Resolve critical errors first.")

    print("="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Pre-flight checker for feature implementation")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--output", help="Output file for JSON report")

    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    checker = PreFlightChecker(args.feature, project_root)

    print(f"Running pre-flight checks for feature: {args.feature}")
    checker.run_all_checks()

    # Print report
    print_report(checker.report)

    # Save JSON report if requested
    if args.output:
        report_dict = {
            "feature": checker.report.feature,
            "overall_status": checker.report.overall_status,
            "pass_count": len(checker.report.passed),
            "warning_count": len(checker.report.warnings),
            "fail_count": len(checker.report.failures),
            "checks": [
                {
                    "name": check.check_name,
                    "status": check.status,
                    "message": check.message,
                    "fix_suggestion": check.fix_suggestion
                }
                for check in checker.report.checks
            ]
        }

        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2)

        print(f"Report saved to: {args.output}")

    # Return exit code based on status
    return 0 if checker.report.overall_status != "NO_GO" else 1


if __name__ == "__main__":
    exit(main())
