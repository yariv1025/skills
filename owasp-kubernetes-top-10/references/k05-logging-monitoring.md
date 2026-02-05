# K05 – Inadequate Logging and Monitoring

## Summary

Insufficient audit logs and monitoring make detection and response difficult. API server and workload logs are critical for security.

## Prevention

- Enable audit logging for API server; aggregate and protect logs. Monitor for suspicious activity (e.g. privilege escalation, sensitive resource access); set alerts and retention.

## Testing

- Verify audit log content and retention; test alerting; review log access control.
