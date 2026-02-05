---
name: owasp-cicd-top-10
description: "OWASP Top 10 CI/CD Security Risks - prevention, detection, and remediation for pipeline security. Use when securing or reviewing CI/CD - flow control, IAM, dependency chain, poisoned pipeline execution, PBAC, credential hygiene, system config, third-party services, artifact integrity, logging and visibility."
---

# OWASP Top 10 CI/CD Security Risks

This skill encodes the OWASP Top 10 CI/CD Security Risks for secure pipeline design and review. References are loaded per risk. Based on OWASP Top 10 CI/CD Security Risks 2022.

## When to Read Which Reference

| Risk | Read |
|------|------|
| CICD-SEC-1 Insufficient Flow Control | [references/cicd-sec-1-flow-control.md](references/cicd-sec-1-flow-control.md) |
| CICD-SEC-2 Inadequate IAM | [references/cicd-sec-2-iam.md](references/cicd-sec-2-iam.md) |
| CICD-SEC-3 Dependency Chain Abuse | [references/cicd-sec-3-dependency-chain-abuse.md](references/cicd-sec-3-dependency-chain-abuse.md) |
| CICD-SEC-4 Poisoned Pipeline Execution | [references/cicd-sec-4-poisoned-pipeline-execution.md](references/cicd-sec-4-poisoned-pipeline-execution.md) |
| CICD-SEC-5 Insufficient PBAC | [references/cicd-sec-5-pbac.md](references/cicd-sec-5-pbac.md) |
| CICD-SEC-6 Insufficient Credential Hygiene | [references/cicd-sec-6-credential-hygiene.md](references/cicd-sec-6-credential-hygiene.md) |
| CICD-SEC-7 Insecure System Configuration | [references/cicd-sec-7-insecure-system-config.md](references/cicd-sec-7-insecure-system-config.md) |
| CICD-SEC-8 Ungoverned 3rd Party Services | [references/cicd-sec-8-third-party-services.md](references/cicd-sec-8-third-party-services.md) |
| CICD-SEC-9 Improper Artifact Integrity Validation | [references/cicd-sec-9-artifact-integrity.md](references/cicd-sec-9-artifact-integrity.md) |
| CICD-SEC-10 Insufficient Logging and Visibility | [references/cicd-sec-10-logging-visibility.md](references/cicd-sec-10-logging-visibility.md) |

## Quick Patterns

- Enforce approval and branching for pipeline execution; apply least-privilege IAM. Verify dependency and artifact integrity; secure credentials; audit third-party usage; enable logging and alerting.

## Quick Reference / Examples

| Task | Approach |
|------|----------|
| Protect main branch | Require PR reviews, signed commits, branch protection. See [CICD-SEC-1](references/cicd-sec-1-flow-control.md). |
| Secure pipeline IAM | Least privilege, short-lived tokens, no shared creds. See [CICD-SEC-2](references/cicd-sec-2-iam.md). |
| Verify dependencies | Lock versions, audit, verify checksums. See [CICD-SEC-3](references/cicd-sec-3-dependency-chain-abuse.md). |
| Protect credentials | Use secrets manager, rotate, never log. See [CICD-SEC-6](references/cicd-sec-6-credential-hygiene.md). |
| Sign artifacts | Sign images/packages, verify before deploy. See [CICD-SEC-9](references/cicd-sec-9-artifact-integrity.md). |

**Safe - GitHub branch protection:**
```yaml
# .github/settings.yml (or repo settings)
branches:
  - name: main
    protection:
      required_pull_request_reviews:
        required_approving_review_count: 1
      required_status_checks:
        strict: true
```

**Safe - short-lived OIDC credentials (GitHub Actions):**
```yaml
permissions:
  id-token: write
  contents: read

steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
      aws-region: us-east-1
```

**Unsafe - long-lived secrets:**
```yaml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_KEY }}  # Prefer OIDC over static keys
```

## Workflow

Load the reference for the risk you are addressing. See [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/) for the official list.
