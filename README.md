<p align="center">
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="100%" max-width="800">
    <defs>
      <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
        <stop offset="50%" style="stop-color:#1e293b;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#0f172a;stop-opacity:1" />
      </linearGradient>
      <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#06b6d4;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
      </linearGradient>
      <filter id="glow">
        <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
        <feMerge>
          <feMergeNode in="coloredBlur"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>
    </defs>
    
    <!-- Background -->
    <rect width="800" height="200" rx="12" fill="url(#bgGrad)"/>
    
    <!-- Grid lines -->
    <g stroke="#1e293b" stroke-width="1">
      <line x1="0" y1="50" x2="800" y2="50"/>
      <line x1="0" y1="100" x2="800" y2="100"/>
      <line x1="0" y1="150" x2="800" y2="150"/>
      <line x1="200" y1="0" x2="200" y2="200"/>
      <line x1="400" y1="0" x2="400" y2="200"/>
      <line x1="600" y1="0" x2="600" y2="200"/>
    </g>
    
    <!-- Decorative circuit/script lines -->
    <g fill="none" stroke="url(#accentGrad)" stroke-width="2" stroke-linecap="round" filter="url(#glow)">
      <path d="M 60 80 L 100 80 L 120 60 L 160 60"/>
      <path d="M 60 100 L 90 100 L 110 120 L 150 120"/>
      <path d="M 60 120 L 80 120 L 100 140 L 140 140"/>
      <circle cx="160" cy="60" r="3" fill="#06b6d4" stroke="none"/>
      <circle cx="150" cy="120" r="3" fill="#8b5cf6" stroke="none"/>
      <circle cx="140" cy="140" r="3" fill="#06b6d4" stroke="none"/>
    </g>
    
    <!-- Document / Blueprint shape -->
    <g transform="translate(520, 40)">
      <rect x="0" y="0" width="140" height="160" rx="6" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
      <rect x="0" y="0" width="140" height="28" rx="6" fill="#0f172a" stroke="#334155" stroke-width="1.5"/>
      <circle cx="16" cy="14" r="4" fill="#ef4444"/>
      <circle cx="32" cy="14" r="4" fill="#f59e0b"/>
      <circle cx="48" cy="14" r="4" fill="#22c55e"/>
      
      <!-- Script lines inside document -->
      <rect x="14" y="44" width="80" height="6" rx="3" fill="#334155"/>
      <rect x="14" y="58" width="110" height="6" rx="3" fill="#334155"/>
      <rect x="14" y="72" width="60" height="6" rx="3" fill="#06b6d4" opacity="0.6"/>
      <rect x="14" y="86" width="100" height="6" rx="3" fill="#334155"/>
      <rect x="14" y="100" width="50" height="6" rx="3" fill="#8b5cf6" opacity="0.6"/>
      <rect x="14" y="114" width="90" height="6" rx="3" fill="#334155"/>
      <rect x="14" y="128" width="70" height="6" rx="3" fill="#06b6d4" opacity="0.6"/>
      
      <!-- Cursor -->
      <rect x="14" y="142" width="8" height="12" rx="1" fill="#06b6d4" opacity="0.8">
        <animate attributeName="opacity" values="0.8;0.2;0.8" dur="1.5s" repeatCount="indefinite"/>
      </rect>
    </g>
    
    <!-- Gear / Cog on right side -->
    <g transform="translate(690, 80)" stroke="#334155" stroke-width="2" fill="none">
      <circle cx="20" cy="20" r="14"/>
      <circle cx="20" cy="20" r="8" stroke="#06b6d4" stroke-width="1.5"/>
      <line x1="20" y1="0" x2="20" y2="6"/>
      <line x1="20" y1="34" x2="20" y2="40"/>
      <line x1="0" y1="20" x2="6" y2="20"/>
      <line x1="34" y1="20" x2="40" y2="20"/>
      <line x1="6" y1="6" x2="10" y2="10"/>
      <line x1="30" y1="30" x2="34" y2="34"/>
      <line x1="6" y1="34" x2="10" y2="30"/>
      <line x1="30" y1="10" x2="34" y2="6"/>
    </g>
    
    <!-- Title text using paths for cross-platform consistency -->
    <g fill="#f1f5f9">
      <!-- S -->
      <path d="M 210 95 Q 210 85 220 85 L 235 85 Q 245 85 245 95 Q 245 102 235 102 L 220 102 Q 210 102 210 110 Q 210 120 220 120 L 235 120 Q 245 120 245 110" stroke="#f1f5f9" stroke-width="4" fill="none" stroke-linecap="round"/>
      <!-- k -->
      <path d="M 255 80 L 255 120 M 255 102 L 270 85 M 255 102 L 270 120" stroke="#f1f5f9" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
      <!-- e -->
      <circle cx="285" cy="108" r="12" stroke="#f1f5f9" stroke-width="4" fill="none"/>
      <line x1="273" y1="108" x2="297" y2="108" stroke="#0f172a" stroke-width="5"/>
      <!-- l -->
      <line x1="305" y1="85" x2="305" y2="118" stroke="#f1f5f9" stroke-width="4" stroke-linecap="round"/>
      <!-- g -->
      <circle cx="325" cy="108" r="12" stroke="#f1f5f9" stroke-width="4" fill="none"/>
      <path d="M 337 108 L 337 122 Q 337 132 325 132 Q 315 132 315 122" stroke="#f1f5f9" stroke-width="4" fill="none" stroke-linecap="round"/>
      <!-- e -->
      <circle cx="355" cy="108" r="12" stroke="#f1f5f9" stroke-width="4" fill="none"/>
      <line x1="343" y1="108" x2="367" y2="108" stroke="#0f172a" stroke-width="5"/>
      <!-- n -->
      <path d="M 375 120 L 375 96 Q 375 88 383 88 Q 391 88 391 96 L 391 120" stroke="#f1f5f9" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
    
    <!-- Accent line under title -->
    <line x1="210" y1="130" x2="395" y2="130" stroke="url(#accentGrad)" stroke-width="3" stroke-linecap="round"/>
    
    <!-- Subtitle -->
    <g fill="#94a3b8" font-family="monospace" font-size="13">
      <rect x="210" y="145" width="6" height="6" rx="1" fill="#06b6d4"/>
      <rect x="220" y="145" width="170" height="6" rx="3" fill="#475569"/>
      <rect x="210" y="158" width="6" height="6" rx="1" fill="#8b5cf6"/>
      <rect x="220" y="158" width="140" height="6" rx="3" fill="#475569"/>
    </g>
    
    <!-- Corner brackets -->
    <g stroke="#334155" stroke-width="2" fill="none" stroke-linecap="round">
      <path d="M 30 170 L 30 185 L 45 185"/>
      <path d="M 770 170 L 770 185 L 755 185"/>
      <path d="M 30 30 L 30 15 L 45 15"/>
      <path d="M 770 30 L 770 15 L 755 15"/>
    </g>
  </svg>
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
