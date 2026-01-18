#!/usr/bin/env python3
"""
Run all skill tests.

Usage:
    python run_tests.py [--verbose]
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from test_skill_structure import main as test_structure
from test_skill_references import main as test_references
from test_skill_scripts import main as test_scripts
from test_skill_mixins import main as test_mixins
from test_manifest_integrity import main as test_manifest


def main():
    parser = argparse.ArgumentParser(description="Run all skill tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  INFORMATIK-AI-METH SKILLS TEST SUITE")
    print("=" * 60)
    print()

    test_modules = [
        ("Skill Structure", test_structure),
        ("Skill References", test_references),
        ("Skill Scripts", test_scripts),
        ("Skill Mixins", test_mixins),
        ("Manifest Integrity", test_manifest),
    ]

    results = []

    for name, test_fn in test_modules:
        print(f"\n>>> Running: {name}")
        print("-" * 40)
        try:
            exit_code = test_fn()
            results.append((name, exit_code == 0))
        except Exception as e:
            print(f"ERROR: {e}")
            results.append((name, False))

    # Summary
    print()
    print("=" * 60)
    print("  SUMMARY")
    print("=" * 60)
    print()

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"  [{status}] {name}")

    print()
    print(f"  Total: {passed}/{total} test suites passed")
    print("=" * 60)

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
