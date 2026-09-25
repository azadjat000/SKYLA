# SKYLA Roadmap

SKYLA is being developed as a local-first personal assistant with a small, testable core.

## Completed foundation

- Linux terminal interface
- JSON configuration with validation
- File logging with safe fallback
- Ollama integration
- Progressive streaming responses
- Ollama/model availability diagnostics
- Built-in terminal commands
- CLI configuration override
- Reliable error handling
- Linux installation and isolated runtime
- Installed launcher
- Safe uninstall and cancellation behavior
- Automated regression test suite

Current baseline: **34 automated tests passing**.

## Development phases

### Phase 1 — Reliable Core
Status: completed.

The terminal core, configuration, model communication, diagnostics, installation lifecycle, and regression coverage are established.

### Phase 2 — Memory
Planned.

Goals:
- Local persistent memory
- Explicit remember/recall/forget commands
- Structured memory storage
- Safe memory boundaries
- Automated memory tests

### Phase 3 — Intent and Command Routing
Planned.

Goals:
- Separate local commands from AI queries
- Detect command intent
- Route requests to the appropriate subsystem
- Keep deterministic commands independent of the language model

### Phase 4 — Voice Interface
Planned.

Goals:
- Local speech recognition
- Wake phrase support
- Speech-to-text input
- Text-to-speech output
- Microphone/device diagnostics

### Phase 5 — PC Automation
Planned.

Goals:
- Controlled local application launching
- File and system operations
- Explicit confirmation for sensitive actions
- Auditable automation

### Phase 6 — Local Web Dashboard
Planned.

Goals:
- Local browser interface
- System status
- Conversation interface
- Configuration controls
- Memory management

### Phase 7 — Advanced AI Routing
Planned.

Goals:
- Multiple local models
- Fast/normal/reasoning model routing
- Coding-oriented routing
- Configurable model policies
- Graceful fallback behavior

### Phase 8 — Multi-device and Hardware
Planned.

Goals:
- Phone/tablet interface
- Local network communication
- Optional ESP32-based voice endpoint
- Device authentication and secure pairing

## Development rule

Each phase is implemented as small, testable tasks.

Before moving to the next architectural feature:
1. Make one focused change.
2. Run targeted tests.
3. Run the complete test suite.
4. Inspect the diff.
5. Commit the change.
6. Push to GitHub.
