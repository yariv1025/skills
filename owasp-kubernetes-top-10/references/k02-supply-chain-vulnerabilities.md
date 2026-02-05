# K02 – Supply Chain Vulnerabilities

## Summary

Risks from compromised or vulnerable container images, Helm charts, and dependencies. Untrusted or stale images can introduce malware or CVEs.

## Prevention

- Use signed images from trusted registries; verify signatures; pin to digest. Scan images for CVEs; use private registry and image pull secrets; minimize base image scope.

## Testing

- Verify image signing and scanning; test with untrusted image sources; check admission controls.
