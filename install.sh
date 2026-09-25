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

if ! command -v python3 >/dev/null 2>&1; then
  echo "Missing dependency: python3. Install it with your Linux distribution's package manager." >&2
  exit 1
fi

if ! python3 - <<'PY'
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY
then
  echo "SKYLA requires Python 3.10 or newer." >&2
  exit 1
fi

mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$CONFIG_DIR" "$STATE_DIR"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

"$VENV_DIR/bin/python" -m pip install --upgrade pip >/dev/null
"$VENV_DIR/bin/python" -m pip install -r "$ROOT_DIR/requirements.txt"

cp "$ROOT_DIR/skyla.py" "$INSTALL_DIR/skyla.py"
cp "$ROOT_DIR/config/default.json" "$INSTALL_DIR/default.json"

if [[ ! -f "$CONFIG_DIR/config.json" ]]; then
  sed "s/__MODEL__/$MODEL/g; s#__STATE_DIR__#$STATE_DIR#g" \
    "$ROOT_DIR/config/default.json" > "$CONFIG_DIR/config.json"
  echo "Created configuration: $CONFIG_DIR/config.json"
else
  echo "Keeping existing configuration: $CONFIG_DIR/config.json"
fi

cat > "$BIN_DIR/skyla" <<EOF
#!/usr/bin/env bash
exec "$VENV_DIR/bin/python" "$INSTALL_DIR/skyla.py" --config "$CONFIG_DIR/config.json" "\$@"
EOF
chmod +x "$BIN_DIR/skyla"
chmod +x "$ROOT_DIR/run.sh" "$ROOT_DIR/uninstall.sh"

printf '\nSKYLA installation complete.\n'
printf 'Start: %s\n' "$BIN_DIR/skyla"
printf 'Status: %s --status\n' "$BIN_DIR/skyla"
printf 'Configuration: %s\n' "$CONFIG_DIR/config.json"

if ! command -v ollama >/dev/null 2>&1; then
  echo "Notice: Ollama is not installed. Install Ollama, then run: ollama pull $MODEL"
elif ! ollama list 2>/dev/null | awk 'NR > 1 {print $1}' | grep -Fxq "$MODEL"; then
  echo "Notice: Ollama model '$MODEL' is not installed. Run: ollama pull $MODEL"
else
  echo "Ollama model '$MODEL' is available."
fi

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
  echo "Add SKYLA to PATH for the 'skyla' command:"
  echo "  export PATH=\"$BIN_DIR:\$PATH\""
fi
