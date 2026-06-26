# Artifact File Ownership Boundary

status: completed

## Problem

The checker validated `gitfiti` bytes, staged mode, and manifest metadata but
used path-following `is_file()` and `read_bytes()` calls. An exact-content
symbolic link or hard link to an external inode therefore passed every artifact
integrity assertion.

## Requirements

1. Reject symbolic-link and multiply linked artifact paths before hashing.
2. Open the artifact with no-follow semantics and compare path and descriptor
   device/inode identity.
3. Preserve controlled diagnostics for missing, unreadable, or swapped files.
4. Leave the protected artifact and schema-version-1 manifest byte-for-byte
   unchanged.
5. Add focused fixtures, static contracts, hostile mutations, and full hosted
   verification.

## Work Completed

- Added singly linked regular-file admission before artifact reads.
- Added no-follow descriptor opening and path/descriptor identity validation.
- Added exact-content symbolic-link and hard-link repository fixtures.
- Added six isolated mutations covering every new guard and its durable evidence.
- Updated maintainer, security, direction, and changelog guidance.

## Verification Completed

- All 15 focused tests passed after the two alias regressions first failed.
- The static baseline rejected six isolated hostile mutations covering path
  following, no-follow removal, single-link removal, descriptor identity,
  removed regression coverage, and incomplete plan status.
- `make check` passed from the repository root and an external working directory.
- `gitfiti` and `docs/artifact-manifest.json` remained byte-for-byte unchanged;
  `git diff --check`, strict Git validation, generated-artifact checks, and
  secret/conflict scans passed before review.
