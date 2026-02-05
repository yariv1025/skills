# A05:2021 – Security Misconfiguration

## Summary

Security misconfiguration includes insecure default configs, unnecessary features enabled, default credentials, verbose errors, and missing security headers. Very common; often the result of incomplete hardening or copy-paste deployment.

## Key CWEs

- CWE-16 Configuration
- CWE-611 XML External Entity (XXE)
- CWE-756 Missing Custom Error Page
- CWE-209 Generation of Error Message Containing Sensitive Information

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/) for the full list.*

## Root Causes / Triggers

- Default credentials or default config left in place.
- Unnecessary features, debug endpoints, or sample apps enabled in production.
- Missing or weak security headers (CSP, HSTS, X-Frame-Options, etc.).
- Verbose error messages or stack traces exposed to users.
- Outdated or unpatched frameworks and servers.

## Prevention Checklist

- Harden all environments; remove or disable unneeded features and accounts.
- Change default credentials; use strong, unique credentials per environment.
- Set secure headers (CSP, HSTS, X-Content-Type-Options, etc.) and restrict CORS.
- Use generic error pages in production; log details server-side only.
- Maintain a secure baseline (e.g. checklist or IaC) and automate checks.

## Secure Patterns

- **Headers:** Configure Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options; avoid exposing server version.
- **Errors:** Catch exceptions at boundary; return generic message to client; log full detail securely.
- **Separation:** Different config for dev/staging/prod; no debug or samples in prod.

## Testing / Detection

- Scan for default credentials and known weak configs.
- Check security headers (e.g. securityheaders.com); verify error pages.
- Automated config review and compliance (e.g. CIS benchmarks, custom checks).
