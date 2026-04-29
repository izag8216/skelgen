"""Tests for skelgen.cli module."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from skelgen.cli import build_parser, cmd_create, cmd_list_templates, cmd_validate, main


class TestBuildParser:
    """Tests for the argument parser."""

    def test_parser_creation(self):
        parser = build_parser()
        assert parser.prog == "skelgen"

    def test_create_subcommand(self):
        parser = build_parser()
        args = parser.parse_args(["create", "myscript"])
        assert args.command == "create"
        assert args.name == "myscript"

    def test_create_with_options(self):
        parser = build_parser()
        args = parser.parse_args([
            "create", "myscript",
            "--args", "env,tag",
            "--shell", "zsh",
            "--template", "service",
            "--description", "My script",
            "--author", "Alice",
            "--version", "1.0.0",
            "--output", "/tmp/test.sh",
        ])
        assert args.name == "myscript"
        assert args.args == "env,tag"
        assert args.shell == "zsh"
        assert args.template == "service"
        assert args.description == "My script"
        assert args.author == "Alice"
        assert args.version == "1.0.0"
        assert args.output == "/tmp/test.sh"

    def test_list_templates_subcommand(self):
        parser = build_parser()
        args = parser.parse_args(["list-templates"])
        assert args.command == "list-templates"

    def test_validate_subcommand(self):
        parser = build_parser()
        args = parser.parse_args(["validate", "script.sh"])
        assert args.command == "validate"
        assert args.script == "script.sh"

    def test_version_flag(self):
        parser = build_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--version"])
        assert exc_info.value.code == 0


class TestCmdCreate:
    """Tests for cmd_create."""

    def test_stdout_output(self, capsys):
        parser = build_parser()
        args = parser.parse_args(["create", "test"])
        exit_code = cmd_create(args)
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "#!/usr/bin/env bash" in captured.out

    def test_file_output(self, tmp_path):
        output_file = tmp_path / "script.sh"
        parser = build_parser()
        args = parser.parse_args(["create", "test", "--output", str(output_file)])
        exit_code = cmd_create(args)
        assert exit_code == 0
        assert output_file.exists()
        assert "#!/usr/bin/env bash" in output_file.read_text()

    def test_file_exists_no_force(self, tmp_path, capsys):
        output_file = tmp_path / "script.sh"
        output_file.write_text("existing")
        parser = build_parser()
        args = parser.parse_args(["create", "test", "--output", str(output_file)])
        exit_code = cmd_create(args)
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "already exists" in captured.err

    def test_file_exists_with_force(self, tmp_path):
        output_file = tmp_path / "script.sh"
        output_file.write_text("existing")
        parser = build_parser()
        args = parser.parse_args(["create", "test", "--output", str(output_file), "--force"])
        exit_code = cmd_create(args)
        assert exit_code == 0
        assert "#!/usr/bin/env bash" in output_file.read_text()

    def test_invalid_shell(self, capsys):
        from skelgen.generator import generate_script
        with pytest.raises(ValueError) as exc_info:
            generate_script(name="test", shell="fish")
        assert "Unsupported shell" in str(exc_info.value)


class TestCmdListTemplates:
    """Tests for cmd_list_templates."""

    def test_lists_templates(self, capsys):
        parser = build_parser()
        args = parser.parse_args(["list-templates"])
        exit_code = cmd_list_templates(args)
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "basic" in captured.out
        assert "service" in captured.out


class TestCmdValidate:
    """Tests for cmd_validate."""

    def test_valid_script(self, tmp_path, capsys):
        script_file = tmp_path / "good.sh"
        parser = build_parser()
        args = parser.parse_args(["create", "test", "--output", str(script_file), "--force"])
        cmd_create(args)

        args = parser.parse_args(["validate", str(script_file)])
        exit_code = cmd_validate(args)
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "All checks passed" in captured.out

    def test_invalid_script(self, tmp_path, capsys):
        script_file = tmp_path / "bad.sh"
        script_file.write_text("echo hello\n")
        parser = build_parser()
        args = parser.parse_args(["validate", str(script_file)])
        exit_code = cmd_validate(args)
        assert exit_code == 2
        captured = capsys.readouterr()
        assert "ERROR" in captured.out or "WARN" in captured.out

    def test_missing_file(self, capsys):
        parser = build_parser()
        args = parser.parse_args(["validate", "/tmp/nonexistent.sh"])
        exit_code = cmd_validate(args)
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "not found" in captured.err


class TestMain:
    """Tests for main entry point."""

    def test_no_args_prints_help(self, capsys):
        with patch.object(sys, "argv", ["skelgen"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "usage:" in captured.out

    def test_create_via_main(self, tmp_path):
        output_file = tmp_path / "script.sh"
        with patch.object(sys, "argv", ["skelgen", "create", "test", "--output", str(output_file)]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
        assert output_file.exists()
