# LLM04 – Data and Model Poisoning

## Summary

Attackers inject malicious or biased content into training data, fine-tuning, or embedding streams to alter model behavior or exfiltrate data.

## Prevention

- Validate and sanitize training and fine-tuning data; use integrity checks and provenance. Protect embedding and RAG pipelines from poisoned inputs; monitor for anomalous behavior.

## Testing

- Attempt poisoning of data and embedding inputs; verify detection and mitigation.
