# K01 – Insecure Workload Configurations

## Summary

Misconfigurations in manifests: running as root, writable filesystem, privileged containers, or excessive capabilities. Increases blast radius and exploitability.

## Prevention

- Set securityContext: runAsNonRoot, readOnlyRootFilesystem where possible; drop capabilities; avoid privileged. Use Pod Security Standards/Admission; scan manifests.

## Examples

### Wrong - Privileged container

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: insecure-pod
spec:
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      privileged: true  # Full host access!
      # Running as root by default
```

### Right - Hardened security context

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secure-pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
  containers:
  - name: app
    image: myapp:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop: ["ALL"]
    volumeMounts:
    - name: tmp
      mountPath: /tmp
  volumes:
  - name: tmp
    emptyDir: {}  # Writable temp directory if needed
```

### Right - Pod Security Standard (Restricted)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Wrong - Excessive capabilities

```yaml
securityContext:
  capabilities:
    add: ["NET_ADMIN", "SYS_ADMIN", "SYS_PTRACE"]  # Too many privileges
```

### Right - Minimal capabilities

```yaml
securityContext:
  capabilities:
    drop: ["ALL"]
    add: ["NET_BIND_SERVICE"]  # Only if needed for port < 1024
```

### Security context checklist

| Setting | Recommended | Why |
|---------|-------------|-----|
| `runAsNonRoot` | true | Prevent root exploits |
| `readOnlyRootFilesystem` | true | Prevent file system tampering |
| `allowPrivilegeEscalation` | false | Block privilege escalation |
| `privileged` | false | Never use in production |
| `capabilities.drop` | ["ALL"] | Principle of least privilege |

## Testing

- Audit manifests and runtime; check for root, privilege, and capability misuse.
