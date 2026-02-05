# M7 – Insufficient Binary Protections

## Summary

Lack of binary protections (e.g. tampering detection, obfuscation, anti-debug) makes reverse engineering and modification easier for attackers.

## Prevention

- Enable integrity checks (e.g. signature verification, runtime checks); detect tampering and respond safely.
- Use obfuscation for sensitive logic; make reverse engineering harder without relying on it alone.
- Detect debuggers and rooted/jailbroken environments where appropriate; limit sensitive operations.

## Testing

- Attempt tampering and reverse engineering; verify integrity and anti-tamper behavior.
