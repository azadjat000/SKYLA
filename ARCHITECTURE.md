# Architecture

`SkylaCore` coordinates configuration, routing, security, skills, memory, system monitoring, and AI. Deterministic intents run without an LLM. Ollama is an optional provider selected only for chat/coding/reasoning.

The current implementation is intentionally dependency-light and CPU-first. Optional voice adapters can be added behind a `VoiceEngine` interface without making text mode or the dashboard depend on audio hardware. The dashboard is a localhost-only Python HTTP service with real API values.

Future boundaries: `voice`, `tts`, `projects`, `tasks`, and `devices` should remain adapters around the core, not direct shell access.
