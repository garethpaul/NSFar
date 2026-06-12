# Changes

## 2026-06-12

- Disabled persisted checkout credentials and enforced the sole pinned
  credential-free workflow boundary.
- Closed the schema version 1 artifact manifest to its exact top-level key set
  so missing, misspelled, obsolete, or undocumented fields fail validation.

## 2026-06-10

- Added pinned, read-only Python 3.12 hosted validation for artifact and
  manifest integrity.
- Corrected file mode validation to inspect Git's tracked mode instead of
  checkout permissions that can vary with the local umask.
- Added checked `valueCountTotal` metadata to the artifact manifest so the
  histogram total stays aligned with the preserved line count.
- Added checked sequence-shape metadata for the artifact's 318 zero-based
  ascending runs, including its run-length histogram.

## 2026-06-08

- Documented the checked-in `gitfiti` file as a preserved numeric artifact.
- Added `make check` static verification for the artifact line count and value
  range plus a SHA-256 checksum guard.
- Added a checked artifact manifest for path, size, line count, value range,
  value counts, encoding, format, and checksum metadata.
- Added a checked schema version to the artifact manifest.
- Added checked line ending and terminal newline metadata to the artifact
  manifest.
- Added checked non-executable file mode metadata to the artifact manifest.
- Added `.gitattributes` LF rules for the byte-sensitive artifact and manifest.
- Added checked distinct values metadata to the artifact manifest.
- Added `make lint`, `make test`, and `make build` aliases so the standard
  gate commands run the same SDK-free static baseline as `make check`.
- Added local ignore rules for environment files, logs, and temporary output.
- Added checked first and last value metadata to the artifact manifest.
