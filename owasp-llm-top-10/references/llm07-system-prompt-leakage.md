# LLM07 – System Prompt Leakage

## Summary

Attackers extract or infer sensitive information (rules, PII, internal logic) from system prompts via crafted user prompts or side channels.

## Prevention

- Minimize sensitive content in system prompts; use separate, protected config where possible. Monitor for extraction attempts; rotate or redact if leakage suspected.

## Testing

- Attempt to extract system prompt and rules; test with "ignore previous instructions" and similar; verify no sensitive leakage.
