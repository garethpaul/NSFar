# Manifest Schema Closure

status: planned

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

- `make lint`
- `make test`
- `make build`
- `make check`
- A temporary unexpected manifest key is rejected by `make check`.
- `git diff --check`
