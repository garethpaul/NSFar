# Manifest Distinct Values

status: completed

## Context

The `gitfiti` artifact is a preserved newline-delimited integer file with a
known value range and value counts. The manifest recorded the minimum, maximum,
and count for each observed value, but it did not expose the complete observed
domain as a simple ordered list.

## Objectives

- Add `distinctValues` to `docs/artifact-manifest.json`.
- Derive the value from the checked-in artifact instead of hand-maintaining it.
- Extend the static checker so the manifest stays aligned with the artifact.
- Keep the existing checksum, line-ending, file-mode, and value-count guards.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
