# P6 – Insufficient Deletion of User Data

## Summary

Failure to properly delete user data on request or when no longer needed. Data persists in backups, logs, or third parties.

## Prevention

Implement secure deletion (including backups and replicas); honor deletion requests within SLA. Map data flows and storage; purge from all systems and processors; document process.

## Testing

Request deletion and verify data is removed from primary and backup storage; check third-party processors.
