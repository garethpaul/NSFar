# Unreadable Artifact Diagnostics

status: completed

## Summary

Keep the artifact checker on its controlled nonzero diagnostic path when the
protected `gitfiti` file exists but cannot be read.

## Problem

The missing-file boundary substitutes empty bytes when `gitfiti` is absent,
but an existing file can still fail during `Path.read_bytes()` because of
permissions or transient filesystem errors. That `OSError` currently escapes
as a Python traceback and prevents independent repository findings from being
reported.

## Requirements

- Convert protected-artifact byte-read failures into a named checker finding.
- Continue checksum, mode, line-ending, row, manifest, documentation, and SVG
  checks using empty bytes after the read failure.
- Preserve existing missing-file and git-index-probe diagnostics.
- Leave `gitfiti` and `docs/artifact-manifest.json` byte-for-byte unchanged.
- Add mutation-sensitive static and disposable runtime evidence.

## Implementation

- Add a small protected-artifact reader that returns bytes plus an optional
  diagnostic and catches `OSError` only around `read_bytes()`.
- Record the diagnostic before running every existing artifact and repository
  contract.
- Document the controlled unreadable-artifact path in all maintenance guidance.

## Verification

- Run every Make gate and external-directory `make check`.
- In a disposable checkout, remove read permissions from `gitfiti`; require
  status 1, a named read diagnostic, no traceback, and independent checksum and
  row findings.
- Reject isolated mutations of the exception boundary, helper use, diagnostic,
  documentation, protected hashes, and completed-plan evidence.
- Audit exact diff, whitespace, generated artifacts, conflict markers,
  intended paths, binary/large files, changed-line credentials, and protected
  artifact/manifest hashes and modes.

## Risks

- This does not repair filesystem permissions or I/O failures; it makes them
  deterministic and diagnosable.
- The change must remain stacked on PR #9 and no pull request may be merged or
  closed without explicit owner authorization.

## Success Criteria

- An unreadable protected artifact returns status 1 without a traceback.
- The diagnostic names the protected artifact read failure.
- Independent integrity findings continue to run.

## Work Completed

- Added a guarded protected-artifact byte reader that converts `OSError` into a
  named checker finding and empty bytes.
- Preserved every existing checksum, mode, line-ending, row, manifest,
  documentation, and SVG check after a read failure.
- Added synchronized maintenance guidance and mutation-sensitive plan/static
  contracts.

## Verification Completed

- A disposable unreadable `gitfiti` reproduction returned status 1 with a
  named artifact-read diagnostic and without a traceback; independent checksum
  and row findings were also reported.
- `python3 -m py_compile scripts/check-baseline.py`, `make lint`, `make test`,
  `make build`, and `make check` passed.
- `make check` passed from an external working directory through the absolute
  Makefile path.
- Six isolated hostile mutations of the exception boundary, helper use,
  diagnostic, guidance, protected hashes, and completed-plan evidence were
  rejected.
- `git diff --check`, exact six-file diff, generated-artifact, conflict-marker,
  intended-path, binary, large-file, changed-line credential, and protected
  artifact/manifest hash and mode audits passed.
