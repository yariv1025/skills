# CNAS-6 – Over-permissive or insecure network policies

## Summary

Over-permissive pod-to-pod or external traffic; missing network segmentation. Enables lateral movement and data exfiltration.

## Prevention

Define and enforce network policies; default deny where possible; segment by tier; restrict egress; use encryption in transit.

## Testing

Verify network policies and segmentation; test cross-pod and egress access; validate default-deny.
