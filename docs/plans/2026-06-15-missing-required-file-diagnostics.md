# Missing Required File Diagnostics

status: in progress

## Summary

Keep the artifact checker on its controlled nonzero diagnostic path when a
required text file, protected artifact, or SVG is absent.

## Problem

The checker first records missing required paths, but later unguarded reads and
XML parsing can raise `OSError`. A damaged checkout can therefore emit a Python
traceback before the checker reports all independent repository findings.

## Requirements

- Return empty text after a required text-file read failure so existing content
  contracts continue to report deterministic findings.
- Use empty artifact bytes only after recording that the protected artifact is
  missing; preserve every checksum, mode, line-ending, row, and manifest check.
- Treat missing or unreadable SVG input as a controlled validation failure.
- Leave `gitfiti` and `docs/artifact-manifest.json` byte-for-byte unchanged.
- Add mutation-sensitive contracts and maintenance documentation.

## Implementation

- Catch `OSError` in the repository text reader and return an empty string.
- Guard the protected artifact byte read with `is_file()`.
- Extend the SVG parser boundary to catch `OSError` beside parse failures.
- Add completed evidence for disposable missing artifact, manifest, README, and
  SVG reproductions.

## Verification

- Run all Make gates and external-directory `make check`.
- Verify disposable missing-file reproductions return status 1 without a
  traceback and name the missing path.
- Reject isolated mutations of the text-read guard, artifact guard, SVG guard,
  documentation, protected hashes, and completed-plan evidence.
- Audit exact diff, whitespace, generated artifacts, conflict markers,
  intended paths, binary/large files, changed-line credentials, and protected
  artifact/manifest hashes and modes.

## Risks

- This does not repair missing files; it only preserves controlled diagnostics
  and independent checks.
- The change must remain stacked on PR #7 and must not be merged or closed
  without explicit owner authorization.

## Verification Completed

Pending implementation and validation.
