# LLM08 – Vector and Embedding Weaknesses

## Summary

RAG and embedding systems are vulnerable to embedding inversion, poisoned corpora, and multi-tenant vector store leakage. Malicious data can affect retrieval and model context.

## Prevention

- Validate and sanitize documents before embedding; isolate tenant data in vector stores. Monitor for poisoning and inversion; use integrity checks on retrieval inputs.

## Testing

- Test RAG with malicious or off-topic documents; attempt embedding inversion; verify tenant isolation.
