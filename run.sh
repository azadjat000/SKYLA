#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$ROOT_DIR/skyla.py" --config "${SKYLA_CONFIG:-$ROOT_DIR/config/default.json}" "$@"
