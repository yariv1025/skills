# A07:2021 – Identification and Authentication Failures

## Summary

Authentication and identification failures allow attackers to compromise passwords, tokens, or session identifiers, or to exploit weak session management. This includes credential stuffing, brute force, weak password policy, and missing MFA.

## Key CWEs

- CWE-287 Improper Authentication
- CWE-384 Session Fixation
- CWE-306 Missing Authentication for Critical Function
- CWE-798 Hard-coded Credentials
- CWE-521 Weak Password Requirements

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/) for the full list.*

## Root Causes / Triggers

- Weak or default credentials; no MFA for sensitive actions.
- Credentials or session tokens transmitted or stored insecurely.
- Session fixation, long-lived or improperly invalidated sessions.
- Missing or weak rate limiting on login and password reset.
- Exposing credential or session info in URLs or logs.

## Prevention Checklist

- Require strong password policy and MFA for sensitive accounts and actions.
- Use secure session management: random session IDs, secure cookie flags, timeout and logout.
- Store passwords with strong adaptive hashing (see A02); never in cleartext.
- Rate limit login and password reset; lock or delay after failures.
- Do not expose session IDs in URLs; use HTTPS and Secure/HttpOnly cookies.

## Secure Patterns

- **Sessions:** Generate cryptographically random session ID; bind to user and IP/UA if appropriate; invalidate on logout and timeout.
- **Passwords:** Hash with Argon2/bcrypt; never log or echo; use secure comparison.
- **MFA:** Prefer TOTP or hardware; avoid SMS for high-risk; enforce for admin and sensitive operations.

## Testing / Detection

- Test for default credentials, weak password rules, and missing MFA.
- Verify session invalidation and timeout; check for fixation and token in URL.
- Brute-force and rate-limiting tests; credential stuffing simulation.
