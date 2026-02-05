# A03:2021 – Injection

## Summary

Injection flaws occur when untrusted data is sent to an interpreter (SQL, NoSQL, OS, LDAP, template engine, etc.) as part of a command or query. Attackers can execute unintended commands or access data. Very common and high impact.

## Key CWEs

- CWE-79 Cross-site Scripting (XSS)
- CWE-89 SQL Injection
- CWE-78 OS Command Injection
- CWE-917 Expression Language Injection
- CWE-94 Code Injection

*Use the official [OWASP Top 10 CWE mapping](https://owasp.org/Top10/A03_2021-Injection/) for the full list.*

## Root Causes / Triggers

- Concatenating or interpolating user input into commands, queries, or templates.
- Missing or weak input validation and output encoding.
- Over-privileged database or process accounts.

## Prevention Checklist

- Use parameterized queries or prepared statements for all SQL/NoSQL; never build queries from string concatenation.
- Validate input (type, length, format) and use allowlists where possible.
- Encode output for the correct context (HTML, URL, JavaScript, etc.) to prevent XSS.
- Use safe APIs that avoid command/shell invocation; if unavoidable, strict allowlists and minimal privilege.
- Apply principle of least privilege for DB and process accounts.

## Secure Patterns

- **SQL:** Prepared statements with bound parameters: `SELECT * FROM users WHERE id = ?` and pass ID as parameter.
- **Output encoding:** Use framework or library encoding for the target context (e.g. HTML entity encoding for HTML body).
- **Templates:** Use template engines that auto-escape by default; avoid raw inclusion of user input.

## Testing / Detection

- SAST for concatenation into queries/commands and missing encoding.
- DAST/injection testing (SQLi, XSS, command injection) with fuzzing and payloads.
- Code review for all sinks that process user input.
