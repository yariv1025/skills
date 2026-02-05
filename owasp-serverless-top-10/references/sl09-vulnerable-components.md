# SL9 – Using Components with Known Vulnerabilities (Serverless)

## Summary

Dependencies (runtime, layers, packages) with known CVEs. Serverless layers and package dependencies must be scanned and updated.

## Prevention

Pin and scan dependencies; update runtime and layers; remove unused. Use SCA in CI; prefer minimal runtime and layer set.

## Testing

Scan function package and layers for CVEs; verify update process.
