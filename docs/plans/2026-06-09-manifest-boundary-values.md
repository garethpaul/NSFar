# Manifest Boundary Values

status: completed

## Context

The `gitfiti` artifact is preserved by checksum and has manifest metadata for
line count, value range, distinct values, and value counts. The manifest did
not expose the first and last observed values, which are useful review hints
when checking sequence-edge changes without opening the full artifact.

## Objectives

- Add `firstValue` and `lastValue` to `docs/artifact-manifest.json`.
- Derive the boundary values from the checked-in artifact in the static
  checker.
- Keep the existing checksum, line-count, line-ending, file-mode, value-count,
  and distinct-value guards intact.
- Document the boundary-value preservation contract in the repository docs.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
