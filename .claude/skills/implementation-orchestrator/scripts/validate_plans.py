#!/usr/bin/env python3
"""
Plan Coherence Validator

Validates consistency across multiple agent plans (database, API, backend, frontend, UI).
Detects mismatches in naming, types, schemas, and integration points.

Usage:
    python3 validate_plans.py --feature "user_auth" --plans-dir ".claude/doc/user_auth/"
"""

import argparse
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class ValidationIssue:
    """Represents a validation issue (warning or error)."""
    severity: str  # "warning" or "error"
    category: str  # "naming", "type", "schema", "integration"
    message: str
    source_file: str
    target_file: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class ValidationResult:
    """Results of plan validation."""
    status: str  # "PASS", "WARNINGS", "FAIL"
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == "warning"]


class PlanValidator:
    """Validates coherence across multiple agent plans."""

    def __init__(self, plans_dir: Path):
        self.plans_dir = plans_dir
        self.plans: Dict[str, str] = {}
        self._load_plans()

    def _load_plans(self):
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

    def validate(self) -> ValidationResult:
        """Run all validation checks."""
        result = ValidationResult(status="PASS")

        # Validate database ↔ API contract
        if "database" in self.plans and "api_contract" in self.plans:
            result.issues.extend(self._validate_db_api())

        # Validate API contract ↔ backend
        if "api_contract" in self.plans and "backend" in self.plans:
            result.issues.extend(self._validate_api_backend())

        # Validate backend ↔ frontend
        if "backend" in self.plans and "frontend" in self.plans:
            result.issues.extend(self._validate_backend_frontend())

        # Validate frontend ↔ UI components
        if "frontend" in self.plans and "ui_components" in self.plans:
            result.issues.extend(self._validate_frontend_ui())

        # Determine overall status
        if result.errors:
            result.status = "FAIL"
        elif result.warnings:
            result.status = "WARNINGS"
        else:
            result.status = "PASS"

        return result

    def _validate_db_api(self) -> List[ValidationIssue]:
        """Validate database schema against API contract."""
        issues = []

        # Extract database fields
        db_fields = self._extract_db_fields(self.plans["database"])

        # Extract API schemas
        api_fields = self._extract_api_fields(self.plans["api_contract"])

        # Check naming conventions
        for table, fields in db_fields.items():
            for field_name, field_type in fields.items():
                # Convert snake_case to camelCase for comparison
                camel_case = self._snake_to_camel(field_name)

                # Check if API uses this field
                for schema, api_schema_fields in api_fields.items():
                    if camel_case in api_schema_fields:
                        api_type = api_schema_fields[camel_case]

                        # Validate type compatibility
                        if not self._types_compatible(field_type, api_type):
                            issues.append(ValidationIssue(
                                severity="error",
                                category="type",
                                message=f"Type mismatch: DB field '{table}.{field_name}' ({field_type}) vs API field '{schema}.{camel_case}' ({api_type})",
                                source_file="database.md",
                                target_file="api_contract.md"
                            ))
                    elif field_name in api_schema_fields:
                        # API uses snake_case instead of camelCase
                        issues.append(ValidationIssue(
                            severity="warning",
                            category="naming",
                            message=f"Naming convention mismatch: DB uses '{field_name}', API should use '{camel_case}' (camelCase)",
                            source_file="database.md",
                            target_file="api_contract.md"
                        ))

        return issues

    def _validate_api_backend(self) -> List[ValidationIssue]:
        """Validate API contract against backend implementation."""
        issues = []

        # Extract API endpoints
        api_endpoints = self._extract_api_endpoints(self.plans["api_contract"])

        # Extract backend handlers/routes
        backend_handlers = self._extract_backend_handlers(self.plans["backend"])

        # Check if all API endpoints have backend handlers
        for endpoint, method in api_endpoints:
            handler_pattern = self._endpoint_to_handler(endpoint, method)

            if not any(handler_pattern in handler for handler in backend_handlers):
                issues.append(ValidationIssue(
                    severity="error",
                    category="integration",
                    message=f"Missing backend handler for API endpoint: {method} {endpoint}",
                    source_file="api_contract.md",
                    target_file="backend.md"
                ))

        return issues

    def _validate_backend_frontend(self) -> List[ValidationIssue]:
        """Validate backend API against frontend API calls."""
        issues = []

        # Extract API endpoints from backend
        api_endpoints = self._extract_api_endpoints(self.plans.get("api_contract", ""))
        if not api_endpoints:
            # Try extracting from backend if API contract not available
            api_endpoints = self._extract_backend_routes(self.plans["backend"])

        # Extract frontend API calls
        frontend_calls = self._extract_frontend_api_calls(self.plans["frontend"])

        # Check if frontend calls non-existent APIs
        for call in frontend_calls:
            if not any(call in endpoint for endpoint, _ in api_endpoints):
                issues.append(ValidationIssue(
                    severity="warning",
                    category="integration",
                    message=f"Frontend calls API endpoint '{call}' which may not exist in backend",
                    source_file="frontend.md",
                    target_file="backend.md"
                ))

        return issues

    def _validate_frontend_ui(self) -> List[ValidationIssue]:
        """Validate frontend plan against UI components."""
        issues = []

        # Extract component references from frontend
        frontend_components = self._extract_frontend_components(self.plans["frontend"])

        # Extract defined UI components
        ui_components = self._extract_ui_components(self.plans["ui_components"])

        # Check if all referenced components are defined
        for component in frontend_components:
            if component not in ui_components:
                issues.append(ValidationIssue(
                    severity="error",
                    category="integration",
                    message=f"Frontend references undefined UI component: {component}",
                    source_file="frontend.md",
                    target_file="ui_components.md"
                ))

        return issues

    # Helper extraction methods

    def _extract_db_fields(self, content: str) -> Dict[str, Dict[str, str]]:
        """Extract database fields from database.md."""
        tables = {}
        current_table = None

        # Simple regex to extract table and field definitions
        table_pattern = r"###?\s+Table:\s+(\w+)|###?\s+(\w+)\s+table"
        field_pattern = r"[-*]\s+(\w+):\s+(\w+)"

        for line in content.split('\n'):
            table_match = re.search(table_pattern, line, re.IGNORECASE)
            if table_match:
                current_table = table_match.group(1) or table_match.group(2)
                tables[current_table] = {}
                continue

            if current_table:
                field_match = re.search(field_pattern, line)
                if field_match:
                    field_name, field_type = field_match.groups()
                    tables[current_table][field_name] = field_type.upper()

        return tables

    def _extract_api_fields(self, content: str) -> Dict[str, Dict[str, str]]:
        """Extract API schema fields from api_contract.md."""
        schemas = {}
        current_schema = None

        # Extract from OpenAPI YAML or JSON schema definitions
        schema_pattern = r"(\w+)(?:Schema|Request|Response):"
        field_pattern = r"(\w+):\s*(?:type:\s*)?(\w+)"

        for line in content.split('\n'):
            schema_match = re.search(schema_pattern, line)
            if schema_match:
                current_schema = schema_match.group(1)
                schemas[current_schema] = {}
                continue

            if current_schema:
                field_match = re.search(field_pattern, line)
                if field_match:
                    field_name, field_type = field_match.groups()
                    schemas[current_schema][field_name] = field_type

        return schemas

    def _extract_api_endpoints(self, content: str) -> List[Tuple[str, str]]:
        """Extract API endpoints and methods."""
        endpoints = []

        # Match patterns like "GET /users", "POST /auth/login"
        endpoint_pattern = r"(GET|POST|PUT|PATCH|DELETE)\s+(/[\w/\-{}]+)"

        for match in re.finditer(endpoint_pattern, content, re.IGNORECASE):
            method, path = match.groups()
            endpoints.append((path, method.upper()))

        return endpoints

    def _extract_backend_handlers(self, content: str) -> List[str]:
        """Extract backend handler names."""
        handlers = []

        # Match handler/route definitions
        handler_patterns = [
            r"def\s+(\w+)",  # Python functions
            r"async\s+def\s+(\w+)",  # Python async functions
            r"function\s+(\w+)",  # JavaScript functions
            r"const\s+(\w+)\s*=",  # JavaScript const
            r"router\.(get|post|put|patch|delete)\s*\(",  # Express routes
        ]

        for pattern in handler_patterns:
            handlers.extend(re.findall(pattern, content, re.IGNORECASE))

        return handlers

    def _extract_backend_routes(self, content: str) -> List[Tuple[str, str]]:
        """Extract backend routes."""
        routes = []

        # Similar to API endpoints
        route_pattern = r"@app\.(?:route|get|post|put|patch|delete)\s*\(['\"]([^'\"]+)['\"]"

        for match in re.finditer(route_pattern, content):
            path = match.group(1)
            routes.append((path, ""))

        return routes

    def _extract_frontend_api_calls(self, content: str) -> List[str]:
        """Extract API calls from frontend plan."""
        calls = []

        # Match fetch/axios/api client calls
        call_patterns = [
            r"fetch\s*\(['\"]([^'\"]+)['\"]",
            r"axios\.(get|post|put|patch|delete)\s*\(['\"]([^'\"]+)['\"]",
            r"api\.(get|post|put|patch|delete)\s*\(['\"]([^'\"]+)['\"]",
        ]

        for pattern in call_patterns:
            for match in re.finditer(pattern, content):
                # Extract the URL path (last group)
                path = match.groups()[-1]
                calls.append(path)

        return calls

    def _extract_frontend_components(self, content: str) -> Set[str]:
        """Extract component references from frontend."""
        components = set()

        # Match component usage patterns
        component_patterns = [
            r"<(\w+)\s+",  # JSX components
            r"import\s+\{\s*(\w+)\s*\}",  # Import statements
            r"const\s+(\w+)\s*=.*useComponent",  # Component hooks
        ]

        for pattern in component_patterns:
            components.update(re.findall(pattern, content))

        return components

    def _extract_ui_components(self, content: str) -> Set[str]:
        """Extract defined UI components."""
        components = set()

        # Match component definitions
        component_patterns = [
            r"##\s+(\w+)\s+Component",
            r"export\s+(?:function|const)\s+(\w+)",
            r"class\s+(\w+)\s+extends",
        ]

        for pattern in component_patterns:
            components.update(re.findall(pattern, content))

        return components

    # Helper utility methods

    def _snake_to_camel(self, snake_str: str) -> str:
        """Convert snake_case to camelCase."""
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def _endpoint_to_handler(self, endpoint: str, method: str) -> str:
        """Convert endpoint to expected handler name pattern."""
        # Remove leading slash and convert to handler name
        # E.g., "/auth/login" + "POST" → "postAuthLogin"
        parts = endpoint.strip('/').split('/')
        handler_name = method.lower() + ''.join(p.title() for p in parts)
        return handler_name

    def _types_compatible(self, db_type: str, api_type: str) -> bool:
        """Check if database type and API type are compatible."""
        # Type compatibility mapping
        compatibility = {
            "UUID": ["string", "String"],
            "VARCHAR": ["string", "String"],
            "TEXT": ["string", "String"],
            "INTEGER": ["integer", "number", "int"],
            "INT": ["integer", "number", "int"],
            "BIGINT": ["integer", "number", "int"],
            "BOOLEAN": ["boolean", "bool"],
            "TIMESTAMP": ["string", "date-time", "DateTime"],
            "DATE": ["string", "date", "Date"],
            "JSON": ["object", "Object"],
            "JSONB": ["object", "Object"],
        }

        db_type_upper = db_type.upper()
        api_type_lower = api_type.lower()

        if db_type_upper in compatibility:
            return api_type_lower in [t.lower() for t in compatibility[db_type_upper]]

        return db_type_upper == api_type.upper()


