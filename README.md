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
| **agent-dev-guardrails/** | Disciplined agent development: plan-first, small slices, self-review roles, quality gates, project setup. Use when starting a project, setting conventions, or enforcing code quality and validation workflows. |
| **python-engineering/** | Production Python engineering patterns: architecture, observability, testing, performance/concurrency, core practices. Use when designing Python systems, implementing APIs, setting up monitoring, structuring tests, or following Python best practices. |
| **owasp-top-10/** | OWASP Web Application Security Top 10. Use when implementing or reviewing access control, authentication, crypto, injection, secure design, config, dependencies, logging, or SSRF. |
| **owasp-api-security-top-10/** | OWASP API Security Top 10. Use when designing or reviewing APIs: authorization, auth, rate limiting, business flows, SSRF, inventory, third-party API consumption. |
| **owasp-mobile-top-10/** | OWASP Mobile Top 10. Use when building or reviewing iOS/Android apps: credentials, supply chain, auth, validation, communication, privacy, binary protection, config, storage, crypto. |
| **owasp-iot-top-10/** | OWASP IoT Top 10. Use when designing or reviewing IoT devices: passwords, network services, ecosystem interfaces, updates, components, data, device management, defaults, physical hardening, privacy. |
| **owasp-llm-top-10/** | OWASP Top 10 for LLM Applications. Use when building or reviewing LLM/GenAI apps: prompt injection, disclosure, supply chain, poisoning, output handling, agency, prompt leakage, vectors, misinformation, consumption. |
| **owasp-kubernetes-top-10/** | OWASP Kubernetes Top 10. Use when designing or reviewing K8s workloads and clusters: workload config, supply chain, RBAC, policy, logging, auth, network segmentation, secrets, cluster config, vulnerable components. |
| **owasp-cicd-top-10/** | OWASP Top 10 CI/CD Security Risks. Use when securing or reviewing pipelines: flow control, IAM, dependency chain, poisoned pipeline, PBAC, credentials, config, third-party services, artifact integrity, logging. |
| **owasp-serverless-top-10/** | OWASP Serverless Top 10. Use when building or reviewing serverless apps: injection, auth, data exposure, XXE, access control, misconfiguration, XSS, deserialization, vulnerable components, logging. |
| **owasp-cloud-native-top-10/** | OWASP Cloud-Native Application Security Top 10 (6 risks). Use when securing containers and cloud-native apps: config, injection, auth, CI/CD and supply chain, secrets, network policies. |
| **owasp-privacy-top-10/** | OWASP Top 10 Privacy Risks. Use when addressing privacy: app vulns, data leakage, breach response, consent, transparency, deletion, data quality, session expiration, user access, excessive collection. |

## agent-dev-guardrails (skill details)

Plan-first development, small slices, self-review roles, quality gates, and project setup. Based on CURSOR_AGENT_GUIDE-style guardrails.

- **Path**: `agent-dev-guardrails/`
- **When to use**: Starting a new project, setting development conventions, wanting structured planning, or enforcing code quality and validation.
- **Contents**: SKILL.md (non-negotiables, hooks), references (planning-protocol, dev-docs-system, specialized-roles, project-setup, quality-gates), scripts/setup_project.py (generates .cursor/rules, AGENTS.md, dev/).
- **Pattern**: Progressive disclosure; references loaded when relevant.

## python-engineering (skill details)

Production-grade Python patterns for designing systems, implementing APIs, monitoring, testing, and performance.

- **Path**: `python-engineering/`
- **When to use**: Designing Python systems, implementing async/sync APIs, setting up monitoring, structuring tests, optimizing performance, or following Python best practices.
- **Contents**:
  - **SKILL.md**: Overview, “When to read which reference” table, quick patterns, workflow pointers.
  - **references/**: `architecture.md` (package layout, DI, config, plugins), `observability.md` (logging, metrics, tracing, health), `testing.md` (test structure, fixtures, CI), `performance-concurrency.md` (async, concurrency, throughput), `core-practices.md` (GIL, packaging, I/O, reliability).
- **Pattern**: Progressive disclosure — SKILL.md stays lean; reference files are loaded only when relevant to the task.

## OWASP Security Skills (skill details)

Ten skills covering OWASP Top 10–style lists. Each has a lean SKILL.md with a “When to read which reference” table and 6–10 reference files (one per risk). Install individually (e.g. `--skill owasp-top-10`) or all at once.

- **owasp-top-10**: Web Application Top 10 (A01–A10). references: a01–a10.
- **owasp-api-security-top-10**: API Security Top 10 (API1–API10). references: api1–api10.
- **owasp-mobile-top-10**: Mobile Top 10 (M1–M10). references: m1–m10.
- **owasp-iot-top-10**: IoT Top 10 (I1–I10). references: i1–i10.
- **owasp-llm-top-10**: Top 10 for LLM Applications (LLM01–LLM10). references: llm01–llm10.
- **owasp-kubernetes-top-10**: Kubernetes Top 10 (K01–K10). references: k01–k10.
- **owasp-cicd-top-10**: CI/CD Security Top 10 (CICD-SEC-1–10). references: cicd-sec-1–10.
- **owasp-serverless-top-10**: Serverless Top 10 (SL1–SL10). references: sl01–sl10.
- **owasp-cloud-native-top-10**: Cloud-Native Top 10 (CNAS-1–6, 6 risks). references: cnas-1–cnas-6.
- **owasp-privacy-top-10**: Privacy Risks (P1–P10). references: p1–p10.

## Install with npx (skills.sh)

Install skills using the [skills CLI](https://www.npmjs.com/package/skills)—no prior install required. The CLI discovers skills in this repo and installs them into your agent’s skills directory (e.g. `.cursor/skills/` for Cursor).

**Install all skills from this repo:**

```bash
npx skills add yariv1025/skills
```

**Install only one skill (e.g. for Cursor):**

```bash
npx skills add yariv1025/skills --skill agent-dev-guardrails -a cursor -y
npx skills add yariv1025/skills --skill python-engineering -a cursor -y
npx skills add yariv1025/skills --skill owasp-top-10 -a cursor -y
```

**Install by direct path:**

```bash
npx skills add https://github.com/yariv1025/skills/tree/main/agent-dev-guardrails
npx skills add https://github.com/yariv1025/skills/tree/main/python-engineering
```

Options: `-a, --agent` (e.g. `cursor`, `claude-code`), `-g, --global` (user directory), `-l, --list` (list skills without installing). See [skills.sh CLI docs](https://skills.sh/docs/cli).

## Other ways to use

Use the skill folder (e.g. `python-engineering/`) with your AI agent in the way it expects (e.g. add the folder to your skills path). To build a distributable `.skill` file from a skill folder (if your tool supports it):

```bash
pip install -r requirements.txt
python skill-creator/scripts/package_skill.py agent-dev-guardrails [output-directory]
python skill-creator/scripts/package_skill.py python-engineering [output-directory]
python skill-creator/scripts/package_skill.py owasp-top-10 [output-directory]
```

Validation runs automatically before packaging.


## License

Skills in this repository are provided under the terms in Apache License 2.0.
