"""Minimal, configurable terminal core for SKYLA."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

VERSION = "0.2.0"
DEFAULT_CONFIG = {
    "version": VERSION,
    "model": "llama3.2",
    "log_file": "~/.local/state/skyla/skyla.log",
}


def load_config(path: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    """Load JSON configuration, falling back to safe built-in defaults."""
    config = dict(DEFAULT_CONFIG)
    if path is None:
        return config
    config_path = Path(path).expanduser()
    try:
        with config_path.open(encoding="utf-8") as handle:
            loaded = json.load(handle)
        if not isinstance(loaded, dict):
            raise ValueError("configuration must contain a JSON object")
        config.update(loaded)
    except FileNotFoundError:
        raise ValueError(f"configuration file not found: {config_path}") from None
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"unable to load configuration {config_path}: {exc}") from exc
    return config


def configure_logging(config: dict[str, Any]) -> logging.Logger:
    """Configure a small file logger without making logging a runtime dependency."""
    logger = logging.getLogger("skyla")
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    log_path = Path(str(config.get("log_file", DEFAULT_CONFIG["log_file"]))).expanduser()
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handler: logging.Handler = logging.FileHandler(log_path, encoding="utf-8")
    except OSError as exc:
        handler = logging.StreamHandler()
        logger.warning("Could not open log file %s: %s", log_path, exc)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    return logger


def respond(command: str) -> str:
    """Return SKYLA's response for a terminal command."""
    normalized = command.strip().lower()
    if normalized == "hello skyla":
        return "Hello! I am SKYLA."
    if normalized == "exit":
        return "Goodbye!"
    return "I don't understand that command yet."


def ollama_status(model: str) -> str:
    """Describe Ollama/model availability without requiring Ollama for core use."""
    executable = shutil.which("ollama")
    if executable is None:
        return "Ollama: not installed"
    try:
        result = subprocess.run(
            [executable, "list"], capture_output=True, text=True, timeout=5, check=False
        )
    except (OSError, subprocess.TimeoutExpired):
        return "Ollama: installed, but unavailable"
    if result.returncode != 0:
        return "Ollama: installed, but unavailable"
    models = {line.split()[0] for line in result.stdout.splitlines()[1:] if line.split()}
    return f"Ollama: installed; model {model}: " + ("available" if model in models else "missing")


def status(config: dict[str, Any]) -> str:
    """Return human-readable diagnostic information."""
    return "\n".join(
        [
            "SKYLA status: healthy",
            f"Version: {config.get('version', VERSION)}",
            f"Configured model: {config.get('model', DEFAULT_CONFIG['model'])}",
            ollama_status(str(config.get("model", DEFAULT_CONFIG["model"]))),
        ]
    )


def run(config: dict[str, Any] | None = None) -> None:
    """Start SKYLA and process terminal input until the user exits."""
    config = config or dict(DEFAULT_CONFIG)
    logger = configure_logging(config)
    logger.info("SKYLA started")
    print(f"SKYLA started (version {config.get('version', VERSION)})")
    print('Type "hello skyla" to test SKYLA, "--status" for diagnostics, or "exit" to quit.')
    while True:
        try:
            command = input("> ")
            if command.strip().lower() == "--status":
                print(status(config))
                continue
            print(respond(command))
            logger.info("Processed command: %s", command.strip().lower())
            if command.strip().lower() == "exit":
                break
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            logger.info("SKYLA stopped")
            break
        except Exception as exc:  # keep the terminal available after command errors
            logger.exception("Command handling failed")
            print(f"SKYLA error: {exc}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SKYLA local terminal assistant")
    parser.add_argument("--config", help="path to a JSON configuration file")
    parser.add_argument("--status", action="store_true", help="show diagnostics and exit")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        if args.status:
            print(status(config))
        else:
            run(config)
        return 0
    except ValueError as exc:
        print(f"SKYLA configuration error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
