# Artifact Line Endings Plan

status: completed

## Context

`gitfiti` is preserved as a byte-sensitive numeric artifact. The manifest
already records checksum, line count, value range, and value counts, but it did
not record whether the artifact uses LF line endings or keeps a terminal
newline.

## Objectives

- Preserve the existing artifact bytes and checksum.
- Record LF line ending metadata in the `lineEnding` manifest field.
- Record that the artifact has a terminal newline.
- Extend `make check` so line ending metadata must match the artifact bytes.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
