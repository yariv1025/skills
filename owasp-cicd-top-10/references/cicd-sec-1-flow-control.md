# CICD-SEC-1 – Insufficient Flow Control Mechanisms

## Summary

Lack of controls over pipeline execution flow allows unauthorized or unintended runs (e.g. from forks, wrong branch, or missing approval).

## Prevention

Require approval for production pipelines; restrict which branches and events can trigger. Validate pull request and branch context; use protected branches and status checks.

## Testing

Attempt to trigger pipeline from fork or wrong branch; verify approval and branch protection.
