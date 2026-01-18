#!/usr/bin/env python3
"""
Dependency Installer - Automated dependency installation across multiple languages

Detects package manager from lock files and runs appropriate install commands.
Supports: npm, pnpm, yarn, bun, pip, poetry, pipenv, bundler, cargo, go, composer

Usage:
    python install_dependencies.py [options]

Options:
    --force          Force reinstall even if already installed
    --skip-audit     Skip security audit after installation
    --dev            Include development dependencies
    --help           Show this help message
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional, Tuple, List


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_step(message: str):
    """Print a step message"""
    print(f"{Colors.BLUE}⏳ {message}{Colors.RESET}")


def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")


def print_warning(message: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.RESET}")


def print_error(message: str):
    """Print an error message"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")


def print_info(message: str):
    """Print an info message"""
    print(f"{Colors.BOLD}ℹ️  {message}{Colors.RESET}")


def detect_package_manager(project_root: Path) -> Tuple[Optional[str], Optional[str]]:
    """
    Detect package manager from lock files.

    Returns:
        Tuple of (package_manager_name, language)
    """
    # Node.js package managers
    if (project_root / "pnpm-lock.yaml").exists():
        return ("pnpm", "node")
    elif (project_root / "yarn.lock").exists():
        return ("yarn", "node")
    elif (project_root / "package-lock.json").exists():
        return ("npm", "node")
    elif (project_root / "bun.lockb").exists():
        return ("bun", "node")
    elif (project_root / "package.json").exists():
        return ("npm", "node")  # Default to npm if package.json exists

    # Python package managers
    elif (project_root / "poetry.lock").exists():
        return ("poetry", "python")
    elif (project_root / "Pipfile.lock").exists():
        return ("pipenv", "python")
    elif (project_root / "requirements.txt").exists():
        return ("pip", "python")

    # Ruby
    elif (project_root / "Gemfile.lock").exists():
        return ("bundle", "ruby")

    # Rust
    elif (project_root / "Cargo.lock").exists():
        return ("cargo", "rust")

    # Go
    elif (project_root / "go.mod").exists():
        return ("go", "go")

    # PHP
    elif (project_root / "composer.lock").exists():
        return ("composer", "php")

    return (None, None)


