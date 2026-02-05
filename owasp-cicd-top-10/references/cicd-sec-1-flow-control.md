# CICD-SEC-1 – Insufficient Flow Control Mechanisms

## Summary

Lack of controls over pipeline execution flow allows unauthorized or unintended runs (e.g. from forks, wrong branch, or missing approval).

## Prevention

Require approval for production pipelines; restrict which branches and events can trigger. Validate pull request and branch context; use protected branches and status checks.

## Examples

### Wrong - No branch restrictions (GitHub Actions)

```yaml
# Any branch, any fork can trigger
name: Deploy
on: [push, pull_request]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh  # Runs on ANY push/PR
```

### Right - Branch and event restrictions

```yaml
name: Deploy
on:
  push:
    branches: [main]  # Only main branch
  workflow_dispatch:  # Manual trigger with approval

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production  # Requires environment approval
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

### Right - Prevent fork execution with secrets

```yaml
name: Build
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  build:
    runs-on: ubuntu-latest
    # Don't run on forks (they can't access secrets anyway)
    if: github.event.pull_request.head.repo.full_name == github.repository
    steps:
      - uses: actions/checkout@v4
      - run: npm test
```

### Right - GitHub branch protection rules

```yaml
# Via GitHub API or settings UI
# Require:
# - Pull request reviews (1+ approvals)
# - Status checks to pass
# - Up-to-date branches
# - Signed commits (optional)
# Restrict who can push to main
```

### Right - GitLab protected branches and approvals

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  script:
    - ./deploy.sh
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual  # Require manual approval
  environment:
    name: production
    url: https://example.com
```

### Flow control checklist

| Control | Implementation |
|---------|----------------|
| Branch protection | Require PR, reviews, status checks |
| Environment gates | Use environments with approvals |
| Fork restrictions | Check repo ownership before sensitive ops |
| Event filtering | Limit which events trigger pipelines |
| Manual approval | Use `workflow_dispatch` or manual gates |

## Testing

Attempt to trigger pipeline from fork or wrong branch; verify approval and branch protection.
