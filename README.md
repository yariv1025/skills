# Skills

This repository provides **skills** for Cursor, Anthropic, and other tools that accept this format. Use the skills in this repo to give your agent domain-specific capabilities.

**Repo:** [github.com/yariv1025/skills](https://github.com/yariv1025/skills)

## What Are Skills?

Skills are self-contained packages that give an AI agent domain-specific capabilities:

- **Workflows** — Multi-step procedures for specific tasks
- **Tool integrations** — Instructions for file formats, APIs, or toolchains
- **Domain expertise** — Schemas, standards, and reference material
- **Bundled resources** — Scripts, references, and assets used during execution

Each skill is built around a required `SKILL.md` (with YAML frontmatter and markdown instructions) and optional folders: `scripts/`, `references/`, and `assets/`.

## Repository Structure (Skills Provided)

| Path | Purpose |
|------|--------|
| **python-engineering/** | Production Python engineering patterns: architecture, observability, testing, performance/concurrency, core practices. Use when designing Python systems, implementing APIs, setting up monitoring, structuring tests, or following Python best practices. |

## python-engineering (skill details)

Production-grade Python patterns for designing systems, implementing APIs, monitoring, testing, and performance.

- **Path**: `python-engineering/`
- **When to use**: Designing Python systems, implementing async/sync APIs, setting up monitoring, structuring tests, optimizing performance, or following Python best practices.
- **Contents**:
  - **SKILL.md**: Overview, “When to read which reference” table, quick patterns, workflow pointers.
  - **references/**: `architecture.md` (package layout, DI, config, plugins), `observability.md` (logging, metrics, tracing, health), `testing.md` (test structure, fixtures, CI), `performance-concurrency.md` (async, concurrency, throughput), `core-practices.md` (GIL, packaging, I/O, reliability).
- **Pattern**: Progressive disclosure — SKILL.md stays lean; reference files are loaded only when relevant to the task.

## Install with npx (skills.sh)

Install skills using the [skills CLI](https://www.npmjs.com/package/skills)—no prior install required. The CLI discovers skills in this repo and installs them into your agent’s skills directory (e.g. `.cursor/skills/` for Cursor).

**Install all skills from this repo:**

```bash
npx skills add yariv1025/skills
```

**Install only `python-engineering` (e.g. for Cursor):**

```bash
npx skills add yariv1025/skills --skill python-engineering -a cursor -y
```

**Install by direct path:**

```bash
npx skills add https://github.com/yariv1025/skills/tree/main/python-engineering
```

Options: `-a, --agent` (e.g. `cursor`, `claude-code`), `-g, --global` (user directory), `-l, --list` (list skills without installing). See [skills.sh CLI docs](https://skills.sh/docs/cli).

## Other ways to use

Use the skill folder (e.g. `python-engineering/`) with your AI agent in the way it expects (e.g. add the folder to your skills path). To build a distributable `.skill` file from a skill folder (if your tool supports it):

```bash
pip install -r requirements.txt
python scripts/package_skill.py python-engineering [output-directory]
```

Validation runs automatically before packaging.


## License

Skills in this repository are provided under the terms in Apache License 2.0.
