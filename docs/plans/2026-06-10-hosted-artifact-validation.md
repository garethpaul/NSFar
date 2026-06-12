# Hosted Artifact Validation

status: completed

## Context

The repository preserves a byte-sensitive numeric artifact and synchronized
manifest, but has no hosted integrity validation.

## Priorities

1. Run the canonical artifact integrity gate on hosted Linux.
2. Pin checkout, Python, permissions, runner, timeout, and concurrency behavior.
3. Enforce the workflow contract from `scripts/check-baseline.py`.
4. Preserve bytes, mode, line endings, checksum, schema, and aggregate metadata.
5. Validate file mode from Git's index so local umask settings cannot create
   false failures.

## Implementation Units

Files:

- `.github/workflows/check.yml`
- `scripts/check-baseline.py`
- `README.md`
- `VISION.md`
- `SECURITY.md`
- `CHANGES.md`

Add push, pull-request, and manual triggers; read-only permissions; concurrency
cancellation; a bounded `ubuntu-24.04` job; commit-pinned checkout and Python
setup; and `make check`. Require that contract from the baseline checker.
Read the artifact mode from `git ls-files --stage`, matching the mode Git stores
and hosts reproduce rather than requiring identical checkout permissions.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- workflow YAML parse
- `git diff --check`
- successful hosted Linux `Check` workflow for the pushed commit

## Boundaries

- Do not rewrite or normalize the preserved artifact.
- Do not change manifest values without updating the corresponding artifact.
