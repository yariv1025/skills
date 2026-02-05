# CICD-SEC-3 – Dependency Chain Abuse

## Summary

Vulnerabilities in how dependencies are fetched (e.g. dependency confusion, typosquatting). Malicious packages can run in build context.

## Prevention

Use private or curated package sources; verify package integrity and namespace. Pin versions and use lock files; scan dependencies; restrict outbound from build.

## Testing

Test dependency resolution and source precedence; attempt dependency confusion; verify scanning.
