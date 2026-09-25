# SKYLA

**Systemic Knowledge & Yielding Local Assistant** — a local-first Linux assistant for Azad.

This repository contains the runnable CPU-first foundation: deterministic commands, safe computer actions, persistent SQLite memory, optional Ollama chat, system monitoring, a localhost dashboard, diagnostics, project discovery, tasks, and extension interfaces for voice, TTS, and future nodes.

## Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[test]'
python -m skyla doctor
python -m skyla dashboard
# open http://127.0.0.1:8765
```

Text mode:

```bash
python -m skyla
python -m skyla command 'open chrome'
python -m skyla status
```

The application continues to support deterministic commands when Ollama, audio, or optional Python packages are unavailable. Dangerous actions are never executed from raw model output.

See [ARCHITECTURE.md](ARCHITECTURE.md), [SECURITY.md](SECURITY.md), [VOICE.md](VOICE.md), and [API.md](API.md).
