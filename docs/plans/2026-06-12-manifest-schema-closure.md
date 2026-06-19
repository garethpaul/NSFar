# Manifest Schema Closure

status: completed

## Context

The artifact checker derives and validates every documented manifest value, but
it currently ignores unexpected top-level keys. That allows misspelled,
obsolete, or undocumented metadata to remain in `artifact-manifest.json` even
though schema version 1 is intended to be an explicit archive contract.

## Objectives

- Require the manifest's top-level key set to match the schema version 1
  contract exactly.
- Report missing and unexpected keys clearly enough to diagnose manifest drift.
- Preserve the `gitfiti` artifact bytes and all existing checksum, sequence,
  file-mode, and line-ending checks.
- Document that schema version changes must deliberately update the accepted
  manifest key set.

## Verification

- `make lint` passed on 2026-06-12.
- `make test` passed on 2026-06-12.
- `make build` passed on 2026-06-12.
- `make check` passed on 2026-06-12.
- `make check` rejected a temporary `unexpectedValidationProbe` field as an
  unexpected manifest key on 2026-06-12.
- `make check` rejected a temporarily removed `bytes` field as a missing
  schema key on 2026-06-12.
- `git diff --check` passed on 2026-06-12.
