# Development

Run `python -m pytest -q` for the dependency-free unit suite. Run `python -m skyla doctor` on the target Linux machine to inspect Ollama, PipeWire, Git, and the database. Use `scripts/backup.sh` before risky source edits.

Voice, TTS, web providers, and ESP32 transport are deliberately adapter seams until their local hardware/provider contracts are verified. No credentials are required for the foundation.
