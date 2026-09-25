#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "SKYLA currently supports Linux only." >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="${SKYLA_HOME:-$HOME/.local/share/skyla}"
BIN_DIR="${SKYLA_BIN_DIR:-$HOME/.local/bin}"
CONFIG_DIR="${SKYLA_CONFIG_DIR:-$HOME/.config/skyla}"
STATE_DIR="${SKYLA_STATE_DIR:-$HOME/.local/state/skyla}"
VENV_DIR="$INSTALL_DIR/venv"
MODEL="${SKYLA_MODEL:-llama3.2}"

command -v python3 >/dev/null || { echo "Missing dependency: install Python 3.10+ using your package manager." >&2; exit 1; }
python3 -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' || { echo "SKYLA requires Python 3.10 or newer." >&2; exit 1; }
python3 -m venv --help >/dev/null 2>&1 || { echo "Python venv support is missing; install your distribution's python3-venv package." >&2; exit 1; }

mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$CONFIG_DIR" "$STATE_DIR"
[[ -d "$VENV_DIR" ]] || python3 -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install -r "$ROOT_DIR/requirements.txt"
cp "$ROOT_DIR/skyla.py" "$INSTALL_DIR/skyla.py"

if [[ ! -f "$CONFIG_DIR/config.json" ]]; then
  sed "s#__MODEL__#$MODEL#g; s#__STATE_DIR__#$STATE_DIR#g" "$ROOT_DIR/config/default.json" > "$CONFIG_DIR/config.json"
  echo "Created configuration: $CONFIG_DIR/config.json"
else
  echo "Keeping existing configuration: $CONFIG_DIR/config.json"
fi

cat > "$BIN_DIR/skyla" <<EOF
#!/usr/bin/env bash
exec "$VENV_DIR/bin/python" "$INSTALL_DIR/skyla.py" --config "$CONFIG_DIR/config.json" "\$@"
EOF
chmod +x "$BIN_DIR/skyla"

printf '\nSKYLA installation complete.\nStart with: %s\nStatus with: %s --status\n' "$BIN_DIR/skyla" "$BIN_DIR/skyla"
if command -v ollama >/dev/null 2>&1; then
  if ollama list 2>/dev/null | awk 'NR > 1 {print $1}' | grep -Fxq "$MODEL"; then echo "Ollama model '$MODEL' is available."; else echo "Ollama is installed, but '$MODEL' is missing. Run: ollama pull $MODEL"; fi
else
  echo "Ollama is not installed. Install it later if local model support is needed; then run: ollama pull $MODEL"
fi
[[ ":$PATH:" == *":$BIN_DIR:"* ]] || echo "For the 'skyla' command, add to PATH: export PATH=\"$BIN_DIR:\$PATH\""
