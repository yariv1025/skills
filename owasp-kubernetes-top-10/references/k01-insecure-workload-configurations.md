# K01 – Insecure Workload Configurations

## Summary

Misconfigurations in manifests: running as root, writable filesystem, privileged containers, or excessive capabilities. Increases blast radius and exploitability.

## Prevention

- Set securityContext: runAsNonRoot, readOnlyRootFilesystem where possible; drop capabilities; avoid privileged. Use Pod Security Standards/Admission; scan manifests.

## Testing

- Audit manifests and runtime; check for root, privilege, and capability misuse.
