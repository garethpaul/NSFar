# Safe Make Root

status: completed

## Problem

Whitespace-splitting Make functions and caller-controlled `MAKEFILE_LIST`
values could redirect verification away from the provenance-sensitive artifact.

## Change

- Resolve the final existing trusted Makefile suffix without splitting spaces,
  including after an inert earlier `-f` input.
- Reject non-file origins for GNU Make's automatic `MAKEFILE_LIST` value.
- Reject `MAKEFILES` preloads and freeze the shell, Python artifact verifier,
  and derived root on every public target.
- Add non-mutating regressions for spaces, a literal apostrophe, all six Make
  aliases, root and interpreter overrides, preload injection, earlier `-f`
  inputs, and both `MAKEFILE_LIST` injection channels.

## Validation

- Run artifact integrity, manifest, thirteen hostile mutation, and root-policy
  checks from the repository and an unrelated directory.
- Confirm pinned Ubuntu CI and CodeQL pass at the exact pull-request head.
