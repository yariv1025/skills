#!/usr/bin/env python3
"""
Setup project conventions for agent-dev-guardrails.

Generates:
- .cursor/rules/ with coding standards and quality gates
- AGENTS.md for cross-tool AI instructions
- dev/active/ folder for task documentation

Usage:
    python setup_project.py [options]

Options:
    --type TYPE     Project type (auto, python, node, go, rust, java, csharp, ruby, php)
    --path PATH     Project path (default: current directory)
    --no-cursor     Skip .cursor/rules/ generation
    --no-agents     Skip AGENTS.md generation
    --no-dev-docs   Skip dev/ folder generation
    --force         Overwrite existing files
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

# Project type markers
PROJECT_MARKERS = {
    "python": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"],
    "node": ["package.json"],
    "go": ["go.mod"],
    "rust": ["Cargo.toml"],
    "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
    "csharp": ["*.csproj", "*.sln"],
    "ruby": ["Gemfile"],
    "php": ["composer.json"],
}

# Language-specific conventions
LANGUAGE_CONVENTIONS = {
    "python": {
        "formatter": "ruff format",
        "linter": "ruff check",
        "type_checker": "mypy",
        "test_cmd": "pytest",
        "install_cmd": "pip install -e '.[dev]'",
    },
    "node": {
        "formatter": "prettier",
        "linter": "eslint",
        "type_checker": "tsc --noEmit",
        "test_cmd": "npm test",
        "install_cmd": "npm install",
    },
    "go": {
        "formatter": "gofmt -w .",
        "linter": "golangci-lint run",
        "type_checker": None,
        "test_cmd": "go test ./...",
        "install_cmd": "go mod download",
    },
    "rust": {
        "formatter": "cargo fmt",
        "linter": "cargo clippy",
        "type_checker": None,
        "test_cmd": "cargo test",
        "install_cmd": "cargo build",
    },
    "java": {
        "formatter": "google-java-format",
        "linter": "mvn checkstyle:check",
        "type_checker": None,
        "test_cmd": "mvn test",
        "install_cmd": "mvn install -DskipTests",
    },
    "csharp": {
        "formatter": "dotnet format",
        "linter": "dotnet build --warnaserror",
        "type_checker": None,
        "test_cmd": "dotnet test",
        "install_cmd": "dotnet restore",
    },
    "ruby": {
        "formatter": "rubocop -a",
        "linter": "rubocop",
        "type_checker": "sorbet",
        "test_cmd": "bundle exec rspec",
        "install_cmd": "bundle install",
    },
    "php": {
        "formatter": "php-cs-fixer fix",
        "linter": "vendor/bin/phpstan analyse",
        "type_checker": None,
        "test_cmd": "vendor/bin/phpunit",
        "install_cmd": "composer install",
    },
}


def detect_project_type(path: Path) -> Optional[str]:
    """Detect project type based on marker files."""
    for proj_type, markers in PROJECT_MARKERS.items():
        for marker in markers:
            if "*" in marker:
                # Glob pattern
                if list(path.glob(marker)):
                    return proj_type
            elif (path / marker).exists():
                return proj_type
    return None


def generate_coding_standards(proj_type: Optional[str]) -> str:
    """Generate coding-standards.mdc content."""
    conv = LANGUAGE_CONVENTIONS.get(proj_type, {})
    
    lang_section = ""
    if proj_type == "python":
        lang_section = """
## Python-Specific
- Use type hints for all function signatures
- Prefer f-strings over .format() or %
- Use pathlib for file paths
- Use context managers for resources
- Prefer dataclasses or Pydantic for data structures
"""
    elif proj_type == "node":
        lang_section = """
## TypeScript/JavaScript-Specific
- Use TypeScript strict mode
- Prefer const over let, avoid var
- Use async/await over raw promises
- Destructure when it improves readability
- Use template literals for string interpolation
"""
    elif proj_type == "go":
        lang_section = """
## Go-Specific
- Follow effective Go guidelines
- Use meaningful package names
- Handle all errors explicitly
- Use defer for cleanup
- Prefer composition over inheritance
"""
    elif proj_type == "rust":
        lang_section = """
## Rust-Specific
- Use Result for error handling
- Prefer &str over String when possible
- Use iterators over explicit loops when cleaner
- Document public APIs with /// comments
- Use #[derive] macros appropriately
"""
    elif proj_type == "java":
        lang_section = """
## Java-Specific
- Follow standard Java naming (camelCase, PascalCase for classes)
- Use try-with-resources for closeable resources
- Prefer Optional over null returns
- Use meaningful package structure (reverse domain)
- Prefer immutable objects where possible
"""
    elif proj_type == "csharp":
        lang_section = """
