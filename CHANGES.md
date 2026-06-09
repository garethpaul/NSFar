# Changes

## 2026-06-08

- Documented the checked-in `gitfiti` file as a preserved numeric artifact.
- Added `make check` static verification for the artifact line count and value
  range plus a SHA-256 checksum guard.
- Added a checked artifact manifest for path, size, line count, value range,
  value counts, encoding, format, and checksum metadata.
- Added a checked schema version to the artifact manifest.
- Added checked line ending and terminal newline metadata to the artifact
  manifest.
- Added local ignore rules for environment files, logs, and temporary output.
