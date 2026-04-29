"""Tests for skelgen.generator module."""

import pytest

from skelgen.generator import (
    BUILTIN_TEMPLATES,
    SHELL_VARIANTS,
    generate_script,
    get_template_content,
    list_templates,
    parse_args_spec,
    validate_script,
)


class TestParseArgsSpec:
    """Tests for parse_args_spec."""

    def test_empty_string(self):
        assert parse_args_spec("") == []

    def test_single_positional(self):
        result = parse_args_spec("env")
        assert len(result) == 1
        assert result[0]["name"] == "env"
        assert result[0]["type"] == "positional"

    def test_multiple_positionals(self):
        result = parse_args_spec("env,tag")
        assert len(result) == 2
        assert result[0]["name"] == "env"
        assert result[1]["name"] == "tag"

    def test_flag(self):
        result = parse_args_spec("--force")
        assert len(result) == 1
        assert result[0]["name"] == "force"
        assert result[0]["type"] == "flag"

    def test_option(self):
        result = parse_args_spec("--count=10")
        assert len(result) == 1
        assert result[0]["name"] == "count"
        assert result[0]["type"] == "option"

    def test_short_opt(self):
        result = parse_args_spec("-n")
        assert len(result) == 1
        assert result[0]["name"] == "n"
        assert result[0]["type"] == "short"

    def test_mixed_args(self):
        result = parse_args_spec("env,--force,--count=10")
        assert len(result) == 3
        assert result[0]["type"] == "positional"
        assert result[1]["type"] == "flag"
        assert result[2]["type"] == "option"

    def test_whitespace_trim(self):
        result = parse_args_spec(" env , --force ")
        assert len(result) == 2
        assert result[0]["name"] == "env"
        assert result[1]["name"] == "force"


class TestListTemplates:
    """Tests for list_templates."""

    def test_returns_builtin_templates(self):
        templates = list_templates()
        assert len(templates) == len(BUILTIN_TEMPLATES)
        assert all("id" in t and "name" in t and "description" in t for t in templates)


class TestGetTemplateContent:
    """Tests for get_template_content."""

    def test_basic_bash(self):
        content = get_template_content("basic", "bash")
        assert "{{ shebang }}" in content

    def test_basic_sh(self):
        content = get_template_content("basic", "sh")
        assert "{{ shebang }}" in content

    def test_service_bash(self):
        content = get_template_content("service", "bash")
        assert "service_start" in content
        assert "service_stop" in content

    def test_deploy_bash(self):
        content = get_template_content("deploy", "bash")
        assert "deploy()" in content or "function deploy" in content

    def test_backup_bash(self):
        content = get_template_content("backup", "bash")
        assert "backup()" in content or "function backup" in content

    def test_api_service_bash(self):
        content = get_template_content("api-service", "bash")
        assert "configtest" in content

    def test_invalid_template_raises(self):
        with pytest.raises(FileNotFoundError):
            get_template_content("nonexistent", "bash")


class TestGenerateScript:
    """Tests for generate_script."""

    def test_basic_generation(self):
        script = generate_script(name="test-script", shell="bash")
        assert "#!/usr/bin/env bash" in script
        assert "test-script" in script
        assert "set -euo pipefail" in script

    def test_sh_generation(self):
        script = generate_script(name="test-script", shell="sh")
        assert "#!/usr/bin/env sh" in script

    def test_zsh_generation(self):
        script = generate_script(name="test-script", shell="zsh")
        assert "#!/usr/bin/env zsh" in script

    def test_with_description(self):
        script = generate_script(name="test", description="My description", shell="bash")
        assert "My description" in script

    def test_with_author(self):
        script = generate_script(name="test", author="Alice", shell="bash")
        assert "Alice" in script

    def test_with_version(self):
        script = generate_script(name="test", version="2.0.0", shell="bash")
        assert "2.0.0" in script

    def test_with_positional_args(self):
        script = generate_script(name="test", args_spec="env,tag", shell="bash")
        assert "env = $env" in script
        assert "tag = $tag" in script

    def test_with_flags(self):
        script = generate_script(name="test", args_spec="--force,--verbose", shell="bash")
        assert "force=true" in script or "force = true" in script

    def test_with_options(self):
        script = generate_script(name="test", args_spec="--count=10", shell="bash")
        assert "count=" in script

    def test_invalid_shell_raises(self):
        with pytest.raises(ValueError):
            generate_script(name="test", shell="fish")

    def test_all_templates_all_shells(self):
        for tmpl in BUILTIN_TEMPLATES:
            for shell in SHELL_VARIANTS:
                try:
                    script = generate_script(
                        name="test", template_id=tmpl["id"], shell=shell
                    )
                    assert script.startswith("#!/usr/bin/env")
                    assert len(script) > 100
                except FileNotFoundError:
                    pytest.fail(
                        f"Template '{tmpl['id']}' missing for shell '{shell}'"
                    )


class TestValidateScript:
    """Tests for validate_script."""

    def test_valid_script(self):
        script = generate_script(name="test", shell="bash")
        issues = validate_script(script)
        # Should have no errors since our generated scripts are valid
        errors = [i for i in issues if i["level"] == "error"]
        assert len(errors) == 0

    def test_missing_shebang(self):
        issues = validate_script("echo hello")
        errors = [i for i in issues if "shebang" in i["message"]]
        assert len(errors) == 1
        assert errors[0]["level"] == "error"

    def test_missing_strict_mode(self):
        script = "#!/bin/bash\necho hello"
        issues = validate_script(script)
        warnings = [i for i in issues if "strict mode" in i["message"]]
        assert len(warnings) == 1
        assert warnings[0]["level"] == "warning"

    def test_missing_help(self):
        script = "#!/bin/bash\nset -euo pipefail\necho hello"
        issues = validate_script(script)
        warnings = [i for i in issues if "help" in i["message"]]
        assert len(warnings) == 1

    def test_empty_script(self):
        issues = validate_script("")
        assert len(issues) >= 2  # at least shebang + strict mode missing
