# API

Run `python -m skyla dashboard` and use localhost port 8765.

GET `/api/status`, `/api/models`, `/api/voice`, `/api/memory`, `/api/projects`, `/api/logs`

POST `/api/chat` or `/api/command` with `{"text":"open chrome"}`. Add `"confirmed":true` only for an action the user explicitly authorized.
