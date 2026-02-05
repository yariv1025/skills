# I2 – Insecure Network Services

## Summary

Unnecessary or poorly secured network services (e.g. open ports, weak TLS) increase attack surface and exposure.

## Prevention

- Disable services not needed; restrict to necessary interfaces and ports. Use TLS and authentication; avoid cleartext. Segment device network.

## Testing

- Port scan and service enumeration; verify TLS and auth; check for default ports and services.
