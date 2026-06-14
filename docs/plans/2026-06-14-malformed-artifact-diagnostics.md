# Malformed Artifact Diagnostics

status: completed

## Context

The checker records a controlled failure when `gitfiti` contains a non-integer
or out-of-range row, but then unconditionally converts every row with `int()`.
A malformed artifact therefore raises a traceback instead of completing the
validation report. That obscures the intended integrity diagnostic and can
mask later independent failures.

## Priorities

1. Return a normal nonzero checker result for malformed artifact rows without a
   traceback.
2. Preserve all existing valid-artifact sequence and manifest checks.
3. Leave `gitfiti` and `docs/artifact-manifest.json` byte-for-byte unchanged.
4. Add a deterministic malformed-input self-contract and hostile mutation
   coverage.

## Implementation Units

### Value Parser

File: `scripts/check-baseline.py`

- Parse rows through one helper that returns invalid rows without raising.
- Run sequence and value-derived manifest checks only when every row is valid.
- Continue fixed schema, documentation, workflow, and repository checks after
  malformed input is found.

### Regression Contract

File: `scripts/check-baseline.py`

- Exercise representative non-integer and out-of-range rows in memory.
- Require controlled invalid-row results and no partially trusted value list.
- Require completed plan evidence in the active checker.

### Documentation

Files: `README.md`, `SECURITY.md`, `VISION.md`, `CHANGES.md`

- Document that malformed artifact rows fail cleanly without traceback output.

## Work Completed

- Added an all-or-nothing artifact value parser that returns invalid rows
  without exposing partially trusted values.
- Guarded sequence and value-derived manifest calculations behind successful
  row validation while preserving fixed schema and repository checks.
- Added in-memory contracts for valid, non-integer, and out-of-range rows.
- Documented controlled malformed-row diagnostics without changing the
  protected artifact or schema version 1 manifest.

## Verification Completed

- A disposable indexed copy containing `not-an-integer` returned a
  controlled nonzero result without a traceback and reported checksum,
  row-domain, and manifest-byte failures.
- `python3 -m py_compile scripts/check-baseline.py` passed.
- `make lint`, `make test`, `make build`, and `make check` passed.
- The checker passed from an external working directory through the absolute
  Makefile path.
- Five isolated hostile mutations removing all-or-nothing parsing, invalid-row
  self-coverage, guarded value derivation, documentation, or completed plan
  evidence were rejected.
- `gitfiti` and `docs/artifact-manifest.json` remained byte-for-byte unchanged.
- `git diff --check` passed.

## Boundaries

- Do not change or infer the artifact, generator, source instructions, or
  intended rendered pattern.
- Do not change manifest schema version 1 or add derived fields.
