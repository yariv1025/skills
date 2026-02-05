# K10 – Outdated and Vulnerable Kubernetes Components

## Summary

Running outdated K8s version or vulnerable addons (e.g. ingress, ArgoCD, Istio). Known CVEs can compromise the cluster.

## Prevention

- Upgrade control plane and nodes on a schedule; patch addons. Track CVEs for K8s and addons; use supported versions; scan and monitor.

## Testing

- Check versions against CVE databases; verify upgrade and patch process; scan for vulnerable addons.
