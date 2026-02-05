# M2 – Inadequate Supply Chain Security

## Summary

Risks from third-party SDKs, libraries, and build tooling. Compromised or malicious dependencies can steal data or alter behavior.

## Prevention

- Vet and minimize dependencies; use signed packages and verify integrity.
- Pin versions; monitor for CVEs; prefer well-maintained, widely used libraries.
- Secure build pipeline and signing keys; protect CI/CD.

## Testing

- SBOM and dependency scanning; review permissions and network access of SDKs.
