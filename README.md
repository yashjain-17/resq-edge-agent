# ResQ-Edge Agent

An offline-first tactical AI co-pilot and agent skill for emergency response drones.

## Open-Weight Model & License
- **Model:** Gemma 2 (9B) via [Ollama](https://ollama.com) (Terms: [Google Gemma License](https://ai.google.dev/gemma/terms))
- **License:** MIT License (see [LICENSE](LICENSE))

## How to Run
1. Pull and run your open-weight model locally:
   \\\ash
   ollama run gemma2:9b
   \\\
2. Start the FastAPI backend server:
   \\\ash
   python agent/server.py
   \\\

