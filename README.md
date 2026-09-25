# SKYLA

SKYLA is a minimal local-first terminal assistant foundation for Linux. The current release provides a terminal interface, configuration, logging, diagnostics, and safe installation scripts. Ollama is detected but is not required for the core terminal commands.

## Fresh installation

```bash
git clone https://github.com/azadjat000/SKYLA.git
cd SKYLA
chmod +x install.sh run.sh uninstall.sh
./install.sh
```

## Run

```bash
./run.sh
```

Type `hello skyla` or `exit`.

## Status

```bash
./run.sh --status
```

## Update

```bash
git pull
./install.sh
```

## Uninstall

```bash
./uninstall.sh
```

The uninstall script removes the installed runtime, launcher, configuration, and logs, but never removes this Git repository.

## Configuration and AI model

The installer creates `$HOME/.config/skyla/config.json` and preserves it on repeat installs. Set `SKYLA_MODEL` before a fresh install to choose the model name, or update the generated JSON configuration normally. If Ollama is installed, SKYLA reports whether the configured model exists. SKYLA never downloads a model automatically; download one explicitly with `ollama pull <model>`.

## Dependencies

- Linux
- Python 3.10 or newer with `venv` support
- No third-party Python packages are currently required
- Ollama is optional and only needed for future local-model integration

## Tests

```bash
python3 -m unittest discover -v
```