## C#-Specific
- Follow C# naming conventions (PascalCase public, _camelCase private)
- Use using statements for IDisposable
- Prefer async/await for I/O
- Use nullable reference types (C# 8+)
- Prefer expression-bodied members when concise
"""
    elif proj_type == "ruby":
        lang_section = """
## Ruby-Specific
- Follow Ruby style guide (2-space indent, snake_case)
- Use blocks and iterators; avoid unnecessary loops
- Prefer symbols for keys when appropriate
- Use meaningful method names (question marks for predicates)
- Handle nil explicitly; use safe navigation (&.) when appropriate
"""
    elif proj_type == "php":
        lang_section = """
## PHP-Specific
- Use PSR-12 for style; type hints for parameters and return types
- Prefer strict types (declare(strict_types=1))
- Use namespaces and autoloading (Composer)
- Avoid global state; use dependency injection
- Validate/sanitize input at boundaries
"""

    return f"""---
description: Coding standards and style guidelines for this project
alwaysApply: true
---

# Coding Standards

## General
- Use clear, descriptive names (variables, functions, types)
- Keep functions focused on a single responsibility
- Add comments only for non-obvious logic
- Handle errors explicitly, don't ignore them
- Prefer immutability when practical
{lang_section}
## File Organization
- Group related functionality in modules/packages
- Keep files under 300 lines when practical
- Use consistent directory structure
- Separate concerns (routes, logic, data, utils)

## Tools
- Formatter: {conv.get('formatter', '[configure]')}
- Linter: {conv.get('linter', '[configure]')}
- Type checker: {conv.get('type_checker', 'N/A')}
"""


def generate_quality_gates(proj_type: Optional[str]) -> str:
    """Generate quality-gates.mdc content."""
    conv = LANGUAGE_CONVENTIONS.get(proj_type, {})
    
    lint_cmd = conv.get('linter', '[linter command]')
    test_cmd = conv.get('test_cmd', '[test command]')
    type_cmd = conv.get('type_checker')
    
    type_check_item = f"- Type check: `{type_cmd}`" if type_cmd else ""
    
    return f"""---
description: Quality checks before and after code changes
alwaysApply: true
---

# Quality Gates

## Pre-Work Checklist
Before starting any code change:
- [ ] Understand the requirement clearly
- [ ] Identify affected files and dependencies
- [ ] Check for existing patterns to follow
- [ ] Plan the approach (for non-trivial changes)
- [ ] Create dev docs if task > 30 minutes

## Post-Work Checklist
After every code change:
- [ ] Lint: `{lint_cmd}` — fix any errors introduced
{type_check_item}
- [ ] Test: `{test_cmd}` — ensure all tests pass
- [ ] Self-review changes (apply reviewer roles)
- [ ] Summarize: files changed, validation results

## Definition of Done
A change is complete when:
- [ ] Code compiles/imports cleanly
- [ ] Lint passes (zero errors)
- [ ] Tests pass (no regressions)
- [ ] New code has test coverage
- [ ] Edge cases handled
- [ ] No hardcoded secrets
- [ ] Self-reviewed with relevant roles
- [ ] Dev docs updated (if applicable)

## Common Commands
| Action | Command |
|--------|---------|
| Install | `{conv.get('install_cmd', '[install command]')}` |
| Lint | `{lint_cmd}` |
| Test | `{test_cmd}` |
| Format | `{conv.get('formatter', '[format command]')}` |
"""


def generate_project_knowledge() -> str:
    """Generate project-knowledge.mdc template."""
    return """---
description: Project-specific context and conventions
alwaysApply: true
---

# Project Knowledge

## Overview
[Brief description of what this project does]

## Architecture
[Key architectural decisions and patterns]

## Key Files
| File | Purpose |
|------|---------|
| [path/to/main] | Entry point |
| [path/to/config] | Configuration |

## Conventions
- [Convention 1]
- [Convention 2]

## Common Tasks
| Task | How To |
|------|--------|
| Run locally | `[command]` |
| Run tests | `[command]` |
| Deploy | `[command]` |

## Do NOT
- [Things to avoid]
- Commit secrets or credentials
- Skip tests
"""


def generate_agents_md(proj_type: Optional[str], project_name: str) -> str:
    """Generate AGENTS.md content."""
    conv = LANGUAGE_CONVENTIONS.get(proj_type, {})
    
    lang_display = {
        "python": "Python",
        "node": "Node.js/TypeScript",
        "go": "Go",
        "rust": "Rust",
        "java": "Java",
        "csharp": "C#",
        "ruby": "Ruby",
        "php": "PHP",
    }.get(proj_type, proj_type.title() if proj_type else "Unknown")
    
    return f"""# AGENTS.md

> AI agent instructions for {project_name}. Works with Claude, Cursor, Copilot, and other AI coding tools.

## Project Overview
[Brief description of what this project does]

**Language:** {lang_display}

## Non-Negotiables

1. **Plan first, implement second** — For non-trivial changes, produce a plan before coding
2. **Work in small slices** — Implement 1-2 checklist items at a time; pause for review
3. **Never leave errors behind** — Fix lint/test failures before moving on
4. **Be explicit about changes** — List files changed and how validated

## Code Style

- **Formatter:** {conv.get('formatter', '[configure]')}
- **Linter:** {conv.get('linter', '[configure]')}
- **Type checker:** {conv.get('type_checker', 'N/A')}

Follow language idioms and existing patterns in the codebase.

## Quality Gates

After every code change:
- [ ] Run linter: `{conv.get('linter', '[linter]')}`
- [ ] Run tests: `{conv.get('test_cmd', '[test cmd]')}`
- [ ] Self-review for correctness, security, edge cases
- [ ] Summarize changes

## Common Commands

| Action | Command |
|--------|---------|
| Install deps | `{conv.get('install_cmd', '[install]')}` |
| Run tests | `{conv.get('test_cmd', '[test]')}` |
| Lint | `{conv.get('linter', '[lint]')}` |
| Format | `{conv.get('formatter', '[format]')}` |

## File Organization

```
[Add your project structure here]
```

## Do NOT

- Modify without understanding the impact
- Commit secrets or credentials
- Skip tests or linting
- Make large changes without a plan
- Ignore pre-existing patterns
"""


def create_file(path: Path, content: str, force: bool = False) -> bool:
    """Create a file with content. Returns True if created."""
    if path.exists() and not force:
        print(f"  Skipped (exists): {path}")
        return False
    
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  Created: {path}")
    return True


def setup_cursor_rules(project_path: Path, proj_type: str, force: bool = False) -> int:
    """Set up .cursor/rules/ directory."""
    rules_dir = project_path / ".cursor" / "rules"
    created = 0
    
    print("\nSetting up .cursor/rules/...")
    
    if create_file(
        rules_dir / "coding-standards.mdc",
        generate_coding_standards(proj_type),
        force
    ):
        created += 1
    
    if create_file(
        rules_dir / "quality-gates.mdc",
        generate_quality_gates(proj_type),
        force
    ):
        created += 1
    
    if create_file(
        rules_dir / "project-knowledge.mdc",
        generate_project_knowledge(),
        force
    ):
        created += 1
    
    return created


def setup_agents_md(project_path: Path, proj_type: Optional[str], force: bool = False) -> int:
    """Set up AGENTS.md file."""
    print("\nSetting up AGENTS.md...")
    
    project_name = project_path.name
    if create_file(
        project_path / "AGENTS.md",
        generate_agents_md(proj_type, project_name),
        force
    ):
        return 1
    return 0


def setup_dev_docs(project_path: Path, force: bool = False) -> int:
    """Set up dev/ directory structure."""
    print("\nSetting up dev/ folder...")
    
    dev_active = project_path / "dev" / "active"
    dev_active.mkdir(parents=True, exist_ok=True)
    
    gitkeep = dev_active / ".gitkeep"
    if create_file(gitkeep, "", force):
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Set up project conventions for agent-dev-guardrails"
    )
    parser.add_argument(
        "--type",
        choices=["auto", "python", "node", "go", "rust", "java", "csharp", "ruby", "php"],
        default="auto",
        help="Project type (default: auto-detect)"
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Project path (default: current directory)"
    )
    parser.add_argument(
        "--no-cursor",
        action="store_true",
        help="Skip .cursor/rules/ generation"
    )
    parser.add_argument(
        "--no-agents",
        action="store_true",
        help="Skip AGENTS.md generation"
    )
    parser.add_argument(
        "--no-dev-docs",
        action="store_true",
        help="Skip dev/ folder generation"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files"
    )
    
    args = parser.parse_args()
    project_path = args.path.resolve()
    
    if not project_path.is_dir():
        print(f"Error: {project_path} is not a directory")
        sys.exit(1)
    
    print(f"Project path: {project_path}")
    
    # Detect or use specified project type
    if args.type == "auto":
        proj_type = detect_project_type(project_path)
        if proj_type:
            print(f"Detected project type: {proj_type}")
        else:
            print("Could not detect project type, using generic templates")
            proj_type = None
    else:
        proj_type = args.type
        print(f"Using specified project type: {proj_type}")
    
    total_created = 0
    
    # Generate files
    if not args.no_cursor:
        total_created += setup_cursor_rules(project_path, proj_type, args.force)
    
    if not args.no_agents:
        total_created += setup_agents_md(project_path, proj_type, args.force)
    
    if not args.no_dev_docs:
        total_created += setup_dev_docs(project_path, args.force)
    
    print(f"\nDone! Created {total_created} file(s).")
    
    if total_created > 0:
        print("\nNext steps:")
        print("1. Review and customize the generated files")
        print("2. Add project-specific details to project-knowledge.mdc")
        print("3. Update AGENTS.md with your project structure")


if __name__ == "__main__":
    main()
