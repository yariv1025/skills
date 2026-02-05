# SL10 – Insufficient Logging and Monitoring (Serverless)

## Summary

Missing or inadequate logging of invocations, errors, and security events. Hard to detect abuse or investigate incidents.

## Prevention

Log invocation metadata, errors, and auth failures; do not log secrets. Use structured logging; integrate with monitoring and alerting; set retention and access control.

## Testing

Verify log content and retention; test alerting; ensure no secret logging.
