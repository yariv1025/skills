# I4 – Lack of Secure Update Mechanism

## Summary

Updates without integrity verification or encryption. Enables supply chain and MITM attacks during update.

## Prevention

- Sign firmware/updates; verify signature before apply. Use secure channel (TLS); support rollback; notify user of update status.

## Testing

- Verify signing and verification; test update over untrusted network; check rollback.
