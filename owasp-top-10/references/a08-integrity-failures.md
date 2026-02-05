# A08:2021 – Software and Data Integrity Failures

## Summary

Failures related to software and data integrity include insecure deserialization, unsigned or unverified pipelines and updates, and supply chain compromise. Trust in build and update process without verification is a core issue.

## Key CWEs

- CWE-829 Inclusion of Functionality from Untrusted Control Sphere
- CWE-494 Download of Code Without Integrity Check
- CWE-502 Deserialization of Untrusted Data
- CWE-915 Improperly Controlled Modification of Dynamically-Determined Object Attributes

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/) for the full list.*

## Root Causes / Triggers

- Deserializing untrusted data without validation or type restriction (leading to RCE or abuse).
- CI/CD pipelines that do not verify artifact integrity or that run untrusted code.
- Updates or plugins installed without signature or integrity checks.
- Reliance on untrusted sources (e.g. unverified package repos).

## Prevention Checklist

- Do not deserialize untrusted data; use safe formats (e.g. JSON) and validate schema; restrict types if deserialization is required.
- Sign and verify artifacts in the pipeline; verify integrity before deployment.
- Use signed updates and verify signatures; secure the update mechanism.
- Maintain integrity of build environment and dependencies (see A06, supply chain).

## Secure Patterns

- **Deserialization:** Prefer data formats that do not allow object injection; if using serialization, use allowlists and minimal types; never deserialize from user input without strict control.
- **Pipeline:** Sign builds (e.g. attestations); verify before deploy; least privilege for pipeline identities.
- **Updates:** Verify signature or hash from a trusted source before applying.

## Testing / Detection

- SAST for deserialization of user-controlled data; review use of dangerous APIs.
- Verify pipeline signing and verification; test update integrity checks.
- Supply chain and dependency verification (see A06).
