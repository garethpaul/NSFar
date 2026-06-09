# Artifact File Mode Plan

status: completed

## Context

`gitfiti` is preserved as a byte-sensitive numeric artifact. The manifest
already records checksum, line count, value range, value counts, encoding, line
endings, and terminal newline state, but it did not record whether the artifact
is executable.

## Objectives

- Preserve the existing artifact bytes and checksum.
- Record the artifact as non-executable with `fileMode` `100644`.
- Extend `make check` so file mode metadata must match the checked-in artifact.
- Document the file mode guard in the archive docs.

## Verification

- `make check`
- `git diff --check`
