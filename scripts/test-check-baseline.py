#!/usr/bin/env python3
"""Hostile regression tests for the NSFar baseline checker."""

from contextlib import contextmanager
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
CHECKER_PATH = ROOT / "scripts/check-baseline.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("nsfar_check_baseline", CHECKER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@contextmanager
def repository_fixture():
    with tempfile.TemporaryDirectory() as temporary_directory:
        fixture = Path(temporary_directory) / "NSFar"
        shutil.copytree(
            ROOT,
            fixture,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )
        subprocess.run(
            ["git", "init", "--quiet"],
            cwd=fixture,
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "add", "--all"],
            cwd=fixture,
            check=True,
            capture_output=True,
            text=True,
        )
        yield fixture


def run_checker(fixture):
    return subprocess.run(
        [sys.executable, "scripts/check-baseline.py"],
        cwd=fixture,
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )


def assert_no_checker_traceback(test_case, result):
    test_case.assertNotIn('/NSFar/scripts/check-baseline.py", line', result.stderr)


class ManifestParserTests(unittest.TestCase):
    def test_excessive_nesting_is_reported_without_recursion_traceback(self):
        checker = load_checker()
        nested_manifest = "[" * 2000 + "0" + "]" * 2000

        manifest, error = checker.parse_manifest(nested_manifest)

        self.assertIsNone(manifest)
        self.assertEqual(error, "maximum JSON nesting depth exceeded")


class GitIndexProbeTests(unittest.TestCase):
    def run_with_fake_git(self, script):
        checker = load_checker()
        with tempfile.TemporaryDirectory() as temporary_directory:
            fake_git = Path(temporary_directory) / "git"
            fake_git.write_bytes(b"#!/bin/sh\n" + script)
            fake_git.chmod(0o755)
            with mock.patch.dict(
                os.environ,
                {"PATH": temporary_directory + os.pathsep + os.environ["PATH"]},
            ):
                return checker.read_indexed_mode("gitfiti")

    def test_whitespace_only_git_output_is_a_controlled_failure(self):
        mode, error = self.run_with_fake_git(b"printf '   \\n'\n")

        self.assertEqual(mode, "")
        self.assertEqual(error, "git index probe returned malformed output")

    def test_unmerged_git_stage_is_a_controlled_failure(self):
        mode, error = self.run_with_fake_git(
            b"printf '100644 0123456789012345678901234567890123456789 2\\tgitfiti\\n'\n"
        )

        self.assertEqual(mode, "")
        self.assertEqual(error, "git index probe returned malformed output")

    def test_non_utf8_git_output_is_a_controlled_failure(self):
        mode, error = self.run_with_fake_git(b"printf '\\377'\n")

        self.assertEqual(mode, "")
        self.assertEqual(error, "git index probe returned undecodable output")


class HostileRepositoryFixtureTests(unittest.TestCase):
    def test_duplicate_checkout_with_mapping_is_rejected(self):
        with repository_fixture() as fixture:
            baseline = run_checker(fixture)
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            workflow_path = fixture / ".github/workflows/check.yml"
            workflow = workflow_path.read_text(encoding="utf-8")
            workflow = workflow.replace(
                "        with:\n          persist-credentials: false\n",
                "        with:\n"
                "          persist-credentials: false\n"
                "        with:\n"
                "          fetch-depth: 1\n",
                1,
            )
            workflow_path.write_text(workflow, encoding="utf-8")

            result = run_checker(fixture)

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "checkout step must contain exactly one with mapping",
            result.stderr,
        )
        assert_no_checker_traceback(self, result)

    def test_quoted_duplicate_checkout_with_mapping_is_rejected(self):
        with repository_fixture() as fixture:
            baseline = run_checker(fixture)
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            workflow_path = fixture / ".github/workflows/check.yml"
            workflow = workflow_path.read_text(encoding="utf-8")
            workflow = workflow.replace(
                "        with:\n          persist-credentials: false\n",
                "        with:\n"
                "          persist-credentials: false\n"
                "        \"with\":\n"
                "          fetch-depth: 1\n",
                1,
            )
            workflow_path.write_text(workflow, encoding="utf-8")

            result = run_checker(fixture)

        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "checkout step must contain only the credential-free with mapping",
            result.stderr,
        )
        assert_no_checker_traceback(self, result)

    def test_missing_workflow_directory_is_reported_without_traceback(self):
        with repository_fixture() as fixture:
            baseline = run_checker(fixture)
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            shutil.rmtree(fixture / ".github/workflows")

            result = run_checker(fixture)

        self.assertEqual(result.returncode, 1)
        self.assertIn("workflow inventory could not be read", result.stderr)
        assert_no_checker_traceback(self, result)


if __name__ == "__main__":
    unittest.main()
