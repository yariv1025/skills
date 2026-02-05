# K09 – Misconfigured Cluster Components

## Summary

Insecure configuration of control plane, etcd, kubelet, or addons (ingress, service mesh). Default or weak config increases risk.

## Prevention

- Harden control plane (TLS, auth, audit); secure etcd; restrict kubelet and node access. Harden addons (ingress, mesh); follow CIS Kubernetes benchmarks; automate config checks.

## Testing

- Run config scanner (e.g. kube-bench); verify TLS and auth; check addon config.
