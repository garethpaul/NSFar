# Manifest Value Count Total

status: completed

## Context

The artifact manifest records `lineCount` and a `valueCounts` histogram for the
preserved `gitfiti` file. A compact total derived from the histogram makes it
easy to confirm that value counts account for every artifact line without
manually summing the histogram.

## Objectives

- Add `valueCountTotal` to `docs/artifact-manifest.json`.
- Derive `valueCountTotal` from the checked-in artifact in the static checker.
- Keep the existing checksum, line-count, value-count, boundary-value,
  line-ending, and file-mode guards intact.
- Document the value-count total preservation contract.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
