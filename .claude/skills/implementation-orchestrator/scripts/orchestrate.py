#!/usr/bin/env python3
"""
Agent Orchestrator

Defines execution order for multiple specialist agents based on dependency graph (DAG).
Ensures agents are invoked in correct sequence (database → API → backend → frontend → UI).

Usage:
    python3 orchestrate.py --feature "user_auth" --plans-dir ".claude/doc/user_auth/"
"""

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class AgentTask:
    """Represents a task to be executed by an agent."""
    agent_name: str
    plan_file: str
    dependencies: List[str] = field(default_factory=list)
    description: str = ""
    checkpoint: str = ""


@dataclass
class ExecutionPlan:
    """Execution plan with ordered agent tasks."""
    steps: List[AgentTask] = field(default_factory=list)

    def add_step(self, task: AgentTask):
        """Add a task to the execution plan."""
        self.steps.append(task)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "steps": [
                {
                    "step_number": idx + 1,
                    "agent": task.agent_name,
                    "plan_file": task.plan_file,
                    "dependencies": task.dependencies,
                    "description": task.description,
                    "checkpoint": task.checkpoint
                }
                for idx, task in enumerate(self.steps)
            ]
        }


class AgentOrchestrator:
    """Orchestrates agent execution based on dependency graph."""

    # Dependency graph: agent → list of agents it depends on
    DEPENDENCY_GRAPH = {
        "database-architect": [],
        "api-contract-designer": ["database-architect"],
        "domain-logic-architect": ["api-contract-designer"],
        "presentation-layer-architect": ["domain-logic-architect"],
        "ui-component-architect": ["presentation-layer-architect"],
    }

    # Mapping: plan file → agent name
    PLAN_TO_AGENT = {
        "database.md": "database-architect",
        "api_contract.md": "api-contract-designer",
        "backend.md": "domain-logic-architect",
        "frontend.md": "presentation-layer-architect",
        "ui_components.md": "ui-component-architect",
    }

    # Agent descriptions and checkpoints
    AGENT_INFO = {
        "database-architect": {
            "description": "Create database schema and migrations",
            "checkpoint": "Run migrations, verify schema with database inspection"
        },
        "api-contract-designer": {
            "description": "Define API contracts (OpenAPI/GraphQL schemas)",
            "checkpoint": "Validate contract syntax, generate API documentation"
        },
        "domain-logic-architect": {
            "description": "Implement backend business logic and API handlers",
            "checkpoint": "Run unit tests, verify API responses with contract"
        },
        "presentation-layer-architect": {
            "description": "Implement frontend logic and API integration",
            "checkpoint": "Run integration tests, verify API calls"
        },
        "ui-component-architect": {
            "description": "Build UI component library",
            "checkpoint": "Run component tests, visual regression tests"
        }
    }

    def __init__(self, plans_dir: Path):
        self.plans_dir = plans_dir
        self.available_plans: Set[str] = set()
        self._detect_plans()

    def _detect_plans(self):
        """Detect which agent plans exist."""
        for plan_file in self.PLAN_TO_AGENT.keys():
            if (self.plans_dir / plan_file).exists():
                self.available_plans.add(plan_file)

    def generate_execution_plan(self) -> ExecutionPlan:
        """Generate execution plan based on available plans and dependencies."""
        execution_plan = ExecutionPlan()

        # Topological sort to determine execution order
        ordered_agents = self._topological_sort()

        # Build execution steps
        for agent_name in ordered_agents:
            # Find the plan file for this agent
            plan_file = self._agent_to_plan(agent_name)
            if plan_file and plan_file in self.available_plans:
                task = AgentTask(
                    agent_name=agent_name,
                    plan_file=plan_file,
                    dependencies=self.DEPENDENCY_GRAPH.get(agent_name, []),
                    description=self.AGENT_INFO[agent_name]["description"],
                    checkpoint=self.AGENT_INFO[agent_name]["checkpoint"]
                )
                execution_plan.add_step(task)

        return execution_plan

    def _topological_sort(self) -> List[str]:
        """Perform topological sort on dependency graph."""
        # Build in-degree map
        in_degree = {agent: 0 for agent in self.DEPENDENCY_GRAPH.keys()}
        for agent, deps in self.DEPENDENCY_GRAPH.items():
            for dep in deps:
                in_degree[agent] += 1

        # Find agents with no dependencies
        queue = [agent for agent, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            # Sort to ensure consistent ordering when multiple agents have same priority
            queue.sort()
            current = queue.pop(0)
            result.append(current)

            # Reduce in-degree for dependent agents
            for agent, deps in self.DEPENDENCY_GRAPH.items():
                if current in deps:
                    in_degree[agent] -= 1
                    if in_degree[agent] == 0:
                        queue.append(agent)

        return result

    def _agent_to_plan(self, agent_name: str) -> Optional[str]:
        """Convert agent name to plan file."""
        for plan_file, agent in self.PLAN_TO_AGENT.items():
            if agent == agent_name:
                return plan_file
        return None

    def print_execution_plan(self, plan: ExecutionPlan):
        """Print execution plan in human-readable format."""
        print(f"\n{'='*60}")
        print(f"Agent Execution Plan")
        print(f"{'='*60}\n")

        for idx, task in enumerate(plan.steps, 1):
            print(f"Step {idx}: {task.agent_name}")
            print(f"  Plan: {task.plan_file}")
            print(f"  Description: {task.description}")

            if task.dependencies:
                deps_str = ", ".join(task.dependencies)
                print(f"  Dependencies: {deps_str}")
            else:
                print(f"  Dependencies: None")

            print(f"  Checkpoint: {task.checkpoint}")
            print()

        print(f"Total steps: {len(plan.steps)}")
        print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Generate agent execution plan")
    parser.add_argument("--feature", required=True, help="Feature name")
    parser.add_argument("--plans-dir", required=True, help="Directory containing plan files")
    parser.add_argument("--output", default=None, help="Output file for execution plan (JSON)")

    args = parser.parse_args()

    plans_dir = Path(args.plans_dir)
    if not plans_dir.exists():
        print(f"Error: Plans directory not found: {plans_dir}")
        return 1

    # Generate execution plan
    orchestrator = AgentOrchestrator(plans_dir)
    execution_plan = orchestrator.generate_execution_plan()

    # Print plan
    orchestrator.print_execution_plan(execution_plan)

    # Save JSON if output specified
    if args.output:
        plan_dict = execution_plan.to_dict()
        plan_dict["feature"] = args.feature

        with open(args.output, 'w') as f:
            json.dump(plan_dict, f, indent=2)

        print(f"Execution plan saved to: {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())
