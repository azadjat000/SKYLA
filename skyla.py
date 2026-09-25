"""Minimal, configurable terminal core for SKYLA with Ollama integration."""

from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

VERSION = "0.3.0"
DEFAULT_CONFIG = {
    "version": VERSION,
    "model": "qwen3:1.7b",
    "ollama_url": "http://localhost:11434",
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


def query_ollama(prompt: str, model: str, ollama_url: str) -> str:
    """Send a prompt to the Ollama API and return the response.

    Args:
        prompt: User's text input
        model: Model name (e.g., 'qwen3:1.7b')
        ollama_url: Base URL of the Ollama server (e.g., 'http://localhost:11434')

    Returns:
        The model's response text

    Raises:
        ValueError: If Ollama is unavailable or the model is missing
    """
    endpoint = f"{ollama_url}/api/generate"
    request_body = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    try:
        req = urllib.request.Request(endpoint, data=request_body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result.get("response", "")
    except urllib.error.URLError as exc:
        raise ValueError(f"Ollama server not available at {ollama_url}: {exc}") from exc
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise ValueError(f"Model '{model}' is not available. Install it with: ollama pull {model}") from exc
        raise ValueError(f"Ollama returned an error: {exc.code}") from exc
    except (TimeoutError, json.JSONDecodeError) as exc:
        raise ValueError(f"Ollama communication error: {exc}") from exc


def respond(command: str, config: dict[str, Any] | None = None, logger: logging.Logger | None = None) -> str:
    """Return SKYLA's response for a terminal command or AI query.

    Built-in commands (hello skyla, exit) are handled locally.
    Other input is sent to Ollama if configured.

    Args:
        command: User input
        config: Configuration dict (required for Ollama queries)
        logger: Optional logger

    Returns:
        Response string
    """
    normalized = command.strip().lower()
    if normalized == "hello skyla":
        return "Hello! I am SKYLA."
    if normalized == "exit":
        return "Goodbye!"
    if config is None:
        return "I don't understand that command yet."
    try:
        model = str(config.get("model", DEFAULT_CONFIG["model"]))
        ollama_url = str(config.get("ollama_url", DEFAULT_CONFIG["ollama_url"]))
        response = query_ollama(command.strip(), model, ollama_url)
        if logger:
            logger.info(f"Model response received for prompt: {command.strip()[:50]}")
        return response.strip()
    except ValueError as exc:
        if logger:
            logger.error(f"Ollama error: {exc}")
        return f"Error: {exc}"


def ollama_status(model: str, ollama_url: str) -> str:
    """Describe Ollama/model availability without requiring an API call."""
    executable = shutil.which("ollama")
    if executable is None:
        return "Ollama: not installed"
    try:
        result = subprocess.run([executable, "list"], capture_output=True, text=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return "Ollama: installed, but unavailable"
    if result.returncode != 0:
        return "Ollama: installed, but unavailable"
    models = {line.split()[0] for line in result.stdout.splitlines()[1:] if line.split()}
    return f"Ollama: installed; model {model}: " + ("available" if model in models else "missing")


def status(config: dict[str, Any]) -> str:
    """Return human-readable diagnostic information."""
    model = str(config.get("model", DEFAULT_CONFIG["model"]))
    ollama_url = str(config.get("ollama_url", DEFAULT_CONFIG["ollama_url"]))
    return "\n".join(
        [
            "SKYLA status: healthy",
            f"Version: {config.get('version', VERSION)}",
            f"Configured model: {model}",
            f"Ollama endpoint: {ollama_url}",
            ollama_status(model, ollama_url),
        ]
    )


def run(config: dict[str, Any] | None = None) -> None:
    """Start SKYLA and process terminal input until the user exits."""
    config = config or dict(DEFAULT_CONFIG)
    logger = configure_logging(config)
    logger.info("SKYLA started")
    print(f"SKYLA started (version {config.get('version', VERSION)})")
    print('Type "hello skyla" to test SKYLA, "--status" for diagnostics, or "exit" to quit.')
    print(f"Using model: {config.get('model', DEFAULT_CONFIG['model'])}")
    while True:
        try:
            command = input("> ")
            if command.strip().lower() == "--status":
                print(status(config))
                continue
            response = respond(command, config, logger)
            print(response)
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
