# Project Setup

Templates and automation for setting up development conventions in new projects.

## Table of Contents

1. [Overview](#overview)
2. [Project Type Detection](#project-type-detection)
3. [Cursor Rules Setup](#cursor-rules-setup)
4. [AGENTS.md Setup](#agentsmd-setup)
5. [Dev Folder Structure](#dev-folder-structure)
6. [Language-Specific Conventions](#language-specific-conventions)
7. [Setup Script Usage](#setup-script-usage)
8. [Examples](#examples)

---

## Overview

When starting a new project or adding guardrails to an existing one, set up:

1. **`.cursor/rules/`** — Cursor-specific AI instructions
2. **`AGENTS.md`** — Cross-tool AI instructions (works with Claude, Copilot, etc.)
3. **`dev/active/`** — Task documentation folder

---

## Project Type Detection

Detect project type by checking for marker files:

| Marker File | Project Type |
|-------------|--------------|
| `pyproject.toml`, `requirements.txt`, `setup.py` | Python |
| `package.json` | Node.js / JavaScript / TypeScript |
| `go.mod` | Go |
| `Cargo.toml` | Rust |
| `pom.xml`, `build.gradle` | Java |
| `*.csproj`, `*.sln` | C# / .NET |
| `Gemfile` | Ruby |
| `composer.json` | PHP |

**Detection order:** Check in priority order. If multiple found, prompt user to choose or use the most specific.

---

## Cursor Rules Setup

### Directory Structure

```
.cursor/
└── rules/
    ├── coding-standards.mdc      # Language/style rules
    ├── quality-gates.mdc         # Pre/post work checklists
    └── project-knowledge.mdc     # Project-specific context
```

### Rule File Format (.mdc)

```markdown
---
description: [When this rule applies]
globs: [Optional file patterns]
alwaysApply: [true/false]
---

[Rule content in markdown]
```

### Template: `coding-standards.mdc`

```markdown
---
description: Coding standards and style guidelines for this project
alwaysApply: true
---

# Coding Standards

## General
- Use clear, descriptive names
- Keep functions focused (single responsibility)
- Add comments only for non-obvious logic
- Handle errors explicitly

## [Language]-Specific
[Add language-specific rules here]

## File Organization
- Group related functionality
- Keep files under 300 lines when practical
- Use consistent directory structure
```

### Template: `quality-gates.mdc`

```markdown
---
description: Quality checks before and after code changes
alwaysApply: true
---

# Quality Gates

## Pre-Work Checklist
Before starting any code change:
- [ ] Understand the requirement
- [ ] Identify affected files
- [ ] Check for existing patterns to follow
- [ ] Plan the approach (for non-trivial changes)

## Post-Work Checklist
After every code change:
- [ ] Run linting (fix any errors introduced)
- [ ] Run tests (ensure nothing broken)
- [ ] Self-review the changes
- [ ] Summarize: files changed, validation results

## Definition of Done
A change is complete when:
- Code compiles/imports cleanly
- Lint and type checks pass
- Tests pass
- Edge cases addressed
- No hardcoded secrets
```

### Template: `project-knowledge.mdc`

```markdown
---
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
| [path] | [description] |

## Conventions
- [Convention 1]
- [Convention 2]

## Common Tasks
| Task | How To |
|------|--------|
| Run tests | `[command]` |
| Start dev server | `[command]` |
| Build | `[command]` |
```

---

## AGENTS.md Setup

`AGENTS.md` is a cross-tool standard for AI agent instructions. Place in project root.

### Template: `AGENTS.md`

```markdown
# AGENTS.md

> AI agent instructions for this project. Works with Claude, Cursor, Copilot, and other AI coding tools.

## Project Overview
[Brief description of the project]

## Non-Negotiables
1. **Plan first, implement second** — For non-trivial changes, produce a plan before coding
2. **Work in small slices** — Implement 1-2 items at a time
3. **Never leave errors behind** — Fix lint/test failures before moving on
4. **Be explicit about changes** — List files changed and how validated

## Code Style
- [Language]: [Style guide or key rules]
- Naming: [Conventions]
- Comments: [When to use]

## Architecture
[Key patterns and organization]

## Testing
- Framework: [Test framework]
- Run tests: `[command]`
- Coverage: [Requirements]

## Common Commands
| Action | Command |
|--------|---------|
| Install deps | `[command]` |
| Run tests | `[command]` |
| Lint | `[command]` |
| Build | `[command]` |

## File Organization
```
[Brief directory tree showing key areas]
```

## Do NOT
- Modify [protected files/directories]
- Commit secrets or credentials
- Skip tests or linting
- Make large changes without a plan
```

---

## Dev Folder Structure

Create a folder for task documentation:

```
dev/
├── active/           # Current work-in-progress tasks
│   └── .gitkeep
└── archive/          # Completed task docs (optional)
    └── .gitkeep
```

Task folders go in `dev/active/<task-name>/` with:
- `<task-name>-plan.md`
- `<task-name>-context.md`
- `<task-name>-tasks.md`

See [dev-docs-system.md](dev-docs-system.md) for templates.

---

## Language-Specific Conventions

### Python

```markdown
## Python Conventions

### Style
- Formatter: black (or ruff format)
- Linter: ruff
- Type checker: mypy (strict mode)

### Structure
```
src/
├── <package>/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── utils.py
tests/
├── conftest.py
├── test_models.py
└── test_services.py
```

### Commands
- Install: `pip install -e ".[dev]"` or `poetry install`
- Lint: `ruff check .`
- Format: `ruff format .`
- Type check: `mypy src/`
- Test: `pytest`
```

### Node.js / TypeScript

```markdown
## Node.js/TypeScript Conventions

### Style
- Formatter: prettier
- Linter: eslint
- Type checker: tsc (TypeScript)

### Structure
```
src/
├── index.ts
├── routes/
├── services/
└── utils/
tests/
├── setup.ts
└── *.test.ts
```

### Commands
- Install: `npm install` or `yarn`
- Lint: `npm run lint`
- Format: `npm run format`
- Type check: `npm run typecheck` or `tsc --noEmit`
- Test: `npm test`
```

### Go

```markdown
## Go Conventions

### Style
- Formatter: gofmt / goimports
- Linter: golangci-lint

### Structure
```
cmd/
├── app/
│   └── main.go
internal/
├── handlers/
├── services/
└── models/
pkg/
└── [shared libraries]
```

### Commands
- Build: `go build ./...`
- Lint: `golangci-lint run`
- Test: `go test ./...`
- Format: `gofmt -w .`
```

### Rust

```markdown
## Rust Conventions

### Style
- Formatter: rustfmt
- Linter: clippy

### Structure
```
src/
├── main.rs (or lib.rs)
├── models/
└── services/
tests/
└── integration_tests.rs
```

### Commands
- Build: `cargo build`
- Lint: `cargo clippy`
- Format: `cargo fmt`
- Test: `cargo test`
```

### Java

```markdown
## Java Conventions

### Style
- Formatter: google-java-format
- Linter: checkstyle (Maven/Gradle plugin)

### Structure
```
src/
├── main/java/
│   └── com/example/app/
└── test/java/
    └── com/example/app/
```

### Commands
- Build: `mvn compile` or `gradle build`
- Lint: `mvn checkstyle:check`
- Test: `mvn test` or `gradle test`
- Format: `google-java-format -i <files>`
```

### C# / .NET

```markdown
## C# Conventions

### Style
- Formatter: dotnet format
- Linter: dotnet build with treat warnings as errors

### Structure
```
src/
├── ProjectName/
│   ├── Program.cs
│   └── ...
tests/
└── ProjectName.Tests/
```

### Commands
- Restore: `dotnet restore`
- Build: `dotnet build`
- Lint: `dotnet format --verify-no-changes`
- Test: `dotnet test`
```

### Ruby

```markdown
## Ruby Conventions

### Style
- Formatter: rubocop -a
- Linter: rubocop
- Type checker: sorbet (optional)

### Structure
```
lib/
├── app_name/
│   └── ...
spec/
├── spec_helper.rb
└── app_name/
```

### Commands
- Install: `bundle install`
- Lint: `bundle exec rubocop`
- Format: `bundle exec rubocop -a`
- Test: `bundle exec rspec`
```

### PHP

```markdown
## PHP Conventions

### Style
- Formatter: php-cs-fixer
- Linter: phpstan

### Structure
```
src/
├── App/
│   └── ...
tests/
└── Unit/
```

### Commands
- Install: `composer install`
- Lint: `vendor/bin/phpstan analyse`
- Format: `vendor/bin/php-cs-fixer fix`
- Test: `vendor/bin/phpunit`
```

---

## Setup Script Usage

Run the setup script to auto-generate project conventions:

```bash
python scripts/setup_project.py [options]

Options:
  --type TYPE      Project type (auto, python, node, go, rust, java, csharp, ruby, php)
  --path PATH      Project path (default: current directory)
  --cursor         Generate .cursor/rules/ (default: yes)
  --agents         Generate AGENTS.md (default: yes)
  --dev-docs       Generate dev/ folder (default: yes)
  --force          Overwrite existing files
```

**Examples:**

```bash
# Auto-detect and generate everything
python scripts/setup_project.py

# Specific project type
python scripts/setup_project.py --type python

# Generate only AGENTS.md
python scripts/setup_project.py --cursor=no --dev-docs=no

# Different directory
python scripts/setup_project.py --path /path/to/project
```

---

## Examples

### Example: Setting Up a Python Project

```
User: "Set up development conventions for this Python project"

Agent:
Detected: Python project (found pyproject.toml)

Creating:
1. .cursor/rules/coding-standards.mdc — Python style (ruff, mypy)
2. .cursor/rules/quality-gates.mdc — Pre/post work checklists
3. .cursor/rules/project-knowledge.mdc — Project overview
4. AGENTS.md — Cross-tool AI instructions
5. dev/active/.gitkeep — Task docs folder

Files created:
- .cursor/rules/coding-standards.mdc
- .cursor/rules/quality-gates.mdc
- .cursor/rules/project-knowledge.mdc
- AGENTS.md
- dev/active/.gitkeep

Next: Review and customize the generated files for your project specifics.
```

### Example: Adding to Existing Project

```
User: "Add AGENTS.md to this project"

Agent:
Creating AGENTS.md based on detected project structure...

Detected:
- Type: Node.js/TypeScript
- Framework: Express + React
- Test framework: Jest
- Build tool: Vite

Generated AGENTS.md with:
- Project overview
- Code style (ESLint, Prettier)
- Architecture notes
- Common commands
- File organization

Created: AGENTS.md (127 lines)

Please review and add project-specific details.
```

### Example: Manual Setup Without Script

```
User: "Help me create Cursor rules manually"

Agent:
I'll create the rules directory and files.

1. Creating .cursor/rules/ directory
2. Creating coding-standards.mdc:

---
description: Coding standards for this project
alwaysApply: true
---

# Coding Standards

[Customize based on your stack]

3. Creating quality-gates.mdc:

---
description: Quality checks for code changes
alwaysApply: true
---

# Quality Gates

## Post-Work Checklist
- [ ] Run linting
- [ ] Run tests
- [ ] Self-review changes

Files created. Customize them for your project.
```
