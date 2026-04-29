"""Core generator logic for shell script skeletons."""

import os
from pathlib import Path
from typing import Any

import jinja2

TEMPLATES_DIR = Path(__file__).parent / "templates"

SHELL_VARIANTS = ["bash", "sh", "zsh"]

BUILTIN_TEMPLATES = [
    {
        "id": "basic",
        "name": "Basic Script",
        "description": "Simple script with args, help, and error handling",
    },
    {
        "id": "service",
        "name": "Service/daemon script",
        "description": "Script with start/stop/restart/status commands",
    },
    {
        "id": "deploy",
        "name": "Deploy script",
        "description": "Deployment script with env, tag, and rollback support",
    },
    {
        "id": "backup",
        "name": "Backup script",
        "description": "Backup script with compression and retention",
    },
    {
        "id": "api-service",
        "name": "API Service wrapper",
        "description": "Script to manage an API service lifecycle",
    },
]


def parse_args_spec(args_str: str) -> list[dict[str, Any]]:
    """Parse a comma-separated args spec into structured argument definitions.

    Args:
        args_str: Comma-separated string like "env,tag,--force,--verbose,-n"

    Returns:
        List of argument dicts with name, type (positional/flag/option), and raw form.
    """
    if not args_str.strip():
        return []

    args = []
    for raw in args_str.split(","):
        raw = raw.strip()
        if not raw:
            continue

        arg: dict[str, Any] = {"raw": raw, "name": raw.lstrip("-")}

        if raw.startswith("--"):
            arg["type"] = "flag" if "=" not in raw else "option"
            if arg["type"] == "option":
                arg["name"] = raw.split("=")[0].lstrip("-")
                arg["default"] = raw.split("=", 1)[1] if "=" in raw else ""
        elif raw.startswith("-"):
            arg["type"] = "short"
        else:
            arg["type"] = "positional"

        args.append(arg)

    return args


def list_templates() -> list[dict[str, str]]:
    """Return list of built-in templates."""
    return BUILTIN_TEMPLATES


def get_template_content(template_id: str, shell: str) -> str:
    """Load a template by ID and shell variant.

    Args:
        template_id: Template identifier (basic, service, deploy, etc.)
        shell: Shell variant (bash, sh, zsh)

    Returns:
        Raw template content string.

    Raises:
        FileNotFoundError: If template doesn't exist.
    """
    template_file = TEMPLATES_DIR / f"{template_id}_{shell}.sh.j2"
    if not template_file.exists():
        template_file = TEMPLATES_DIR / f"{template_id}.sh.j2"
    if not template_file.exists():
        available = [f.stem.replace(".sh.j2", "") for f in TEMPLATES_DIR.glob("*.sh.j2")]
        raise FileNotFoundError(
            f"Template '{template_id}' not found for shell '{shell}'. "
            f"Available: {', '.join(sorted(set(available)))}"
        )
    return template_file.read_text(encoding="utf-8")


def generate_script(
    name: str,
    args_spec: str = "",
    template_id: str = "basic",
    shell: str = "bash",
    description: str = "",
    author: str = "",
    version: str = "0.1.0",
) -> str:
    """Generate a complete shell script from template.

    Args:
        name: Script name (used in help text and shebang comments)
        args_spec: Comma-separated argument specification
        template_id: Template to use (basic, service, deploy, etc.)
        shell: Target shell (bash, sh, zsh)
        description: One-line description of the script
        author: Author name
        version: Script version string

    Returns:
        Complete shell script source code.
    """
    if shell not in SHELL_VARIANTS:
        raise ValueError(f"Unsupported shell '{shell}'. Choose from: {', '.join(SHELL_VARIANTS)}")

    template_content = get_template_content(template_id, shell)
    parsed_args = parse_args_spec(args_spec)

    shebang_map = {
        "bash": "#!/usr/bin/env bash",
        "sh": "#!/usr/bin/env sh",
        "zsh": "#!/usr/bin/env zsh",
    }

    env = jinja2.Environment(
        loader=jinja2.BaseLoader(),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    template = env.from_string(template_content)

    return template.render(
        script_name=name,
        description=description or f"{name} -- auto-generated shell script",
        author=author,
        version=version,
        shell=shell,
        shebang=shebang_map.get(shell, shebang_map["bash"]),
        args=parsed_args,
        args_raw=args_spec,
        positional_args=[a for a in parsed_args if a["type"] == "positional"],
        flags=[a for a in parsed_args if a["type"] == "flag"],
        options=[a for a in parsed_args if a["type"] == "option"],
        short_opts=[a for a in parsed_args if a["type"] == "short"],
    )


def validate_script(content: str) -> list[dict[str, str]]:
    """Validate a shell script against best practices.

    Checks for:
    - Shebang line
    - set -euo pipefail (or equivalent)
    - Help function
    - Error handling
    - Cleanup traps
    - Consistent exit codes

    Args:
        content: Shell script source code.

    Returns:
        List of issue dicts with 'level' (error/warning/info) and 'message'.
    """
    issues: list[dict[str, str]] = []
    lines = content.split("\n")

    has_shebang = any(line.startswith("#!") for line in lines[:3])
    has_strict_mode = any("set -e" in line or "set -eu" in line for line in lines)
    has_help = any("usage()" in line or "show_help()" in line or "help()" in line for line in lines)
    has_error_func = any("error()" in line or "die()" in line or "log_error()" in line for line in lines)
    has_cleanup = any("trap " in line and "EXIT" in line for line in lines)
    has_main_guard = any(
        'if [[ "${BASH_SOURCE[0]}" == "${0}" ]]' in line or
        '"$0" == "$BASH_SOURCE"' in line or
        'if [ "$0" = "$(basename "$0")" ]' in line
        for line in lines
    )

    if not has_shebang:
        issues.append({"level": "error", "message": "Missing shebang line (#!/usr/bin/env bash)"})

    if not has_strict_mode:
        issues.append({"level": "warning", "message": "Missing strict mode (set -euo pipefail)"})

    if not has_help:
        issues.append({"level": "warning", "message": "No help/usage function found"})

    if not has_error_func:
        issues.append({"level": "info", "message": "No dedicated error logging function found"})

    if not has_cleanup:
        issues.append({"level": "info", "message": "No EXIT trap for cleanup found"})

    if not has_main_guard:
        issues.append({"level": "info", "message": "No main guard (if [[ \"${BASH_SOURCE[0]}\" == \"${0}\" ]]) found"})

    return issues
