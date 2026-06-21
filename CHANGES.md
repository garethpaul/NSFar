# Changes

## 2026-06-21

- Made absolute Makefile artifact verification safe for spaces and apostrophes
  and rejected `MAKEFILE_LIST` injection.
- Expanded the hostile suite to ten tests covering all six Make aliases, root
  overrides, and command-line or environment `MAKEFILE_LIST` injection.
- Rejected `MAKEFILES` preloads, froze the artifact verifier interpreter and
  shell, and preserved relative trusted Makefiles after inert earlier `-f`
  inputs.

## 2026-06-19

- Added checked-in hostile regression tests for malformed manifest nesting,
  malformed or undecodable Git index output, missing workflow directories, and
  duplicate checkout mappings.
- Tightened checkout validation so duplicate YAML `with` mappings cannot hide
  the credential-free checkout input from the effective workflow structure.
- Made excessive JSON nesting and malformed Git index records fail with
  controlled diagnostics instead of tracebacks or ambiguous tracked modes.

## 2026-06-17

- Added manifest duplicate-key rejection at every JSON object depth so
  ambiguous metadata cannot pass exact schema and value validation.

## 2026-06-16

- Added manifest value type closure so boolean and floating-point substitutions
  cannot satisfy integer schema fields or nested derived metadata.

## 2026-06-15

- Made missing required files fail cleanly without traceback output while
  independent artifact and repository diagnostics continue.
- Made Git index probe failures fail cleanly without traceback output while
  tracked-mode and independent repository diagnostics continue.
- Made unreadable protected artifacts fail cleanly without traceback output
  while checksum, row, and independent repository diagnostics continue.

## 2026-06-14

- Made malformed artifact manifests fail cleanly without traceback output,
  including non-object JSON, while independent checker findings continue.
- Made malformed or out-of-range artifact rows return controlled integrity
  diagnostics instead of crashing the checker during integer conversion.

## 2026-06-13

- Made every dependency-free Make alias resolve the static checker from the
  checkout when the Makefile is invoked by absolute path.
- Documented that 2,889 one-line-addition commits constructed the preserved
  artifact while leaving its generator and intended rendered pattern unresolved.

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
