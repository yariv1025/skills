# LLM06 – Excessive Agency

## Summary

Agentic systems with broad permissions and little human oversight can take harmful or unintended actions (e.g. tool use, API calls, data modification).

## Prevention

- Limit tool and API permissions; require human approval for sensitive actions. Use allowlists and quotas; audit agent decisions; design for least privilege.

## Testing

- Test agent with adversarial goals; verify permission checks and approval flows; check for privilege escalation.
