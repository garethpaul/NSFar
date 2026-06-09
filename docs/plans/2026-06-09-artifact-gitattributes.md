# Artifact Gitattributes Plan

status: completed

## Context

`gitfiti` is guarded as a byte-sensitive numeric artifact with LF line endings
and a terminal newline. The checker catches line-ending drift after it happens,
but the repository did not have `.gitattributes` rules to guide checkout and
normalization behavior.

## Objectives

- Add `.gitattributes` rules that pin `gitfiti` to LF line endings.
- Pin `docs/artifact-manifest.json` to LF line endings as archive metadata.
- Extend `make check` so the line-ending attributes cannot be removed silently.
- Document the repository-level line-ending policy for maintainers.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
