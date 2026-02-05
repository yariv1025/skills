---
name: owasp-llm-top-10
description: "OWASP Top 10 for LLM Applications - prevention, detection, and remediation for LLM and GenAI security. Use when building or reviewing LLM apps - prompt injection, information disclosure, training/supply chain, poisoning, output handling, excessive agency, system prompt leakage, vectors/embeddings, misinformation, unbounded consumption."
---

# OWASP Top 10 for LLM Applications

This skill encodes the OWASP Top 10 for Large Language Model Applications for secure LLM/GenAI design and review. References are loaded per risk. Based on OWASP Top 10 for LLM Applications 2025.

## When to Read Which Reference

| Risk | Read |
|------|------|
| LLM01 Prompt Injection | [references/llm01-prompt-injection.md](references/llm01-prompt-injection.md) |
| LLM02 Sensitive Information Disclosure | [references/llm02-sensitive-information-disclosure.md](references/llm02-sensitive-information-disclosure.md) |
| LLM03 Training Data & Supply Chain | [references/llm03-training-data-supply-chain.md](references/llm03-training-data-supply-chain.md) |
| LLM04 Data and Model Poisoning | [references/llm04-data-model-poisoning.md](references/llm04-data-model-poisoning.md) |
| LLM05 Improper Output Handling | [references/llm05-improper-output-handling.md](references/llm05-improper-output-handling.md) |
| LLM06 Excessive Agency | [references/llm06-excessive-agency.md](references/llm06-excessive-agency.md) |
| LLM07 System Prompt Leakage | [references/llm07-system-prompt-leakage.md](references/llm07-system-prompt-leakage.md) |
| LLM08 Vector and Embedding Weaknesses | [references/llm08-vector-embedding-weaknesses.md](references/llm08-vector-embedding-weaknesses.md) |
| LLM09 Misinformation | [references/llm09-misinformation.md](references/llm09-misinformation.md) |
| LLM10 Unbounded Consumption | [references/llm10-unbounded-consumption.md](references/llm10-unbounded-consumption.md) |

## Quick Patterns

- Treat all user and external input as untrusted; validate and sanitize LLM outputs before use (XSS, SSRF, RCE). Limit agency and tool use; protect system prompts and RAG data. Apply rate limits and cost controls.

## Workflow

Load the reference for the risk you are addressing. See [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications) and [genai.owasp.org](https://genai.owasp.org/) for the official list.
