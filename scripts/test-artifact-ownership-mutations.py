#!/usr/bin/env python3
"""Require artifact ownership checks to reject isolated hostile changes."""

from pathlib import Path
import os
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = [
    (
        "path-lstat",
        "scripts/check-baseline.py",
        "path_stat = path.lstat()",
        "path_stat = path.stat()",
    ),
    (
        "read-no-follow",
        "scripts/check-baseline.py",
        "os.O_RDONLY | os.O_NOFOLLOW",
        "os.O_RDONLY",
    ),
    (
        "single-link-check",
        "scripts/check-baseline.py",
        "path_stat.st_nlink != 1",
        "False",
    ),
    (
        "descriptor-identity",
        "scripts/check-baseline.py",
        "!= (path_stat.st_dev, path_stat.st_ino)",
        "== (path_stat.st_dev, path_stat.st_ino)",
    ),
    (
        "regression-test",
        "scripts/test-check-baseline.py",
        "test_hard_link_artifact_is_rejected",
        "removed_hard_link_artifact_regression",
    ),
    (
        "completed-plan",
        "docs/plans/2026-06-26-artifact-file-ownership.md",
        "status: completed",
        "status: in progress",
    ),
]


def copy_repository(destination):
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns(
            ".git", ".explore", "__pycache__", "*.pyc"
        ),
    )
    subprocess.run(["git", "init", "--quiet"], cwd=destination, check=True)
    subprocess.run(["git", "add", "--all"], cwd=destination, check=True)


def run_baseline(repository):
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, "scripts/check-baseline.py"],
        cwd=repository,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    ).returncode


def main():
    with tempfile.TemporaryDirectory(prefix="nsfar-artifact-mutations-") as temporary:
        seed = Path(temporary) / "seed"
        copy_repository(seed)
        if run_baseline(seed) != 0:
            raise SystemExit("unmodified mutation fixture must pass the static baseline")

        for name, relative_path, original, replacement in MUTATIONS:
            fixture = Path(temporary) / name
            shutil.copytree(seed, fixture)
            path = fixture / relative_path
            contents = path.read_text(encoding="utf-8")
            if contents.count(original) != 1:
                raise SystemExit(f"mutation source must occur exactly once: {name}")
            path.write_text(contents.replace(original, replacement), encoding="utf-8")
            if run_baseline(fixture) == 0:
                raise SystemExit(f"mutation survived: {name}")
            print(f"Rejected mutation: {name}")

    print("Artifact ownership mutation tests passed for 6 hostile changes.")


if __name__ == "__main__":
    main()
