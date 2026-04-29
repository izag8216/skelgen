"""CLI entry point for skelgen."""

import argparse
import sys
from pathlib import Path

from skelgen import __version__
from skelgen.generator import (
    generate_script,
    list_templates,
    validate_script,
)


def cmd_create(args: argparse.Namespace) -> int:
    """Handle the 'create' subcommand."""
    try:
        script_content = generate_script(
            name=args.name,
            args_spec=getattr(args, "args", "") or "",
            template_id=args.template,
            shell=args.shell,
            description=args.description or "",
            author=args.author or "",
            version=args.version,
        )
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output)
        if output_path.exists() and not args.force:
            print(f"Error: {output_path} already exists. Use --force to overwrite.", file=sys.stderr)
            return 1
        output_path.write_text(script_content, encoding="utf-8")
        print(f"Created: {output_path}")
    else:
        print(script_content, end="")

    return 0


def cmd_list_templates(args: argparse.Namespace) -> int:  # noqa: ARG001
    """Handle the 'list-templates' subcommand."""
    templates = list_templates()
    print("Available templates:\n")
    for tmpl in templates:
        print(f"  {tmpl['id']:<15} {tmpl['name']:<25} {tmpl['description']}")
    print()
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Handle the 'validate' subcommand."""
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Error: {script_path} not found", file=sys.stderr)
        return 1

    content = script_path.read_text(encoding="utf-8")
    issues = validate_script(content)

    if not issues:
        print("All checks passed!")
        return 0

    level_map = {"error": "ERROR", "warning": "WARN", "info": "INFO"}
    exit_code = 0

    for issue in issues:
        level = issue["level"]
        if level == "error":
            exit_code = 2
        print(f"  [{level_map[level]:<7}] {issue['message']}")

    print(f"\nFound {len(issues)} issue(s).")
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="skelgen",
        description="Shell script skeleton generator with arg parsing, help, and error handling",
    )
    parser.add_argument("--version", action="version", version=f"skelgen {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create
    create_parser = subparsers.add_parser("create", help="Generate a shell script skeleton")
    create_parser.add_argument("name", help="Script name")
    create_parser.add_argument(
        "--args",
        help="Comma-separated argument spec (e.g. 'env,tag,--force,--verbose')",
    )
    create_parser.add_argument(
        "--template", "-t",
        default="basic",
        help="Template to use (default: basic)",
    )
    create_parser.add_argument(
        "--shell", "-s",
        choices=["bash", "sh", "zsh"],
        default="bash",
        help="Target shell (default: bash)",
    )
    create_parser.add_argument("--description", "-d", help="Script description")
    create_parser.add_argument("--author", "-a", help="Author name")
    create_parser.add_argument("--version", "-v", default="0.1.0", help="Script version")
    create_parser.add_argument("--output", "-o", help="Output file path")
    create_parser.add_argument("--force", "-f", action="store_true", help="Overwrite existing file")
    create_parser.set_defaults(func=cmd_create)

    # list-templates
    list_parser = subparsers.add_parser("list-templates", help="List available templates")
    list_parser.set_defaults(func=cmd_list_templates)

    # validate
    validate_parser = subparsers.add_parser("validate", help="Validate a shell script")
    validate_parser.add_argument("script", help="Path to shell script")
    validate_parser.set_defaults(func=cmd_validate)

    return parser


def main() -> None:
    """Main entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    exit_code = args.func(args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
