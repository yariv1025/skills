# CICD-SEC-4 – Poisoned Pipeline Execution (PPE)

## Summary

Malicious code injected into pipeline (e.g. via PR, compromised job, or dependency) runs in trusted build context and can exfiltrate secrets or modify artifacts.

## Prevention

- Isolate and sandbox jobs; minimize secrets in env. Review and approve pipeline changes; use signed pipelines and verified inputs; restrict what jobs can do.

## Testing

- Attempt to inject steps or modify pipeline from PR; verify isolation and approval; test secret exposure.
