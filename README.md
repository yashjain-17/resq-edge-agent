# ResQ-Edge Agent

A small FastAPI service that sends responder prompts and telemetry context to a locally running Ollama model. This is an experimental assistant for emergency-response drone workflows.

> **Safety notice:** This prototype must not control a drone or replace a trained pilot, incident commander, emergency service, or approved operating procedure. Verify every generated suggestion with qualified personnel.

## Repository layout

- `agent/server.py` — FastAPI endpoints and local Ollama integration
- `agent/test_server.py` — unit tests for health and query response handling
- `agent/skills/telemetry_parser/SKILL.md` — telemetry/mission-log skill description
- `requirements.txt` — Python dependencies

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com)
- Sufficient RAM/VRAM for Gemma 2 9B, or configure a model already installed locally

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

## Configuration

The API can be configured with environment variables:

| Variable | Default | Purpose |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://127.0.0.1:11434` | Base URL for the local Ollama service |
| `OLLAMA_MODEL` | `gemma2:9b` | Model name sent to Ollama |
| `OLLAMA_TIMEOUT_SECONDS` | `45` | Timeout for model generation requests |
| `RESQ_ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated browser origins allowed by CORS |
| `RESQ_HOST` | `127.0.0.1` | API bind address |
| `RESQ_PORT` | `8000` | API port |

CORS origin restrictions are a browser policy, not an authentication mechanism. Do not expose the development API to untrusted networks.

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

The API listens on `127.0.0.1:8000` by default.

- `GET /health` reports whether Ollama is reachable and whether the configured model is installed.
- `POST /api/agent/query` accepts a JSON body with `prompt` and optional `telemetry_context`.

Example request:

```json
{
  "prompt": "Summarize the current mission risks.",
  "telemetry_context": "Battery: 72%; GPS fix: 3D; link: stable"
}
```

## Run tests

From the repository root:

```bash
python -m unittest discover -s agent -p "test_*.py" -v
```

The tests mock the Ollama HTTP calls, so a running Ollama service is not required.

## Current limitations and safety boundaries

- The API has no authentication, authorization, or rate limiting. Keep it on a trusted local machine.
- Telemetry context is accepted as bounded free text; it is not yet validated against a typed telemetry schema.
- Responses are model-generated decision support and are not independently verified against flight rules, sensor truth, or mission procedures.
- Audit logging, operator approval workflows, and production deployment controls are not implemented.
- The telemetry parser skill describes intended capabilities; it does not prove that a telemetry parser is implemented or connected to the API.

Before any controlled field evaluation, add identity and access controls, a validated telemetry schema, audit trails, human approval gates, and a documented safety test plan. Test only with simulated data until the required reviews and safeguards are in place.

## License

See [LICENSE](LICENSE). The Gemma model is subject to its own terms: https://ai.google.dev/gemma/terms.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
