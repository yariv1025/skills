# M8 – Security Misconfiguration

## Summary

Insecure default or custom configuration: debug mode in release, unnecessary permissions, exposed components, or weak platform settings.

## Prevention

- Disable debug and test code in release builds; strip logging and verbose errors.
- Request minimum permissions; justify and document each; review periodically.
- Use secure defaults for WebView, file access, and backups; follow platform hardening guides.

## Testing

- Inspect release build for debug flags and permissions; test backup and export; verify WebView config.
