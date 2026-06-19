# Checkout Credential Boundary

status: completed

## Context

The hosted gate is read-only and performs no authenticated Git operation after
source retrieval, but the checkout step still accepted the action default that
stores the workflow token in the runner's Git configuration.

## Implementation

- Set `persist-credentials: false` on the single commit-pinned checkout step.
- Require exactly one checkout action and only the canonical workflow file.
- Keep the read-only permission, Ubuntu 24.04 runner, Python 3.12 setup, timeout,
  concurrency, and `make check` command unchanged.
- Document the credential-free checkout boundary in repository guidance.

## Verification

- `make lint`, `make test`, `make build`, and `make check` passed.
- The checker passed from an external working directory.
- Workflow YAML parsing, Python compilation, and `git diff --check` passed.
- Focused hostile mutations rejected a missing or true credential setting,
  duplicate checkout action, extra workflow file, incomplete plan, and stale
  documentation; all hostile mutations rejected.
- Exact-head hosted verification remains pending until this successor is
  pushed.

## Boundaries

- Do not add post-checkout pushes, tag creation, or authenticated Git fetches.
- Do not change the preserved numeric artifact or its manifest.
