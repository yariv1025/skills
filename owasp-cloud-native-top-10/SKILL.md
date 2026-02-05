---
name: owasp-cloud-native-top-10
description: "OWASP Cloud-Native Application Security Top 10 - prevention, detection, and remediation for containers, orchestration, and cloud-native apps. Use when securing insecure config, injection, auth, CI/CD and supply chain, secrets, network policies. Note - official list has 6 risks; project archived."
---

# OWASP Cloud-Native Application Security Top 10

This skill encodes the OWASP Cloud-Native Application Security Top 10 for secure cloud-native design and review. References are loaded per risk. Based on OWASP Cloud-Native Application Security Top 10 2022. **The official list defines 6 risks (CNAS-1 to CNAS-6); the project is archived.**

## When to Read Which Reference

| Risk | Read |
|------|------|
| CNAS-1 Insecure cloud, container or orchestration configuration | [references/cnas-1-insecure-configuration.md](references/cnas-1-insecure-configuration.md) |
| CNAS-2 Injection flaws | [references/cnas-2-injection-flaws.md](references/cnas-2-injection-flaws.md) |
| CNAS-3 Improper authentication and authorization | [references/cnas-3-auth.md](references/cnas-3-auth.md) |
| CNAS-4 CI/CD pipeline and software supply chain flaws | [references/cnas-4-cicd-supply-chain.md](references/cnas-4-cicd-supply-chain.md) |
| CNAS-5 Insecure secrets storage | [references/cnas-5-secrets-storage.md](references/cnas-5-secrets-storage.md) |
| CNAS-6 Over-permissive or insecure network policies | [references/cnas-6-network-policies.md](references/cnas-6-network-policies.md) |

## Quick Patterns

- Harden cloud and container config; validate input and avoid injection; enforce auth and least privilege; secure CI/CD and supply chain; protect secrets; apply network segmentation.

## Workflow

Load the reference for the risk you are addressing. See [OWASP Cloud-Native Application Security Top 10](https://owasp.org/www-project-cloud-native-application-security-top-10) (archived).
