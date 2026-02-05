# API6:2023 – Unrestricted Access to Sensitive Business Flows

## Summary

APIs expose business flows (e.g. signup, checkout, booking) without protection against excessive or automated use. Enables scalping, fake account creation, inventory abuse, or competitive scraping.

## Key CWEs

- CWE-799 Improper Control of Interaction Frequency
- CWE-837 Improper Enforcement of a Single, Unique Action

## Root Causes

- No anti-automation or bot detection; no limits on high-value or abuse-prone flows.
- Business logic not designed for adversarial use.

## Prevention Checklist

- Apply rate limiting and anti-automation (e.g. CAPTCHA, behavior analysis) to sensitive flows.
- Require step-up auth or additional verification for high-value actions.
- Monitor for abuse patterns; limit bulk or automated access.

## Secure Patterns

- Identify sensitive business flows and protect with rate limits, quotas, and optional CAPTCHA or challenge.
- Use idempotency keys where appropriate to prevent duplicate submissions while allowing retries.

## Testing

- Automate sensitive flows and check for detection/blocking; test rate limits and step-up auth.
