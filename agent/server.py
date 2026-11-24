import os

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="ResQ-Edge Agent API", version="1.1.0")

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "RESQ_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "gemma2:9b")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "45"))


class QueryRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    telemetry_context: str = Field(default="", max_length=12000)


@app.get("/health")
def health_check():
    """Report local model availability without exposing internal exception details."""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Unexpected Ollama response.")
        models = payload.get("models", [])
        if not isinstance(models, list):
            raise ValueError("Unexpected Ollama model list.")
        return {
            "status": "online",
            "model_configured": MODEL_NAME,
            "model_available": any(
                isinstance(item, dict) and item.get("name") == MODEL_NAME
                for item in models
            ),
        }
    except (requests.RequestException, ValueError):
        return {"status": "offline", "model_configured": MODEL_NAME, "model_available": False}


@app.post("/api/agent/query")
def query_agent(req: QueryRequest):
    prompt = req.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=422, detail="Prompt cannot be blank.")

    system_prompt = (
        "You are ResQ-Edge Agent, a decision-support assistant for rescue-drone operators. "
        "Use only the supplied telemetry and mission context. Clearly distinguish observed "
        "telemetry from assumptions. If information is missing or contradictory, say so. "
        "Never claim to control a drone or issue flight commands. Human operators retain control."
    )
    full_prompt = (
        f"{system_prompt}\n\nTelemetry context:\n{req.telemetry_context.strip()}\n\n"
        f"Operator question:\n{prompt}"
    )

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": MODEL_NAME, "prompt": full_prompt, "stream": False},
            timeout=OLLAMA_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        result = response.json()
        if not isinstance(result, dict):
            raise HTTPException(
                status_code=502,
                detail="The local model returned an invalid response payload.",
            )

        raw_answer = result.get("response")
        if not isinstance(raw_answer, str):
            raise HTTPException(
                status_code=502,
                detail="The local model returned an invalid response payload.",
            )

        answer = raw_answer.strip()
        if not answer:
            raise HTTPException(status_code=502, detail="The local model returned an empty response.")
        return {"response": answer, "model": MODEL_NAME, "status": "generated"}
    except requests.Timeout as exc:
        raise HTTPException(status_code=504, detail="The local model request timed out.") from exc
    except requests.RequestException as exc:
        raise HTTPException(status_code=503, detail="The local Ollama service is unavailable.") from exc
    except ValueError as exc:
        raise HTTPException(status_code=502, detail="The local model returned invalid JSON.") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=os.getenv("RESQ_HOST", "127.0.0.1"),
        port=int(os.getenv("RESQ_PORT", "8000")),
    )
