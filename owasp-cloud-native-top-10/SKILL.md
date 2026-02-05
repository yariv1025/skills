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

## Quick Reference / Examples

| Task | Approach |
|------|----------|
| Harden containers | Non-root, minimal base images, read-only fs. See [CNAS-1](references/cnas-1-insecure-configuration.md). |
| Prevent injection | Parameterized queries, validate cloud event data. See [CNAS-2](references/cnas-2-injection-flaws.md). |
| Secure auth | Use managed identity (IAM roles), short-lived tokens. See [CNAS-3](references/cnas-3-auth.md). |
| Protect CI/CD | Sign artifacts, verify dependencies, secure pipelines. See [CNAS-4](references/cnas-4-cicd-supply-chain.md). |
| Manage secrets | Use cloud secrets manager, never in code/env. See [CNAS-5](references/cnas-5-secrets-storage.md). |

**Safe - minimal Dockerfile:**
```dockerfile
FROM gcr.io/distroless/python3-debian12
COPY --chown=nonroot:nonroot app.py /app/
USER nonroot
ENTRYPOINT ["python3", "/app/app.py"]
```

**Unsafe - bloated image with root:**
```dockerfile
FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 curl vim  # Attack surface
COPY app.py /app/
# Running as root by default
```

**Secrets via AWS Secrets Manager:**
```python
import boto3
client = boto3.client("secretsmanager")
secret = client.get_secret_value(SecretId="prod/db/password")
db_password = secret["SecretString"]
```

## Workflow

Load the reference for the risk you are addressing. See [OWASP Cloud-Native Application Security Top 10](https://owasp.org/www-project-cloud-native-application-security-top-10) (archived).
