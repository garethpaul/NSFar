# Manifest Schema Version Plan

status: completed

## Context

The artifact manifest records derived metadata for the preserved `gitfiti`
file, but its JSON shape did not identify a schema version.

## Objectives

- Add `schemaVersion` 1 to `docs/artifact-manifest.json`.
- Extend `make check` so the schema version cannot be removed silently.
- Document the schema version in the archive docs.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
