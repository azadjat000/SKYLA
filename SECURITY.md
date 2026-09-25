# Security

Risk levels are assigned before execution. Safe actions include status, memory, and known application launchers. Terminal and coding are not treated as arbitrary shell access. Raw Ollama output is never passed to `subprocess`.

Future high-risk actions must use an explicit confirmation token and an auditable plan. Keep the dashboard bound to `127.0.0.1` unless LAN access is deliberately configured.
