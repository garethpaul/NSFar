# Artifact Manifest

status: completed

## Context

`NSFar` preserves a single numeric artifact named `gitfiti`. The static checker
already protects its checksum, line count, and value range, but the metadata
was only available in prose and checker constants.

## Objectives

- Add a machine-readable artifact manifest at `docs/artifact-manifest.json`.
- Record the artifact path, byte size, line count, value range, value counts,
  encoding, format, and SHA-256 checksum.
- Extend `make check` so the manifest must match the checked-in artifact bytes.
- Document the manifest in README, security, vision, and changes.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
