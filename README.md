<p align="center">
  <img src="assets/header.svg" alt="skelgen header" width="100%" style="max-width: 800px;"/>
</p>

<h1 align="center">skelgen</h1>

<p align="center">
  <strong>Shell script skeleton generator with arg parsing, help text, and error handling baked in</strong>
</p>

<p align="center">
  <a href="https://github.com/izag8216/skelgen/actions">
    <img src="https://img.shields.io/badge/tests-passing-22c55e?style=flat-square" alt="Tests"/>
  </a>
  <a href="https://github.com/izag8216/skelgen/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-3b82f6?style=flat-square" alt="License"/>
  </a>
  <a href="https://pypi.org/project/skelgen/">
    <img src="https://img.shields.io/badge/pypi-0.1.0-8b5cf6?style=flat-square" alt="PyPI"/>
  </a>
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/python-3.9+-06b6d4?style=flat-square" alt="Python"/>
  </a>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=gradient&color=0:0f172a,50:1e293b,100:0f172a&height=2&section=header" width="100%"/>
</p>

---

## Why skelgen?

Writing robust shell scripts from scratch requires boilerplate for argument parsing, help text generation, error handling, logging, and cleanup traps. Developers either copy-paste from old scripts (perpetuating bad patterns) or skip the boilerplate entirely (creating fragile scripts).

**skelgen** interactively generates opinionated, best-practice shell script skeletons from Jinja2 templates. Generated scripts include `getopts`-style argument parsing, `--help` output, `set -euo pipefail` safety, logging functions, temp file cleanup traps, and consistent exit codes.

## Installation

```bash
pip install skelgen
```

## Quick Start

```bash
# Generate a basic script with arguments
skelgen create deploy --args "env,tag,--force,--verbose" --output deploy.sh

# Use a service template
skelgen create myapp --template service --output myapp.sh

# List all available templates
skelgen list-templates

# Validate an existing script against best practices
skelgen validate script.sh
```

## Commands

### `create`

Generate a shell script skeleton.

```bash
skelgen create <name> [options]
```

| Option | Description |
|--------|-------------|
| `--args ARGS` | Comma-separated argument spec (e.g. `env,tag,--force`) |
| `--template TEMPLATE` | Template to use (default: `basic`) |
| `--shell {bash,sh,zsh}` | Target shell (default: `bash`) |
| `--description DESC` | Script description |
| `--author NAME` | Author name |
| `--version VER` | Script version (default: `0.1.0`) |
| `--output PATH` | Output file path |
| `--force` | Overwrite existing file |

**Argument specification syntax:**

| Form | Type | Example |
|------|------|---------|
| `name` | Positional argument | `env`, `tag` |
| `--flag` | Boolean flag | `--force`, `--verbose` |
| `--opt=default` | Option with default | `--count=10` |

### `list-templates`

Show all built-in templates.

```bash
skelgen list-templates
```

Available templates:

| Template | Description |
|----------|-------------|
| `basic` | Simple script with args, help, and error handling |
| `service` | Service/daemon script with start/stop/restart/status |
| `deploy` | Deployment script with env, tag, and rollback support |
| `backup` | Backup script with compression and retention |
| `api-service` | API service wrapper with configtest |

### `validate`

Check a shell script against best practices.

```bash
skelgen validate script.sh
```

Checks for:
- Shebang line
- Strict mode (`set -euo pipefail` or equivalent)
- Help/usage function
- Error logging function
- Cleanup traps
- Main guard

## Examples

### Basic script with positional args and flags

```bash
skelgen create deploy \
  --args "env,tag,--force,--dry-run" \
  --description "Deploy application to target environment" \
  --author "izag8216" \
  --output deploy.sh
```

Generates:

```bash
#!/usr/bin/env bash
#
# deploy
# Deploy application to target environment
#

set -euo pipefail

log_info()  { printf '%s [INFO]  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }
log_warn()  { printf '%s [WARN]  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2; }
log_error() { printf '%s [ERROR] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2; }

die() { log_error "$*"; exit 1; }

cleanup() {
    local exit_code=$?
    exit ${exit_code}
}
trap cleanup EXIT

# ... argument parsing, help, main logic ...
```

### Service script

```bash
skelgen create myapp --template service --output myapp.sh
chmod +x myapp.sh
./myapp.sh start
./myapp.sh status
./myapp.sh stop
```

## Supported Shells

- **bash** (default) -- Full feature set
- **sh** -- POSIX-compatible scripts
- **zsh** -- Zsh-specific scripts

## Development

```bash
git clone https://github.com/izag8216/skelgen.git
cd skelgen
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest
```

## License

MIT License -- see [LICENSE](LICENSE) for details.

## Author

Created by [izag8216](https://github.com/izag8216).
