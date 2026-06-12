# Manifest Sequence Shape

status: completed

## Context

The artifact checksum protects exact bytes and the manifest describes value
counts, but neither metadata surface explains the sequence's visible structure.
The rows form zero-based ascending runs, making run boundaries and lengths a
useful independently derived invariant for archive review.

## Objectives

- Record the zero-based ascending-run sequence pattern in the manifest.
- Derive and check the run count, minimum and maximum run lengths, and
  `runLengthCounts` histogram from the preserved artifact.
- Keep the existing checksum, line-count, value-count, boundary-value,
  line-ending, and file-mode guards intact.
- Document the sequence-shape preservation contract.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
