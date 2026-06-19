---
title: Manifest Value Type Closure
status: completed
date: 2026-06-16
---

# Manifest Value Type Closure

## Priority

P2 archive integrity. JSON booleans and floating-point values can compare equal
to expected Python integers, allowing type-invalid schema values to pass the
manifest baseline.

## Problem

The checker compares decoded manifest values with Python `!=`. In Python,
`True == 1` and `2889.0 == 2889`, so fields such as `schemaVersion`, counts, or
nested histogram values are not constrained to their documented JSON types.

## Approach

- Add one recursive JSON comparator that requires exact container and scalar
  types as well as equal values.
- Use it for every derived manifest field, including nested lists and maps.
- Add focused self-contracts for boolean/integer, float/integer, list, and map
  distinctions.
- Preserve the protected artifact, schema version 1 manifest bytes, workflow,
  Makefile, and all existing controlled diagnostics.

## Files

- `scripts/check-baseline.py`
- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`
- `docs/plans/2026-06-16-manifest-value-type-closure.md`

## Verification

- Reproduce acceptance of `schemaVersion: true` before the fix in a disposable
  initialized repository.
- Prove boolean-for-integer, float-for-integer, and nested histogram type drift
  fail cleanly without traceback output after the fix.
- Run all repository and external-directory Make gates.
- Reject isolated comparator, call-site, self-contract, guidance, protected
  hash, and completed-plan mutations.
- Audit exact diff, protected hashes and modes, generated artifacts,
  credentials, conflicts, binaries, large files, modes, and whitespace.

## Scope Boundaries

- Do not alter `gitfiti`, `docs/artifact-manifest.json`, schema version, derived
  values, workflow, Makefile, or artifact provenance claims.
- Do not add a JSON Schema dependency or redesign the repository-local manifest.
- Keep PR #10 and its predecessors open and retain base-first stack ordering.

## Success Criteria

- Every manifest field must match both the expected JSON value and exact JSON
  type, recursively through arrays and objects.
- Valid schema version 1 evidence and all controlled diagnostics remain stable.

## Work Completed

- Added one recursive comparator that requires exact scalar and container types
  before comparing values.
- Applied strict comparison to the schema version and every derived manifest
  value, including nested arrays and histograms.
- Added focused comparator self-contracts, mutation-sensitive call-site
  contracts, maintained guidance, and changelog evidence.

## Verification Completed

- A disposable initialized repository reproduced that `schemaVersion: true`
  passed before strict comparison.
- Boolean-for-integer, float-for-integer, and nested histogram float mutations
  now return status 1 without a traceback.
- All four Make gates passed from the repository root and an external directory.
- Ten isolated hostile mutations were rejected across runtime type drift,
  comparator behavior, both production call sites, guidance, changelog, and the
  protected artifact hash.
- Python checker compilation, exact diff, protected artifact and manifest hash
  and mode, generated artifact, credential, conflict marker, binary, large-file,
  mode, and whitespace audits passed.
