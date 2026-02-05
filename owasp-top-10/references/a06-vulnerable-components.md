# A06:2021 – Vulnerable and Outdated Components

## Summary

Using components (libraries, frameworks, OS) with known vulnerabilities or that are unsupported increases risk of exploitation. This category includes both direct and transitive dependencies. OWASP 2025 A03 Software Supply Chain Failures expands this theme (build, distribution, integrity).

## Key CWEs

- CWE-1035 OWASP Top Ten 2017 A9 Using Components with Known Vulnerabilities
- CWE-1104 Use of Unmaintained Third Party Components
- CWE-1395 Dependency on Vulnerable Third-Party Component

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/) for the full list.*

## Root Causes / Triggers

- Dependencies with known CVEs; no process to track or upgrade.
- No Software Bill of Materials (SBOM); transitive dependencies unknown.
- Using abandoned or unmaintained packages.
- Build and distribution pipeline not verified (supply chain; see 2025 A03).

## Prevention Checklist

- Maintain an inventory of dependencies (SBOM); scan for known vulnerabilities.
- Upgrade or patch vulnerable components; have a policy for acceptable risk and timelines.
- Prefer well-maintained, widely used components; remove unused dependencies.
- Pin versions (lock file) and verify integrity (checksums, signatures) when fetching.
- Harden build and release pipeline; verify artifact integrity.

## Secure Patterns

- **Dependency scanning:** Integrate SCA in CI; fail or gate on high/critical CVEs; track exceptions.
- **Pinning:** Use lock files (e.g. package-lock.json, poetry.lock) and reproducible builds.
- **SBOM:** Generate and store SBOM for releases; use for vulnerability and license compliance.

## Testing / Detection

- SCA tools (e.g. Snyk, Dependabot, OWASP Dependency-Check); run in CI.
- Review SBOM and dependency tree; check for outdated or abandoned packages.
- Verify build artifacts (signing, provenance) where supply chain is in scope.
