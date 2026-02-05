# CNAS-3 – Improper authentication and authorization

## Summary

Unauthenticated API access, over-permissive cloud IAM, or unauthorized orchestrator access. Auth must be enforced at every layer.

## Prevention

Enforce auth for all APIs and control planes; use least-privilege IAM and RBAC. Validate tokens and identity; audit permissions regularly.

## Testing

Test unauthenticated access; verify IAM and RBAC scope; attempt privilege escalation.
