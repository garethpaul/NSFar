# Git Probe Diagnostics

status: planned

## Summary

Keep the artifact checker on its controlled nonzero diagnostic path when the
`git ls-files` tracked-mode probe cannot start.

## Problem

The checker validates the protected artifact's indexed mode by launching
`git`. If that executable is unavailable or the process cannot start,
`subprocess.run` raises `OSError` and replaces the repository findings with a
Python traceback.

## Requirements

- Convert tracked-mode probe startup failures into a named checker failure.
- Preserve the existing nonzero-exit and indexed `100644` mode checks.
- Continue all independent artifact, manifest, documentation, and SVG checks.
- Leave `gitfiti` and `docs/artifact-manifest.json` byte-for-byte unchanged.
- Add mutation-sensitive static and runtime evidence for the controlled path.

## Implementation

- Move the `git ls-files --stage -- gitfiti` invocation behind a small helper
  that returns no mode and a diagnostic when process creation raises
  `OSError`.
- Keep successful probe parsing and validation behavior unchanged.
- Document the controlled diagnostic in repository guidance and checker
  maintenance contracts.

## Verification

- Run every Make gate and external-directory `make check`.
- Invoke the checker with an absolute Python interpreter and a `PATH` that has
  no `git`; require status 1, a named git-probe diagnostic, and no traceback.
- Reject isolated mutations of the exception boundary, helper use,
  documentation, protected hashes, and completed-plan evidence.
- Audit exact diff, whitespace, generated artifacts, conflict markers,
  intended paths, binary/large files, changed-line credentials, and protected
  artifact/manifest hashes and modes.

## Risks

- This does not make Git optional for a passing check; it makes an unavailable
  probe deterministic and diagnosable.
- The change must remain stacked on PR #8 and must not be merged or closed
  without explicit owner authorization.
