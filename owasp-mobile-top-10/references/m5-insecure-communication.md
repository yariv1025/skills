# M5 – Insecure Communication

## Summary

Data transmitted over the network without encryption or with weak TLS can be intercepted or modified. Certificate validation and pinning mitigate MITM.

## Prevention

- Use TLS 1.2+ for all network traffic; enforce certificate validation; avoid cleartext.
- Consider certificate pinning for high-risk apps; handle pinning failures securely.
- Do not send sensitive data in URLs or headers; use secure cookie flags for web views.

## Testing

- Verify TLS and certificate validation; test with proxy; check for cleartext and weak ciphers.
