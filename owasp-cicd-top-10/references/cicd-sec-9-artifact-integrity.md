# CICD-SEC-9 – Improper Artifact Integrity Validation

## Summary

Artifacts (images, packages) not signed or verified before use. Compromised or tampered artifacts can be deployed.

## Prevention

- Sign artifacts in pipeline; verify signature before deploy. Use attestations and SBOM; verify provenance; reject unsigned or mismatched artifacts.

## Testing

- Verify signing and verification in pipeline; attempt to deploy unsigned or tampered artifact; check provenance.
