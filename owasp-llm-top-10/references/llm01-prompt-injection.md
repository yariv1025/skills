# LLM01 – Prompt Injection

## Summary

Attackers manipulate LLM behavior via crafted inputs (direct or indirect) to bypass safeguards, extract data, or trigger unintended actions.

## Prevention

- Validate and constrain user input; use delimiters and structured prompts. Separate instructions from data; validate model output before acting. Prefer indirect injection controls (e.g. allowlisted actions).

## Testing

- Test with adversarial prompts; try instruction override and indirect injection; verify output validation.
