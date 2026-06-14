# Malformed Manifest Diagnostics

status: completed

## Context

The checker now reports malformed artifact rows without a traceback, but it
still loads `docs/artifact-manifest.json` through an unguarded `json.loads`.
Malformed JSON can therefore terminate validation before the checker reports
the independent artifact, documentation, workflow, and repository findings.

## Priorities

1. Report malformed manifest JSON as a controlled checker failure.
2. Continue independent fixed artifact and repository checks after the load
   failure.
3. Preserve all valid schema version 1 manifest behavior.
4. Leave `gitfiti` and `docs/artifact-manifest.json` byte-for-byte unchanged.

## Implementation Units

### Manifest Loader

File: `scripts/check-baseline.py`

- Parse manifest text through a helper that returns a diagnostic instead of
  raising.
- Require the decoded top-level value to be an object before schema checks.
- Use an empty object after a controlled load failure so fixed checks continue.

### Regression Contract

File: `scripts/check-baseline.py`

- Exercise malformed JSON, a non-object JSON value, and a valid object in
  memory.
- Require completed plan evidence and the safe loader call in the maintained
  checker.

### Documentation

Files: `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`

- Document controlled malformed-manifest diagnostics and the unchanged
  protected artifact boundary.

## Work Completed

- Added a safe manifest parser that rejects malformed JSON and non-object
  top-level values without raising.
- Continued schema and independent repository checks with an empty manifest
  only after recording the controlled load diagnostic.
- Added in-memory malformed, non-object, and valid-object fixtures plus static
  contracts requiring the real manifest path and fallback to use the loader.
- Documented controlled manifest diagnostics without modifying the protected
  artifact or schema version 1 manifest.

## Verification Completed

- Disposable malformed and non-object manifest fixtures each returned a
  controlled nonzero result without a traceback.
- `python3 -m py_compile scripts/check-baseline.py` passed.
- `make lint`, `make test`, `make build`, and `make check` passed.
- The checker passed from an external working directory through the absolute
  Makefile path.
- Five isolated hostile mutations of loader use, the non-object fixture, the
  type guard, the empty-manifest fallback, and documentation were rejected.
- Protected artifact and manifest hashes and tracked modes remained unchanged.
- `git diff --check`, generated-artifact, conflict-marker, and changed-line
  secret audits passed.

## Boundaries

- Do not modify the protected artifact or schema version 1 manifest.
- Do not infer a generator, source instructions, or rendered pattern.
- Do not weaken existing checksum, mode, line-ending, schema, or provenance
  checks.
