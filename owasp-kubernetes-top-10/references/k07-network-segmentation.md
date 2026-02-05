# K07 – Missing Network Segmentation Controls

## Summary

Lack of network policies allows unrestricted pod-to-pod and external traffic. Lateral movement and data exfiltration become easier.

## Prevention

- Define NetworkPolicies to restrict ingress/egress per namespace or pod; default deny where possible. Segment by tier (frontend, backend, data); restrict external egress.

## Testing

- Verify network policies; test cross-pod and egress access; validate default-deny behavior.
