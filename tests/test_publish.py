"""Test publishing without sending requests or using real credentials."""

import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "publish", Path(__file__).resolve().parents[1] / "scripts" / "publish.py"
)
publish = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(publish)


class PublishingTests(unittest.TestCase):
    def test_tokens_are_read_as_data(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / ".creds"
            path.write_text(
                'unrelated text\nPYPI_API_TOKEN="pypi-$(false)"\n'
                "TESTPYPI_API_TOKEN='pypi-test'\n"
            )
            self.assertEqual(
                publish.read_token(path, "PYPI_API_TOKEN"), "pypi-$(false)"
            )
            self.assertEqual(
                publish.read_token(path, "TESTPYPI_API_TOKEN"), "pypi-test"
            )

    def test_invalid_credentials_do_not_leak(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / ".creds"
            for contents in [
                "private-value",
                "PYPI_API_TOKEN=private-value",
                "PYPI_API_TOKEN=pypi-secret\nPYPI_API_TOKEN=pypi-secret",
            ]:
                path.write_text(contents)
                with self.assertRaises(ValueError) as caught:
                    publish.read_token(path, "PYPI_API_TOKEN")
                self.assertNotIn("private-value", str(caught.exception))
                self.assertNotIn("pypi-secret", str(caught.exception))
            with self.assertRaises(ValueError):
                publish.read_token(Path(folder) / "missing", "PYPI_API_TOKEN")

    def test_upload_routes_token_and_propagates_failure(self):
        for repository, (key, url) in publish.REPOSITORIES.items():
            with (
                self.subTest(repository=repository),
                patch.object(publish, "read_token", return_value="pypi-fake") as read,
                patch.object(
                    publish.Path,
                    "glob",
                    side_effect=[
                        [Path("dist/package.whl")],
                        [Path("dist/package.tar.gz")],
                    ]
                    * 2,
                ),
                patch.object(publish.subprocess, "run") as run,
                patch.dict(os.environ, {"TWINE_PASSWORD": "wrong-token"}),
            ):
                run.return_value.returncode = 7
                self.assertEqual(publish.main([repository]), 7)
                read.assert_called_once_with(Path(".creds"), key)
                command = run.call_args.args[0]
                self.assertIn(url, command)
                self.assertNotIn("pypi-fake", command)
                self.assertEqual(
                    run.call_args.kwargs["env"]["TWINE_PASSWORD"], "pypi-fake"
                )
                self.assertEqual(
                    run.call_args.kwargs["env"]["TWINE_USERNAME"], "__token__"
                )
                self.assertNotIn("--verbose", command)
                self.assertEqual(publish.main([repository, "--verbose"]), 7)
                self.assertIn("--verbose", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
