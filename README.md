# ResQ-Edge Agent

A small FastAPI service that sends responder prompts and telemetry context to a locally running Ollama model. This is an experimental assistant for emergency-response drone workflows.

> **Safety notice:** This prototype must not control a drone or replace a trained pilot, incident commander, emergency service, or approved operating procedure. Verify every generated suggestion with qualified personnel.

## Repository layout

- `agent/server.py` — FastAPI endpoint
- `agent/skills/telemetry_parser/SKILL.md` — telemetry/mission-log skill description
- `requirements.txt` — Python dependencies
- `LICENSE` — project license

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com)
- Sufficient RAM/VRAM for Gemma 2 9B, or change the model in `agent/server.py` to one installed locally

## Setup

From the repository root:

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Start the local model and API

In one terminal:

```bash
ollama pull gemma2:9b
ollama serve
```

If Ollama is already running as a service, leave it running and skip the second command.

In another terminal, from the repository root:

```bash
python agent/server.py
```

The API listens on port `8000`. The query endpoint is `POST /api/agent/query` and accepts a JSON body with `prompt` and optional `telemetry_context`.

## Current limitations

- The server currently uses a fixed Ollama URL and model name in source code.
- The HTTP request to Ollama does not currently set a timeout.
- CORS is permissive and the service has no authentication or authorization layer.
- The telemetry parser file documents intended tools; it does not by itself prove those tools are implemented or connected to the API.
- Do not expose this development server to the public internet or use it for live mission decisions.

## Validation before field research

Add input validation, request timeouts, authentication, origin restrictions, structured telemetry schemas, test fixtures, model failure handling, audit logging, and human approval gates. Test with simulated data before any controlled evaluation.

## License

See [LICENSE](LICENSE). The Gemma model is subject to its own terms: https://ai.google.dev/gemma/terms.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
