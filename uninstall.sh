#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${SKYLA_HOME:-$HOME/.local/share/skyla}"
CONFIG_DIR="${SKYLA_CONFIG_DIR:-$HOME/.config/skyla}"
STATE_DIR="${SKYLA_STATE_DIR:-$HOME/.local/state/skyla}"
BIN_DIR="${SKYLA_BIN_DIR:-$HOME/.local/bin}"

if [[ "${1:-}" != "--yes" ]]; then
  read -r -p "Remove SKYLA installation, configuration, and state? [y/N] " answer
  [[ "$answer" =~ ^[Yy]$ ]] || { echo "Uninstall cancelled."; exit 0; }
fi

rm -f "$BIN_DIR/skyla"
rm -rf "$INSTALL_DIR" "$CONFIG_DIR" "$STATE_DIR"
echo "SKYLA was uninstalled."
