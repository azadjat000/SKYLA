# SKYLA

SKYLA is a minimal local-first terminal assistant for Linux. The current release integrates with Ollama to send user queries to a local language model (qwen3:1.7b by default) and display responses in the terminal.

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

Type a message to send it to the configured model, or use:

- `hello skyla` — test built-in response
- `--status` — show diagnostics
- `exit` — quit

## Status

```bash
./run.sh --status
```

Shows Ollama availability and the configured model status without requiring an API call.

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

The installer creates `$HOME/.config/skyla/config.json` and preserves it on repeat installs. Default model is `qwen3:1.7b`. To use a different model:

1. Edit `$HOME/.config/skyla/config.json` and change the `model` field
2. Make sure Ollama has the model installed: `ollama list` and `ollama pull <model>` if needed
3. Restart SKYLA

Ollama endpoint defaults to `http://localhost:11434` and can be customized in the configuration.

SKYLA will show clear errors if Ollama is not running or the model is missing.

## Dependencies

- Linux
- Python 3.10 or newer with `venv` support
- No third-party Python packages are currently required
- Ollama (optional, but needed for model responses)

## Tests

```bash
python3 -m unittest discover -v
```

Tests use mocks and do not require Ollama to be running.

## Real Ollama integration test

With Ollama running and qwen3:1.7b installed:

```bash
./run.sh
> what is 2+2?
Answer: 4 (or similar from the model)
> exit
```
