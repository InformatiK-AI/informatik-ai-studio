#!/usr/bin/env python3
"""
Unified Plan Generator

Synthesizes multiple agent plans into a single unified implementation plan.
Integrates database, API, backend, frontend, and UI plans with execution order.

Usage:
    python3 generate_unified_plan.py --feature "user_auth" \
        --plans-dir ".claude/doc/user_auth/" \
        --output ".claude/doc/user_auth/implementation_plan.md"
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class UnifiedPlanGenerator:
    """Generates unified implementation plan from multiple agent plans."""

    def __init__(self, feature: str, plans_dir: Path):
        self.feature = feature
        self.plans_dir = plans_dir
        self.plans: Dict[str, str] = {}
        self.validation_result: Optional[Dict] = None
        self.execution_plan: Optional[Dict] = None

    def load_plans(self):
        """Load all available plan files."""
        plan_files = {
            "database": "database.md",
            "api_contract": "api_contract.md",
            "backend": "backend.md",
            "frontend": "frontend.md",
            "ui_components": "ui_components.md"
        }

        for plan_type, filename in plan_files.items():
            filepath = self.plans_dir / filename
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.plans[plan_type] = f.read()

    def run_validation(self) -> bool:
        """Run plan validation script."""
        validation_output = self.plans_dir / "validation_result.json"

        try:
            result = subprocess.run([
                sys.executable,
                str(Path(__file__).parent / "validate_plans.py"),
                "--feature", self.feature,
                "--plans-dir", str(self.plans_dir),
                "--output", str(validation_output)
            ], capture_output=True, text=True, check=True)

            # Load validation results
            if validation_output.exists():
                with open(validation_output, 'r') as f:
                    self.validation_result = json.load(f)

            return True

        except subprocess.CalledProcessError as e:
            print(f"Validation failed: {e}")
            return False

    def run_orchestration(self) -> bool:
        """Run orchestration script to get execution order."""
        orchestration_output = self.plans_dir / "execution_plan.json"

        try:
            result = subprocess.run([
                sys.executable,
                str(Path(__file__).parent / "orchestrate.py"),
                "--feature", self.feature,
                "--plans-dir", str(self.plans_dir),
                "--output", str(orchestration_output)
            ], capture_output=True, text=True, check=True)

            # Load execution plan
            if orchestration_output.exists():
                with open(orchestration_output, 'r') as f:
                    self.execution_plan = json.load(f)

            return True

        except subprocess.CalledProcessError as e:
            print(f"Orchestration failed: {e}")
            return False

    def generate_unified_plan(self) -> str:
        """Generate the unified implementation plan markdown."""
        lines = []

        # Header
        lines.append(f"# Unified Implementation Plan: {self.feature}")
        lines.append("")
        lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Feature**: {self.feature}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Table of Contents
        lines.append("## Table of Contents")
        lines.append("")
        lines.append("1. [Validation Status](#validation-status)")
        lines.append("2. [Execution Order](#execution-order)")
        lines.append("3. [File Changes Summary](#file-changes-summary)")
        lines.append("4. [Cross-Layer Integration](#cross-layer-integration)")
        lines.append("5. [Test Strategy](#test-strategy)")
        lines.append("6. [Implementation Checkpoints](#implementation-checkpoints)")
        lines.append("7. [Detailed Plans](#detailed-plans)")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Section 1: Validation Status
        lines.append("## Validation Status")
        lines.append("")

        if self.validation_result:
            status = self.validation_result.get("status", "UNKNOWN")
            error_count = self.validation_result.get("error_count", 0)
            warning_count = self.validation_result.get("warning_count", 0)

            if status == "PASS":
                lines.append("✅ **Status**: PASS")
                lines.append("")
                lines.append("All plans are coherent and ready for implementation.")
            elif status == "WARNINGS":
                lines.append(f"⚠️ **Status**: WARNINGS ({warning_count} warning(s))")
                lines.append("")
                lines.append("Plans have warnings. Review recommended before implementation:")
                lines.append("")
                for warning in self.validation_result.get("warnings", []):
                    lines.append(f"- **[{warning['category']}]** {warning['message']}")
                    lines.append(f"  - Source: `{warning['source_file']}`")
                    if warning.get('target_file'):
                        lines.append(f"  - Target: `{warning['target_file']}`")
            else:  # FAIL
                lines.append(f"❌ **Status**: FAIL ({error_count} error(s))")
                lines.append("")
                lines.append("Critical errors detected. Cannot proceed with implementation:")
                lines.append("")
                for error in self.validation_result.get("errors", []):
                    lines.append(f"- **[{error['category']}]** {error['message']}")
                    lines.append(f"  - Source: `{error['source_file']}`")
                    if error.get('target_file'):
                        lines.append(f"  - Target: `{error['target_file']}`")
        else:
            lines.append("⚠️ Validation not run")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Section 2: Execution Order
        lines.append("## Execution Order")
        lines.append("")
        lines.append("Implementation should follow this dependency-ordered sequence:")
        lines.append("")

        if self.execution_plan and "steps" in self.execution_plan:
            for step in self.execution_plan["steps"]:
                step_num = step["step_number"]
                agent = step["agent"]
                desc = step["description"]
                deps = step.get("dependencies", [])

                lines.append(f"### Step {step_num}: {agent}")
                lines.append("")
                lines.append(f"**Description**: {desc}")
                lines.append("")
                lines.append(f"**Plan File**: `{step['plan_file']}`")
                lines.append("")

                if deps:
                    lines.append(f"**Dependencies**: {', '.join(deps)}")
                else:
                    lines.append("**Dependencies**: None")

                lines.append("")
                lines.append(f"**Checkpoint**: {step['checkpoint']}")
                lines.append("")
        else:
            lines.append("No execution plan available.")
            lines.append("")

        lines.append("---")
        lines.append("")

        # Section 3: File Changes Summary
        lines.append("## File Changes Summary")
        lines.append("")
        lines.append("Estimated files to create or modify:")
        lines.append("")

        # Extract file references from all plans
        file_changes = self._extract_file_changes()

        for category, files in file_changes.items():
            if files:
                lines.append(f"### {category}")
                lines.append("")
                for file in sorted(files):
                    lines.append(f"- `{file}`")
                lines.append("")

        lines.append("---")
        lines.append("")

        # Section 4: Cross-Layer Integration
        lines.append("## Cross-Layer Integration")
        lines.append("")
        lines.append("Key integration points between architectural layers:")
        lines.append("")

        if "database" in self.plans and "api_contract" in self.plans:
            lines.append("### Database ↔ API Contract")
            lines.append("")
            lines.append("- Database schemas map to API request/response models")
            lines.append("- Field naming conventions should align (snake_case in DB, camelCase in API)")
            lines.append("- Data type compatibility validated")
            lines.append("")

        if "api_contract" in self.plans and "backend" in self.plans:
            lines.append("### API Contract ↔ Backend")
            lines.append("")
            lines.append("- Each API endpoint has corresponding backend handler")
            lines.append("- Request/response schemas match backend data transformations")
            lines.append("- Error codes defined in API are handled in backend")
            lines.append("")

        if "backend" in self.plans and "frontend" in self.plans:
            lines.append("### Backend ↔ Frontend")
            lines.append("")
            lines.append("- Frontend API client calls match backend endpoints")
            lines.append("- State management aligns with API response structures")
            lines.append("- Error handling covers all API error responses")
            lines.append("")

        if "frontend" in self.plans and "ui_components" in self.plans:
            lines.append("### Frontend ↔ UI Components")
            lines.append("")
            lines.append("- All UI components referenced in frontend are defined")
            lines.append("- Component props match frontend data structures")
            lines.append("- Design system conventions are consistent")
            lines.append("")

        lines.append("---")
        lines.append("")

        # Section 5: Test Strategy
        lines.append("## Test Strategy")
        lines.append("")
        lines.append("Comprehensive testing approach across all layers:")
        lines.append("")

        test_strategy = {
            "database": [
                "Run migrations on test database",
                "Verify schema integrity",
                "Test database constraints and indexes"
            ],
            "api_contract": [
                "Validate OpenAPI/GraphQL schema syntax",
                "Run contract tests (Pact, Postman)",
                "Test API documentation accuracy"
            ],
            "backend": [
                "Unit tests for business logic",
                "Integration tests for API endpoints",
                "Test error handling and edge cases"
            ],
            "frontend": [
                "Integration tests for API calls",
                "State management tests",
                "End-to-end tests (Playwright/Cypress)"
            ],
            "ui_components": [
                "Component unit tests",
                "Visual regression tests",
                "Accessibility tests (WCAG compliance)"
            ]
        }

        for layer, tests in test_strategy.items():
            if layer in self.plans:
                layer_name = layer.replace("_", " ").title()
                lines.append(f"### {layer_name} Tests")
                lines.append("")
                for test in tests:
                    lines.append(f"- {test}")
                lines.append("")

        lines.append("---")
        lines.append("")

        # Section 6: Implementation Checkpoints
        lines.append("## Implementation Checkpoints")
        lines.append("")
        lines.append("Verify these checkpoints after each implementation step:")
        lines.append("")

        if self.execution_plan and "steps" in self.execution_plan:
            for step in self.execution_plan["steps"]:
                step_num = step["step_number"]
                checkpoint = step["checkpoint"]
                lines.append(f"{step_num}. **After {step['agent']}**: {checkpoint}")

        lines.append("")
        lines.append("---")
        lines.append("")

        # Section 7: Detailed Plans
        lines.append("## Detailed Plans")
        lines.append("")
        lines.append("Full agent plans for reference:")
        lines.append("")

        for plan_type, content in self.plans.items():
            plan_name = plan_type.replace("_", " ").title()
            lines.append(f"### {plan_name}")
            lines.append("")
            lines.append(f"See: `.claude/doc/{self.feature}/{plan_type}.md`")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append(f"**End of Unified Implementation Plan for {self.feature}**")

        return "\n".join(lines)

    def _extract_file_changes(self) -> Dict[str, List[str]]:
        """Extract file references from all plans."""
        file_changes = {
            "Database Migrations": [],
            "Backend Files": [],
            "Frontend Files": [],
            "UI Components": [],
            "Tests": [],
            "Configuration": []
        }

        # Simple pattern matching to extract file references
        # This is a basic implementation - can be enhanced with more sophisticated parsing

        for plan_type, content in self.plans.items():
            # Look for file paths in backticks or code blocks
            import re
            file_pattern = r'`([a-zA-Z0-9_/\-\.]+\.(ts|js|tsx|jsx|py|sql|yml|yaml|json|md))`'
            matches = re.findall(file_pattern, content)

            for file_path, ext in matches:
                if "migration" in file_path.lower() or ext == "sql":
                    file_changes["Database Migrations"].append(file_path)
                elif "test" in file_path.lower() or "spec" in file_path.lower():
                    file_changes["Tests"].append(file_path)
                elif "component" in file_path.lower() or plan_type == "ui_components":
                    file_changes["UI Components"].append(file_path)
                elif ext in ["yml", "yaml", "json"] and "config" in file_path.lower():
                    file_changes["Configuration"].append(file_path)
                elif plan_type in ["backend", "domain_logic"]:
                    file_changes["Backend Files"].append(file_path)
                elif plan_type in ["frontend", "presentation"]:
                    file_changes["Frontend Files"].append(file_path)

        # Remove duplicates
        for category in file_changes:
            file_changes[category] = list(set(file_changes[category]))

        return file_changes


def main():
    parser = argparse.ArgumentParser(description="Generate unified implementation plan")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--plans-dir", required=True, help="Directory containing plan files")
    parser.add_argument("--output", required=True, help="Output file for unified plan")

    args = parser.parse_args()

    plans_dir = Path(args.plans_dir)
    if not plans_dir.exists():
        print(f"Error: Plans directory not found: {plans_dir}")
        return 1

    # Generate unified plan
    generator = UnifiedPlanGenerator(args.feature, plans_dir)

    print("Loading agent plans...")
    generator.load_plans()

    print("Running validation...")
    generator.run_validation()

    print("Running orchestration...")
    generator.run_orchestration()

    print("Generating unified plan...")
    unified_plan = generator.generate_unified_plan()

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(unified_plan)

    print(f"\n✅ Unified implementation plan generated: {output_path}")

    return 0


if __name__ == "__main__":
    exit(main())