def check_if_installed(pkg_manager: str, project_root: Path) -> bool:
    """Check if dependencies are already installed"""
    if pkg_manager in ["npm", "pnpm", "yarn", "bun"]:
        return (project_root / "node_modules").exists()
    elif pkg_manager == "pip":
        return (project_root / "venv").exists() or (project_root / ".venv").exists()
    elif pkg_manager == "poetry":
        # Check if poetry env exists
        result = subprocess.run(
            ["poetry", "env", "info", "--path"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    elif pkg_manager == "bundle":
        return (project_root / "vendor" / "bundle").exists()

    return False


def get_install_command(
    pkg_manager: str,
    include_dev: bool = False,
    frozen: bool = True
) -> List[str]:
    """Get the install command for the detected package manager"""
    if pkg_manager == "pnpm":
        cmd = ["pnpm", "install"]
        if frozen:
            cmd.append("--frozen-lockfile")
        return cmd

    elif pkg_manager == "npm":
        # Use npm ci for frozen installs (CI mode)
        return ["npm", "ci"] if frozen else ["npm", "install"]

    elif pkg_manager == "yarn":
        cmd = ["yarn", "install"]
        if frozen:
            # Check if Yarn 2+ (Berry)
            result = subprocess.run(
                ["yarn", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                if version.startswith("1."):
                    cmd.append("--frozen-lockfile")
                else:
                    cmd.append("--immutable")
        return cmd

    elif pkg_manager == "bun":
        cmd = ["bun", "install"]
        if frozen:
            cmd.append("--frozen-lockfile")
        return cmd

    elif pkg_manager == "poetry":
        cmd = ["poetry", "install"]
        if not include_dev:
            cmd.extend(["--without", "dev"])
        return cmd

    elif pkg_manager == "pipenv":
        cmd = ["pipenv", "install"]
        if include_dev:
            cmd.append("--dev")
        return cmd

    elif pkg_manager == "pip":
        return ["pip", "install", "-r", "requirements.txt"]

    elif pkg_manager == "bundle":
        return ["bundle", "install"]

    elif pkg_manager == "cargo":
        return ["cargo", "fetch"]

    elif pkg_manager == "go":
        return ["go", "mod", "download"]

    elif pkg_manager == "composer":
        cmd = ["composer", "install"]
        if not include_dev:
            cmd.append("--no-dev")
        return cmd

    return []


def run_security_audit(pkg_manager: str, project_root: Path) -> bool:
    """Run security audit if supported"""
    if pkg_manager == "npm":
        print_step("Running security audit...")
        result = subprocess.run(
            ["npm", "audit", "--production"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_warning("Security vulnerabilities found. Run 'npm audit fix' to resolve.")
            return False
        else:
            print_success("No security vulnerabilities found")
            return True

    elif pkg_manager == "pnpm":
        print_step("Running security audit...")
        result = subprocess.run(
            ["pnpm", "audit", "--production"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_warning("Security vulnerabilities found.")
            return False
        else:
            print_success("No security vulnerabilities found")
            return True

    elif pkg_manager == "yarn":
        print_step("Running security audit...")
        result = subprocess.run(
            ["yarn", "audit"],
            cwd=project_root,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print_warning("Security vulnerabilities found.")
            return False
        else:
            print_success("No security vulnerabilities found")
            return True

    return True


def count_packages(pkg_manager: str, project_root: Path) -> int:
    """Count installed packages"""
    try:
        if pkg_manager in ["npm", "pnpm", "yarn", "bun"]:
            node_modules = project_root / "node_modules"
            if node_modules.exists():
                return len([d for d in node_modules.iterdir() if d.is_dir() and not d.name.startswith(".")])
        elif pkg_manager == "pip":
            result = subprocess.run(
                ["pip", "list", "--format=freeze"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return len(result.stdout.strip().split("\n"))
    except Exception:
        pass

    return 0


def main():
    # Parse arguments
    force_install = "--force" in sys.argv
    skip_audit = "--skip-audit" in sys.argv
    include_dev = "--dev" in sys.argv

    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)

    project_root = Path.cwd()

    print(f"{Colors.BOLD}🚀 Dependency Installer{Colors.RESET}")
    print(f"Project: {project_root}\n")

    # Detect package manager
    print_step("Detecting package manager...")
    pkg_manager, language = detect_package_manager(project_root)

    if not pkg_manager:
        print_error("No package manager detected. No package.json, requirements.txt, or similar found.")
        sys.exit(1)

    print_success(f"Detected: {pkg_manager} ({language})")

    # Check if already installed
    if not force_install and check_if_installed(pkg_manager, project_root):
        print_info("Dependencies appear to be already installed.")
        print_info("Use --force to reinstall.")
        response = input("Continue with installation anyway? (y/N): ")
        if response.lower() != 'y':
            print("Installation cancelled.")
            sys.exit(0)

    # Get install command
    install_cmd = get_install_command(pkg_manager, include_dev=include_dev, frozen=True)

    if not install_cmd:
        print_error(f"Install command not configured for {pkg_manager}")
        sys.exit(1)

    # Run installation
    print(f"\n{Colors.BOLD}Running installation...{Colors.RESET}")
    print(f"Command: {' '.join(install_cmd)}\n")

    start_time = time.time()

    try:
        result = subprocess.run(
            install_cmd,
            cwd=project_root,
            check=True
        )

        end_time = time.time()
        duration = end_time - start_time

        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Installation completed in {duration:.1f}s{Colors.RESET}\n")

        # Count packages
        pkg_count = count_packages(pkg_manager, project_root)
        if pkg_count > 0:
            print_info(f"Total packages installed: {pkg_count}")

        # Run security audit
        if not skip_audit and pkg_manager in ["npm", "pnpm", "yarn"]:
            print()
            run_security_audit(pkg_manager, project_root)

        # Print next steps
        print(f"\n{Colors.BOLD}🎉 Ready to develop!{Colors.RESET}")
        if pkg_manager in ["npm", "pnpm", "yarn", "bun"]:
            print(f"Next: {pkg_manager} run dev")
        elif pkg_manager == "poetry":
            print("Next: poetry run python main.py")
        elif pkg_manager == "pip":
            print("Next: source venv/bin/activate && python main.py")

        sys.exit(0)

    except subprocess.CalledProcessError as e:
        print_error(f"Installation failed with exit code {e.returncode}")
        sys.exit(1)
    except FileNotFoundError:
        print_error(f"Package manager '{pkg_manager}' not found. Please install it first.")
        if pkg_manager == "pnpm":
            print_info("Install pnpm: npm install -g pnpm")
        elif pkg_manager == "poetry":
            print_info("Install poetry: curl -sSL https://install.python-poetry.org | python3 -")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
