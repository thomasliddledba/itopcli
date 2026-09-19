"""Offline regression tests for CLI payloads and failures."""

import importlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from click.testing import CliRunner
import requests

app = importlib.import_module("itopcli_app.cli")


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def config(self, **overrides):
        values = dict(
            url="https://example.invalid",
            apisuffix="/webservices/rest.php",
            apiversion="1.3",
            username="test",
            password="p%ss",
            organization="7",
            timeout=10,
            verify_ssl=True,
        )
        values.update(overrides)
        app.ClientConfiguration().set(values)

    def test_quoted_query_and_key_precedence(self):
        self.assertEqual(
            app.build_query_key("Server", "name", "O'Brien\\host", 0),
            "SELECT Server WHERE name = 'O\\'Brien\\\\host'",
        )
        self.assertEqual(app.build_query_key("Server", "name", "*", 0), "SELECT Server")
        self.assertEqual(app.build_query_key("Server", "name", "O'Brien", 3), 3)
        with patch.object(app.requests, "post") as post:
            result = self.runner.invoke(
                app.cli,
                [
                    "query",
                    "--class",
                    "Server",
                    "--attribute",
                    "name",
                    "--criteria",
                    "O'Brien\\host",
                    "--dry-run",
                ],
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertEqual(
                json.loads(result.output)["key"],
                "SELECT Server WHERE name = 'O\\'Brien\\\\host'",
            )
            post.assert_not_called()

    def test_field_types_and_precedence(self):
        fields = app.merge_update_fields(
            ("cpu=8", "active=true", 'tags=["web"]', "empty=null", "label=a=b"),
            '{"cpu":2,"ram":32}',
        )
        self.assertEqual(
            fields,
            dict(cpu=8, active=True, tags=["web"], empty=None, label="a=b", ram=32),
        )

    def test_invalid_fields(self):
        for pairs, raw in [
            (("broken",), None),
            (("=value",), None),
            ((), "[]"),
            ((), "{"),
        ]:
            with self.subTest(pairs=pairs, raw=raw), self.assertRaises(app.ClientError):
                app.merge_update_fields(pairs, raw)

    def test_configuration_round_trip(self):
        with self.runner.isolated_filesystem():
            self.config()
            cfg = app.load_config(".itopcli")
            self.assertEqual(cfg.password, "p%ss")
            self.assertEqual(cfg.timeout, 10)
            self.assertTrue(cfg.verify_ssl)
            self.assertEqual(
                cfg.endpoint, "https://example.invalid/webservices/rest.php?version=1.3"
            )

    def test_configure_questionnaire(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(
                app.cli,
                ["configure"],
                input=(
                    "https://example.invalid\n\n\n7\n12\ntester\nhidden%secret\nn\ncustom.ini\n"
                ),
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertNotIn("hidden%secret", result.output)
            cfg = app.load_config("custom.ini")
            self.assertEqual(cfg.url, "https://example.invalid")
            self.assertEqual(cfg.apisuffix, "/webservices/rest.php")
            self.assertEqual(cfg.apiversion, "1.3")
            self.assertEqual(cfg.organization, "7")
            self.assertEqual(cfg.timeout, 12)
            self.assertEqual(cfg.username, "tester")
            self.assertEqual(cfg.password, "hidden%secret")
            self.assertFalse(cfg.verify_ssl)
            self.assertFalse(Path(".itopcli").exists())

    def test_configure_options_and_password_prompt(self):
        options = [
            "configure",
            "--url",
            "https://example.invalid",
            "--apisuffix",
            "/rest.php",
            "--apiversion",
            "1.2",
            "--username",
            "tester",
        ]
        with self.runner.isolated_filesystem():
            with patch.object(app.click, "prompt") as prompt:
                result = self.runner.invoke(app.cli, options + ["--password", "secret"])
                self.assertEqual(result.exit_code, 0, result.output)
                prompt.assert_not_called()
                json.loads(result.output)
            result = self.runner.invoke(app.cli, options, input="hidden-secret\n")
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertNotIn("hidden-secret", result.output)
            self.assertEqual(app.load_config(".itopcli").password, "hidden-secret")
            self.assertEqual(app.load_config(".itopcli").timeout, 10)

    def test_configure_defaults_validation_and_abort(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(
                app.cli,
                ["configure"],
                input=(
                    "https://example.invalid\n\ninvalid\n1.3\n\n0\n10\nuser\nsecret\n\n\n"
                ),
            )
            self.assertEqual(result.exit_code, 0, result.output)
            cfg = app.load_config(".itopcli")
            self.assertEqual(cfg.organization, "")
            self.assertTrue(cfg.verify_ssl)
            original = Path(".itopcli").read_bytes()
            with patch.object(app.click, "prompt", side_effect=app.click.Abort):
                result = self.runner.invoke(app.cli, ["configure"])
            self.assertNotEqual(result.exit_code, 0)
            self.assertEqual(Path(".itopcli").read_bytes(), original)

    def test_bad_configuration_is_json_error(self):
        with self.runner.isolated_filesystem():
            for overrides in ({"timeout": "oops"}, {"verify_ssl": "oops"}):
                self.config(**overrides)
                result = self.runner.invoke(app.cli, ["query"])
                self.assertEqual(result.exit_code, 1)
                self.assertEqual(
                    json.loads(result.output)["source"], "ReadClientConfiguration"
                )

    def test_missing_configuration(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(app.cli, ["query"])
            self.assertEqual(result.exit_code, 1)
            self.assertIn(
                "Could not read configuration", json.loads(result.output)["message"]
            )

    def test_dry_runs_without_configuration(self):
        commands = [
            ["query"],
            ["create", "--class", "Server", "--set", "name=test"],
            ["update", "--class", "Server", "--key", "1", "--set", "cpu=8"],
            ["delete", "--class", "Server", "--key", "1"],
        ]
        with (
            self.runner.isolated_filesystem(),
            patch.object(app.requests, "post") as post,
        ):
            for command in commands:
                with self.subTest(command=command):
                    result = self.runner.invoke(app.cli, command + ["--dry-run"])
                    self.assertEqual(result.exit_code, 0, result.output)
                    self.assertIn("operation", json.loads(result.output))
            post.assert_not_called()

    def test_create_default_and_explicit_organization(self):
        with (
            self.runner.isolated_filesystem(),
            patch.object(app.requests, "post") as post,
        ):
            self.config()
            post.return_value.json.return_value = {"code": 0}
            for extra, expected in [
                ([], "7"),
                (["--set", "org_id=9"], 9),
                (["--fields-json", '{"org_id":null}'], None),
            ]:
                args = ["create", "--class", "Server", "--set", "name=test"] + extra
                preview = self.runner.invoke(app.cli, args + ["--dry-run"])
                self.assertEqual(preview.exit_code, 0, preview.output)
                payload = json.loads(preview.output)
                self.assertEqual(payload["fields"]["org_id"], expected)
                result = self.runner.invoke(app.cli, args)
                self.assertEqual(result.exit_code, 0, result.output)
                self.assertEqual(
                    json.loads(post.call_args.kwargs["data"]["json_data"]), payload
                )

    def test_create_without_default_organization(self):
        with self.runner.isolated_filesystem():
            self.config(organization="")
            result = self.runner.invoke(
                app.cli,
                ["create", "--class", "Server", "--set", "name=test", "--dry-run"],
            )
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertNotIn("org_id", json.loads(result.output)["fields"])

    def test_request_parameters(self):
        cfg = app.ClientConfiguration()
        cfg.username, cfg.password, cfg.timeout = "user", "pass", 12
        with patch.object(app.requests, "post") as post:
            post.return_value.json.return_value = {"code": 0, "objects": {}}
            self.assertEqual(app.call_itop(cfg, {"operation": "core/get"})["code"], 0)
            kwargs = post.call_args.kwargs
            self.assertEqual(kwargs["timeout"], 12)
            self.assertTrue(kwargs["verify"])
            self.assertEqual(kwargs["data"]["auth_user"], "user")
            self.assertEqual(kwargs["data"]["auth_pwd"], "pass")

    def test_api_errors(self):
        for value in [{"code": 1, "message": "denied"}, [], None, {}]:
            with self.subTest(value=value), patch.object(app.requests, "post") as post:
                post.return_value.json.return_value = value
                with self.assertRaises(app.ClientError):
                    app.call_itop(app.ClientConfiguration(), {})
        with patch.object(
            app.requests, "post", side_effect=requests.Timeout("timeout")
        ):
            with self.assertRaisesRegex(app.ClientError, "HTTP error"):
                app.call_itop(app.ClientConfiguration(), {})
        with patch.object(app.requests, "post") as post:
            post.return_value.json.side_effect = ValueError("bad JSON")
            with self.assertRaisesRegex(app.ClientError, "Invalid JSON"):
                app.call_itop(app.ClientConfiguration(), {})
            post.return_value.raise_for_status.side_effect = requests.HTTPError("500")
            with self.assertRaisesRegex(app.ClientError, "HTTP error"):
                app.call_itop(app.ClientConfiguration(), {})

    def test_validation_prevents_requests(self):
        commands = [
            ["query", "--criteria", "test"],
            ["update", "--class", "Server", "--key", "1"],
            ["create", "--class", "Server", "--fields-json", "[]"],
        ]
        with patch.object(app.requests, "post") as post:
            for command in commands:
                result = self.runner.invoke(app.cli, command)
                self.assertEqual(result.exit_code, 1)
                json.loads(result.output)
            post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
