# LLM02 – Sensitive Information Disclosure

## Summary

Model outputs expose PII, proprietary data, or confidential business information. Training data or context can leak through responses.

## Prevention

- Filter and redact training data and context; do not include secrets in prompts or RAG. Apply output filters and access control; log and monitor for leakage.

## Testing

- Probe for PII and confidential data in outputs; test with edge queries; verify filtering.
