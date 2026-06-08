# NSFar Artifact Baseline Plan

status: completed

## Context

`NSFar` is a sparse repository with one checked-in artifact named `gitfiti`.
The artifact is a 2,889-line numeric file containing integer rows in the range
0 through 17.

## Risks

- The repository did not explain the artifact shape.
- Future changes could accidentally rewrite the artifact without provenance.
- There was no verification command for the archive.

## Work Completed

- Documented the artifact as preserved numeric data rather than an installable
  runtime.
- Added `make check` and `scripts/check-baseline.py` to verify the artifact
  shape, docs, and overview XML.
- Added local ignore rules for environment files, logs, and temporary output.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
