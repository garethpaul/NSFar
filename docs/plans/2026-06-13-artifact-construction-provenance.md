# Artifact Construction Provenance

status: planned

## Context

The repository preserves `gitfiti` byte-for-byte and records its shape in a
machine-readable manifest, but the documentation still describes its
provenance as unknown. The local Git history contains bounded construction
evidence that can narrow that uncertainty without claiming a missing generator
or intended rendered design.

## Priorities

1. Record reproducible commit-history evidence for the artifact's construction.
2. Separate established history facts from unresolved purpose and generator
   questions.
3. Keep the schema version 1 manifest and artifact bytes unchanged.
4. Protect the provenance note and its uncertainty boundary with static checks.

## Implementation Units

### Provenance Note

File: `docs/artifact-provenance.md`

Record the exact number and shape of commits that built `gitfiti`, representative
first and last commits, author-date range, and commands used to derive the
evidence. State explicitly that the generator, source instructions, and
intended rendered pattern are not present in the repository.

### Archive Documentation

Files:

- `README.md`
- `SECURITY.md`
- `VISION.md`
- `CHANGES.md`

Link the provenance note, distinguish construction history from reproducible
generation, and retain the no-rewrite boundary.

### Static Contract

Files:

- `scripts/check-baseline.py`
- `docs/plans/2026-06-13-artifact-construction-provenance.md`

Require the provenance evidence, unresolved fields, unchanged manifest schema,
completed plan, and verification record without requiring full Git history in
the shallow hosted checkout.

## Verification Plan

- rerun bounded local Git-history queries for commit count, numstat shape,
  representative commits, and author-date range
- `python3 -m py_compile scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- run the checker outside the repository working directory
- parse the workflow YAML and artifact manifest JSON
- run focused hostile mutations against the provenance contracts
- verify `gitfiti` and `docs/artifact-manifest.json` have no diff
- `git diff --check`
- scan the intended diff for secrets and generated artifacts

## Boundaries

- Do not infer an intended image, message, generator, or source instructions.
- Do not change `gitfiti` or `docs/artifact-manifest.json`.
- Do not add manifest provenance fields until their schema and source are
  deliberately defined.
- Do not make hosted validation depend on repository history depth.
