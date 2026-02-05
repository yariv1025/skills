# K03 – Overly Permissive RBAC Configurations

## Summary

Excessive Role/ClusterRole permissions allow privilege escalation or lateral movement. Over-granting to service accounts and users is common.

## Prevention

- Apply least privilege; use namespaced roles; avoid cluster-admin and wildcards. Audit and trim bindings; prefer dedicated roles per workload; use automated RBAC review.

## Testing

- Enumerate permissions per service account and user; attempt privilege escalation; verify least privilege.
