# CICD-SEC-2 – Inadequate Identity and Access Management

## Summary

Weak authentication and authorization for pipeline and runner access. Over-privileged identities enable compromise and lateral movement.

## Prevention

Apply least privilege to pipeline identities and runners; use short-lived credentials. Enforce MFA and audit access; separate human and machine identities.

## Testing

Audit pipeline IAM and runner permissions; test for over-privilege and credential scope.
