# Artifact Construction Provenance

status: completed

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

## Work Completed

- Added a provenance note that separates established repository construction
  history from unresolved generator, source-instruction, and intended-pattern
  questions.
- Recorded representative first and last commits, author/committer date range,
  linear-history shape, and reproducible local audit commands.
- Linked the provenance boundary from archive, security, vision, and changelog
  guidance.
- Added static contracts without changing the protected artifact or schema
  version 1 manifest.

## Verification Completed

Completed locally on 2026-06-13:

- `git rev-list --count HEAD -- gitfiti` reported 2,889 commits
- numstat aggregation reported 2,889 additions and zero deletions across 2,889
  rows, with every row shaped as one addition and no deletion
- all 2,889 subjects were `gitfiti`, one author identity was observed, the
  author-date range was `2013-12-08T12:00:00-08:00` through
  `2014-11-29T12:00:00-08:00`, and the history had one root and no merges
- representative commits `425882d4734218b7fc5b5f672611d671b22c93b7`
  and `5b41cbeb9e52af1e0ac449b779b8ff06c212f4f1` matched the documented first and
  final one-line additions
- `python3 -m py_compile scripts/check-baseline.py`
- `make lint`
- `make test`
- `make build`
- `make check`
- artifact manifest JSON and workflow YAML parsed successfully
- the checker passed from an external working directory
- eight focused hostile mutations rejected completed-provenance claims,
  incorrect counts, missing commit evidence, erased uncertainty, manifest
  schema drift, a stale README link, incomplete status, and unfinished evidence
- `gitfiti` and `docs/artifact-manifest.json` had no diff
- `git diff --check`

The Make gates and hostile mutation suite first passed against a disposable
indexed copy with completed-plan evidence. The complete gates were then rerun
against this completed plan in the repository worktree.

## Boundaries

- Do not infer an intended image, message, generator, or source instructions.
- Do not change `gitfiti` or `docs/artifact-manifest.json`.
- Do not add manifest provenance fields until their schema and source are
  deliberately defined.
- Do not make hosted validation depend on repository history depth.