def main():
    parser = argparse.ArgumentParser(description="Validate coherence across agent plans")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--plans-dir", required=True, help="Directory containing plan files")
    parser.add_argument("--output", default=None, help="Output file for validation report (JSON)")

    args = parser.parse_args()

    plans_dir = Path(args.plans_dir)
    if not plans_dir.exists():
        print(f"Error: Plans directory not found: {plans_dir}")
        return 1

    # Run validation
    validator = PlanValidator(plans_dir)
    result = validator.validate()

    # Print results
    print(f"\n{'='*60}")
    print(f"Plan Validation Report: {args.feature}")
    print(f"{'='*60}\n")
    print(f"Status: {result.status}")
    print(f"Errors: {len(result.errors)}")
    print(f"Warnings: {len(result.warnings)}")
    print()

    if result.errors:
        print("❌ ERRORS:")
        for issue in result.errors:
            print(f"  [{issue.category}] {issue.message}")
            print(f"    Source: {issue.source_file}")
            if issue.target_file:
                print(f"    Target: {issue.target_file}")
            print()

    if result.warnings:
        print("⚠️  WARNINGS:")
        for issue in result.warnings:
            print(f"  [{issue.category}] {issue.message}")
            print(f"    Source: {issue.source_file}")
            if issue.target_file:
                print(f"    Target: {issue.target_file}")
            print()

    if result.status == "PASS":
        print("✅ All plans are coherent. Ready to implement.")

    # Save JSON report if output specified
    if args.output:
        report = {
            "feature": args.feature,
            "status": result.status,
            "error_count": len(result.errors),
            "warning_count": len(result.warnings),
            "errors": [
                {
                    "severity": issue.severity,
                    "category": issue.category,
                    "message": issue.message,
                    "source_file": issue.source_file,
                    "target_file": issue.target_file
                }
                for issue in result.errors
            ],
            "warnings": [
                {
                    "severity": issue.severity,
                    "category": issue.category,
                    "message": issue.message,
                    "source_file": issue.source_file,
                    "target_file": issue.target_file
                }
                for issue in result.warnings
            ]
        }

        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\nValidation report saved to: {args.output}")

    # Return exit code based on status
    return 0 if result.status != "FAIL" else 1


if __name__ == "__main__":
    exit(main())
