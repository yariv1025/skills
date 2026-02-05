# CNAS-4 – CI/CD pipeline and software supply chain flaws

## Summary

Insufficient auth in pipeline, untrusted or stale images, insecure registry communication, or over-permissive registry access. Supply chain compromise leads to malicious workloads.

## Prevention

Secure pipeline auth and artifact signing; use trusted registries and verify image integrity; restrict registry access; scan and sign images.

## Testing

Verify pipeline and registry security; test image signing and verification; check for stale or untrusted images.
