# K04 – Lack of Centralized Policy Enforcement

## Summary

No cluster-wide policy (e.g. OPA/Gatekeeper) leads to inconsistent security (images, labels, resources) and drift. Hard to enforce standards at scale.

## Prevention

- Deploy admission controllers (OPA, Gatekeeper, Kyverno); define policies for images, resources, and labels. Enforce namespace and resource quotas; block non-compliant workloads.

## Testing

- Deploy non-compliant workload and verify rejection; audit policy coverage and exceptions.
