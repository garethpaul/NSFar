# Safe Make Root

status: completed

## Problem

Whitespace-splitting Make functions and caller-controlled `MAKEFILE_LIST`
values could redirect verification away from the provenance-sensitive artifact.

## Change

- Resolve the raw Makefile path with POSIX-compatible system tooling.
- Reject non-file origins for GNU Make's automatic `MAKEFILE_LIST` value.
- Add non-mutating regressions for spaces, a literal apostrophe, all six Make
  aliases, root overrides, and both `MAKEFILE_LIST` injection channels.

## Validation

- Run artifact integrity, manifest, ten hostile mutation, and root-policy
  checks from the repository and an unrelated directory.
- Confirm pinned Ubuntu CI and CodeQL pass at the exact pull-request head.
