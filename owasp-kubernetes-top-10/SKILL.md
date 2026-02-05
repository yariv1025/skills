---
name: owasp-kubernetes-top-10
description: "OWASP Kubernetes Top 10 - prevention, detection, and remediation for Kubernetes security. Use when designing or reviewing K8s workloads and clusters - workload config, supply chain, RBAC, policy enforcement, logging, authentication, network segmentation, secrets, cluster components, vulnerable components."
---

# OWASP Kubernetes Top 10

This skill encodes the OWASP Kubernetes Top 10 for secure cluster and workload design and review. References are loaded per risk. Based on OWASP Kubernetes Top 10 2022.

## When to Read Which Reference

| Risk | Read |
|------|------|
| K01 Insecure Workload Configurations | [references/k01-insecure-workload-configurations.md](references/k01-insecure-workload-configurations.md) |
| K02 Supply Chain Vulnerabilities | [references/k02-supply-chain-vulnerabilities.md](references/k02-supply-chain-vulnerabilities.md) |
| K03 Overly Permissive RBAC | [references/k03-permissive-rbac.md](references/k03-permissive-rbac.md) |
| K04 Lack of Centralized Policy Enforcement | [references/k04-policy-enforcement.md](references/k04-policy-enforcement.md) |
| K05 Inadequate Logging and Monitoring | [references/k05-logging-monitoring.md](references/k05-logging-monitoring.md) |
| K06 Broken Authentication Mechanisms | [references/k06-broken-authentication.md](references/k06-broken-authentication.md) |
| K07 Missing Network Segmentation | [references/k07-network-segmentation.md](references/k07-network-segmentation.md) |
| K08 Secrets Management Failures | [references/k08-secrets-management.md](references/k08-secrets-management.md) |
| K09 Misconfigured Cluster Components | [references/k09-misconfigured-cluster-components.md](references/k09-misconfigured-cluster-components.md) |
| K10 Outdated and Vulnerable Components | [references/k10-vulnerable-components.md](references/k10-vulnerable-components.md) |

## Quick Patterns

- Run workloads as non-root with read-only filesystem where possible; use image signing and supply chain controls. Apply least-privilege RBAC and network policies; centralize policy (e.g. OPA); secure secrets and audit logging.

## Workflow

Load the reference for the risk you are addressing. See [OWASP Kubernetes Top 10](https://owasp.org/www-project-kubernetes-top-ten/) for the official list.
