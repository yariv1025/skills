# CICD-SEC-5 – Insufficient PBAC (Pipeline-Based Access Controls)

## Summary

Inadequate access restrictions within pipeline systems. Users or jobs can access or modify more than intended (e.g. other projects, secrets).

## Prevention

- Scope permissions per pipeline and project; restrict cross-project access. Use pipeline-level roles and secrets; audit who can edit pipelines and access logs.

## Testing

- Test cross-project and cross-pipeline access; verify secret and artifact isolation.
