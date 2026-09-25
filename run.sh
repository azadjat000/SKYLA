#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${SKYLA_HOME:-$HOME/.local/share/skyla}"
CONFIG_DIR="${SKYLA_CONFIG_DIR:-$HOME/.config/skyla}"
STATE_DIR="${SKYLA_STATE_DIR:-$HOME/.local/state/skyla}"
BIN_DIR="${SKYLA_BIN_DIR:-$HOME/.local/bin}"

if [[ -x "$BIN_DIR/skyla" && -f "$INSTALL_DIR/skyla.py" ]]; then
  exec "$BIN_DIR/skyla" "$@"
fi
if [[ ! -x "$INSTALL_DIR/venv/bin/python" ]]; then
  echo "SKYLA is not installed. Run ./install.sh first." >&2
  exit 1
fi
exec "$INSTALL_DIR/venv/bin/python" "$INSTALL_DIR/skyla.py" --config "${SKYLA_CONFIG:-$CONFIG_DIR/config.json}" "$@"
